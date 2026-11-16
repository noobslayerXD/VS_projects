"""
Køretidssimulering: InterCityLyn København H -> Aalborg
Sammenligner IC3, IC5 (Coradia Stream), Desiro HC og Velaro Novo.

Scenarie 1: Toget begrænses af BÅDE sin egen tophastighed og strækningshastigheden.
Scenarie 2: Kun togets egne grænser (tophastighed, trækkraft/effekt, kørselsmodstand, bremsning).

Metode: Fremad/baglæns integration på et afstandsgitter (dx = 5 m).
  - Fremad:   v[i+1]^2 = v[i]^2 + 2*a(v)*dx, a(v) = (F_trækkraft(v) - R(v)) / m_eff
  - Baglæns:  v[i]^2 <= v[i+1]^2 + 2*b*dx  (konstant driftsbremsning b)
  - Hale-regel: toget må først accelerere, når hele toglængden har forladt
    en lavere hastighedsbegrænsning.
Resultatet er TEKNISK MINIMUMSKØRETID (ingen køreplanstillæg, ingen gradienter).
"""

import numpy as np

DX = 5.0       # m, gitteropløsning
B_SERVICE = 0.6  # m/s^2, driftsbremsning (samme for alle tog for fair sammenligning)

# ------------------------------------------------------------------
# Togdata (kilder: DSB, Siemens datablade, Wikipedia - se svar)
# m = tjenestemasse + passagerer (80 kg/plads), P = trækeffekt ved hjul,
# F0 = starttrækkraft, Davis-modstand R = A + B*v + C*v^2  [N, v i m/s]
# A/B/C er ingeniørskøn - IKKE fabrikantdata.
# ------------------------------------------------------------------
TRAINS = {
    "IC3": dict(
        m=97e3 + 11e3, rot=1.08, P=1100e3, F0=72e3, vmax=180, L=58.8,
        A=1600, B=20, C=5.5,
        note="Diesel-mek., 4 motorer (~1.370 kW), ~0,6 m/s^2 start"),
    "IC5": dict(
        m=205e3 + 24e3, rot=1.06, P=5600e3, F0=295e3, vmax=200, L=109.4,
        A=2700, B=40, C=6.8,
        note="Coradia Stream, 5.930 kW, 1,2 m/s^2 (0-70 km/t)"),
    "Desiro HC": dict(
        m=200e3 + 32e3, rot=1.06, P=4000e3, F0=274e3, vmax=160, L=105.3,
        A=2700, B=40, C=7.2,
        note="4-vogns, 4.000 kW, op til 1,1 m/s^2"),
    "Velaro Novo": dict(
        m=420e3 + 36e3, rot=1.04, P=8000e3, F0=275e3, vmax=360, L=202.0,
        A=4900, B=60, C=5.8,
        note="7-vogns 360 km/t-variant, 8.000 kW, 275 kN"),
}

# ------------------------------------------------------------------
# Strækning: IC Lyn stopmønster K26 (Kbh H - Odense - Fredericia - Vejle -
# Horsens - Skanderborg - Aarhus H - Randers - Hobro - Aalborg)
# Hver delstrækning: (navn, længde_km, [(fra_km, til_km, km/t), ...])
# Hastighedsprofiler er forenklede skøn ud fra Banedanmark/TRM-kilder.
# ------------------------------------------------------------------
LEGS = [
    ("København H - Odense", 163.0, [
        (0, 1.5, 60), (1.5, 4.5, 80), (4.5, 8, 160), (8, 36, 200),
        (36, 42, 180), (42, 62, 200), (62, 67, 160), (67, 158, 180),
        (158, 161.5, 120), (161.5, 163.0, 80)]),
    ("Odense - Fredericia", 58.0, [
        (0, 1.5, 80), (1.5, 4, 120), (4, 52, 180), (52, 55, 160),
        (55, 58.0, 120)]),
    ("Fredericia - Vejle", 26.0, [
        (0, 3, 120), (3, 10, 140), (10, 22, 160), (22, 26.0, 100)]),
    ("Vejle - Horsens", 30.0, [
        (0, 3, 100), (3, 26, 180), (26, 30.0, 120)]),
    ("Horsens - Skanderborg", 28.0, [
        (0, 3, 120), (3, 25, 180), (25, 28.0, 140)]),
    ("Skanderborg - Aarhus H", 24.5, [
        (0, 2, 140), (2, 19, 180), (19, 22.5, 120), (22.5, 24.5, 60)]),
    ("Aarhus H - Randers", 59.2, [
        (0, 2, 60), (2, 6, 120), (6, 25, 160), (25, 35, 140), (35, 45, 160),
        (45, 48, 120), (48, 56, 160), (56, 59.2, 120)]),
    ("Randers - Hobro", 31.3, [
        (0, 2, 100), (2, 29, 180), (29, 31.3, 120)]),
    ("Hobro - Aalborg", 49.4, [
        (0, 2, 120), (2, 46, 180), (46, 49.4, 100)]),
]

# Opholdstider fra DSB K26 (min) ved mellemstationerne
DWELL_MIN = {"Odense": 3, "Fredericia": 4, "Vejle": 1, "Horsens": 1,
             "Skanderborg": 1, "Aarhus H": 7, "Randers": 1, "Hobro": 1}

# Køreplan K26, tog l 27 (Kbh H 7.52 -> Aalborg 11.53): køretid pr. delstrækning (min)
TIMETABLE_RUN_MIN = [71, 28, 14, 16, 14, 13, 29, 14, 23]


def line_limit(length_km, profile, x):
    """Strækningshastighed [m/s] i hvert gitterpunkt."""
    v = np.full_like(x, np.inf)
    for a, b, kmh in profile:
        sel = (x >= a * 1000) & (x <= b * 1000)
        v[sel] = np.minimum(v[sel], kmh / 3.6)
    return v


def apply_tail_rule(vlim, L, dx):
    """Begrænsning gælder indtil togets hale har passeret: min over [x-L, x]."""
    n = int(np.ceil(L / dx))
    out = vlim.copy()
    for k in range(1, n + 1):
        out[k:] = np.minimum(out[k:], vlim[:-k])
    return out


def accel(v, t):
    F = t["F0"] if v < 1e-3 else min(t["F0"], t["P"] / v)
    R = t["A"] + t["B"] * v + t["C"] * v * v
    return (F - R) / (t["m"] * t["rot"])


def run_leg(length_km, profile, t, use_line_speed=True):
    x = np.arange(0, length_km * 1000 + DX, DX)
    vlim = np.full_like(x, t["vmax"] / 3.6)
    if use_line_speed:
        vlim = np.minimum(vlim, line_limit(length_km, profile, x))
        vlim = apply_tail_rule(vlim, t["L"], DX)

    # Fremadpass (acceleration)
    vf = np.zeros_like(x)
    for i in range(len(x) - 1):
        a = accel(vf[i], t)
        v2 = vf[i] ** 2 + 2 * max(a, 0.0) * DX
        vf[i + 1] = min(np.sqrt(v2), vlim[i + 1])

    # Baglænspass (bremsning til stop og før lavere begrænsninger)
    vb = np.zeros_like(x)
    vb[-1] = 0.0
    for i in range(len(x) - 2, -1, -1):
        vb[i] = min(vf[i], np.sqrt(vb[i + 1] ** 2 + 2 * B_SERVICE * DX))

    v = vb
    vm = 0.5 * (v[:-1] + v[1:])
    vm[vm < 0.05] = 0.05  # undgå division med 0 ved start
    # Præcis tid i første/sidste celle (v starter/slutter i 0)
    dt = DX / vm
    return dt.sum(), x, v


def simulate():
    results = {}
    for name, t in TRAINS.items():
        results[name] = {}
        for scen, use in (("med", True), ("uden", False)):
            legs = [run_leg(L, prof, t, use)[0] / 60 for _, L, prof in LEGS]
            results[name][scen] = legs
    return results


def fmt(mins):
    h = int(mins // 60)
    m = mins - 60 * h
    return f"{h}:{m:04.1f}"


if __name__ == "__main__":
    res = simulate()
    dwell = sum(DWELL_MIN.values())
    total_km = sum(L for _, L, _ in LEGS)
    print(f"Strækning: {total_km:.1f} km, {len(LEGS)} delstrækninger, ophold {dwell} min\n")

    for scen, title in (("med", "SCENARIE 1: med strækningshastigheder"),
                        ("uden", "SCENARIE 2: kun togets egne grænser")):
        print(title)
        print(f"{'Tog':<12}{'Køretid':>10}{'+ophold':>10}{'Snit km/t':>11}{'vs IC3':>10}")
        base = sum(res["IC3"][scen])
        for name in TRAINS:
            run = sum(res[name][scen])
            print(f"{name:<12}{fmt(run):>10}{fmt(run + dwell):>10}"
                  f"{total_km / (run / 60):>11.1f}{run - base:>+10.1f}")
        print()

    print("Delstrækninger, scenarie 1 (min) og IC3 mod køreplan K26:")
    hdr = f"{'Delstrækning':<24}" + "".join(f"{n:>12}" for n in TRAINS) + f"{'K26':>8}"
    print(hdr)
    for i, (leg, _, _) in enumerate(LEGS):
        row = f"{leg:<24}" + "".join(f"{res[n]['med'][i]:>12.1f}" for n in TRAINS)
        print(row + f"{TIMETABLE_RUN_MIN[i]:>8}")
    ic3 = sum(res["IC3"]["med"])
    tt = sum(TIMETABLE_RUN_MIN)
    print(f"\nIC3 simuleret {ic3:.1f} min mod køreplan {tt} min "
          f"(køreplanstillæg ≈ {100 * (tt - ic3) / ic3:.1f} %)")
