import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd
import requests
import shapely
from shapely.geometry import LineString, Point
from shapely.ops import linemerge

# ============================================================
# KONFIGURATION
# ============================================================

HORSENS_ST     = (9.8355, 55.8630)            # lon, lat (Horsens Station)
AARHUS_H       = (10.2045, 56.1500)           # lon, lat (Aarhus H)
BBOX           = (9.80, 55.84, 10.23, 56.16)  # west, south, east, north – kun Horsens–Aarhus
LINE_REF       = "23"                         # OSM ref for Fredericia–Aarhus (Østjyske Længdebane)

SPEED_LIMIT_KMH = 160                         # vis alle steder hvor V_max er under denne
RAIL_CENTRE_MM  = 1_500                       # afstand mellem skinnemidter (ikke sporvidden 1435 mm)
TRACK_CANT_MM   = 150                         # Sæt faktisk overhøjde her, hvis den kendes
DEFICIENCY_MM   = 150                         # tilladt manglende overhøjde (personvogne)
G               = 9.81

STEP_M          = 10                          # punktafstand ved resampling af sporet
HALF_CHORD_M    = 100                         # radius beregnes over en korde på 2·HALF_CHORD_M
MERGE_GAP_M     = 200                         # kurvestykker tættere end dette (langs banen) er samme sted
BTR_MAX_DIST_M  = 50                          # BTR-segment skal ligge så tæt på for at blive brugt

# Banedanmarks aktuelle åbne BTR-spordata.
BTR_URL = (
    "https://gis.bane.dk/server/rest/services"
    "/OD/BTR_SPORDATA_M_OD/FeatureServer/0/query"
)

# ============================================================
# 1) Hent jernbanegeometri (OSM) – kun hovedsporet Horsens–Aarhus
# ============================================================

rail = ox.features_from_bbox(bbox=BBOX, tags={"railway": "rail"})
rail = rail[rail.geometry.type == "LineString"]

def tag(gdf: gpd.GeoDataFrame, key: str) -> pd.Series:
    """OSM-tag som kolonne (NaN hvis tagget slet ikke findes i data)."""
    return gdf[key] if key in gdf.columns else pd.Series(np.nan, index=gdf.index)

# ref=23 er Østjyske Længdebane. Den Jyske Midtbane (Skanderborg–Silkeborg),
# Odderbanen, sidespor, rangerspor og sporskifteforbindelser sorteres fra.
line = rail[(tag(rail, "ref") == LINE_REF) & tag(rail, "service").isna()]
line_utm = line.to_crs(epsg=32632)

stations_utm = gpd.GeoSeries(
    [Point(HORSENS_ST), Point(AARHUS_H)], crs="EPSG:4326"
).to_crs(epsg=32632)

# OSM deler sporet op i mange korte ways. Sæt dem sammen til sammenhængende spor,
# så kurver ikke bliver skåret over ved hver way-grænse.
tracks = list(shapely.get_parts(linemerge(list(line_utm.geometry))))

# Det længste spor bruges som reference for kilometrering fra Horsens.
reference = max(tracks, key=lambda t: t.length)
pos_horsens, pos_aarhus = (reference.project(p) for p in stations_utm)

def km_from_horsens(pts: np.ndarray) -> np.ndarray:
    """Afstand langs banen fra Horsens (km), uanset hvilken vej referencen er tegnet."""
    pos = reference.project(shapely.points(pts))
    return np.sign(pos_aarhus - pos_horsens) * (pos - pos_horsens) / 1000

stretch_km = abs(pos_aarhus - pos_horsens) / 1000

# ============================================================
# 2) Hent BTR-spordata fra Banedanmarks åbne data (GeoJSON)
# ============================================================

def fetch_btr_segments(bbox) -> gpd.GeoDataFrame | None:
    """
    Henter BTR-spordata fra Banedanmarks åbne ArcGIS FeatureServer.
    Returnerer GeoDataFrame i EPSG:4326.
    bbox = (west, south, east, north)
    """
    west, south, east, north = bbox
    base_params = {
        "f":            "geojson",
        "where":        "1=1",
        "outFields":    "OBJECTID,KPMSTRK,STRKAFS,STRKAFS_NAVN,SPORNUMMER",
        "orderByFields": "OBJECTID",
        "geometry":     f"{west},{south},{east},{north}",
        "geometryType": "esriGeometryEnvelope",
        "inSR":         "4326",
        "spatialRel":   "esriSpatialRelIntersects",
        "returnGeometry": "true",
        "outSR":        "4326",
    }
    try:
        features = []
        offset = 0
        page_size = 2000

        while True:
            params = base_params | {
                "resultOffset": offset,
                "resultRecordCount": page_size,
            }
            r = requests.get(BTR_URL, params=params, timeout=20)
            r.raise_for_status()

            data = r.json()
            page_features = data.get("features", [])
            if not page_features:
                break

            features.extend(page_features)
            if len(page_features) < page_size:
                break

            offset += len(page_features)

        if not features:
            print("⚠ BTR-forespørgsel returnerede ingen data — fortsætter uden BTR-info.")
            return None

        return gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
    except (requests.RequestException, ValueError) as e:
        print(f"⚠ BTR-forespørgsel fejlede ({e}) — fortsætter uden BTR-info.")
        return None

btr = fetch_btr_segments(BBOX)

# Behold kun BTR-segmenter langs hovedsporet (ikke fx sporet vest for Skanderborg).
btr_utm = None
if btr is not None:
    btr_utm = btr.to_crs(epsg=32632)
    corridor = line_utm.geometry.union_all().buffer(BTR_MAX_DIST_M)
    btr_utm = btr_utm[btr_utm.intersects(corridor)]

# ============================================================
# 3) Sammenhæng mellem hastighed, radius og overhøjde
#    V² = g·R·(D+I)/e        (e = afstand mellem skinnemidter)
#    D_req = V²·e/(g·R) - I
#    V_max = 3.6·√(g·R·(D+I)/e)
# ============================================================

def required_cant_mm(speed_kmh: float, radius_m: float) -> float:
    """
    Beregner den overhøjde (mm), der kræves for at køre med speed_kmh
    ved den valgte tilladte overhøjdeunderskud.

    Brug denne til kontrol mod en kendt linehastighed.
    Brug den ikke som input til v_max-beregning, medmindre du vil
    rekonstruere den samme hastighed.
    """
    V = speed_kmh / 3.6
    D_mm = (V**2 * (RAIL_CENTRE_MM/1000) / (G * radius_m) - DEFICIENCY_MM/1000) * 1000
    return max(D_mm, 0.0)

def max_speed_kmh(radius_m: np.ndarray | float, cant_mm: float = TRACK_CANT_MM) -> np.ndarray | float:
    """Beregn v_max ud fra radius og kendt/antaget overhøjde."""
    D = cant_mm / 1000
    I = DEFICIENCY_MM / 1000
    e = RAIL_CENTRE_MM / 1000
    return 3.6 * np.sqrt(G * radius_m * (D + I) / e)

# ============================================================
# 4) Kurveradius langs hvert spor
# ============================================================

def resample(track: LineString, step: float) -> np.ndarray:
    """Punkter med fast afstand langs sporet (OSM-knuder ligger meget ujævnt)."""
    dists = np.arange(0, track.length, step)
    return shapely.get_coordinates(shapely.line_interpolate_point(track, dists))

def track_radii(pts: np.ndarray, k: int) -> np.ndarray:
    """
    Omskreven cirkel gennem punkterne i-k, i, i+k. En lang korde udglatter
    små unøjagtigheder i OSM-geometrien, som ellers giver falske skarpe kurver.
    Punkter nærmere end k fra sporets ender får radius = inf.
    """
    radii = np.full(len(pts), np.inf)
    if len(pts) < 2*k + 1:
        return radii
    p1, p2, p3 = pts[:-2*k], pts[k:-k], pts[2*k:]
    a = np.linalg.norm(p2 - p1, axis=1)
    b = np.linalg.norm(p3 - p2, axis=1)
    c = np.linalg.norm(p3 - p1, axis=1)
    u, v = p2 - p1, p3 - p1
    cross = np.abs(u[:, 0]*v[:, 1] - u[:, 1]*v[:, 0])
    with np.errstate(divide="ignore"):
        radii[k:-k] = np.where(cross > 1e-9, a * b * c / (2 * cross), np.inf)
    return radii

k = HALF_CHORD_M // STEP_M
samples = []   # én DataFrame pr. spor
for track_id, track in enumerate(tracks):
    pts = resample(track, STEP_M)
    df = pd.DataFrame({"x": pts[:, 0], "y": pts[:, 1], "radius": track_radii(pts, k)})
    df["track"] = track_id
    df["km"] = km_from_horsens(pts)
    samples.append(df)

samples = pd.concat(samples, ignore_index=True)
samples = samples[samples["km"].between(0, stretch_km)]
samples["v_max"] = max_speed_kmh(samples["radius"].to_numpy())

# ============================================================
# 5) Find alle steder hvor V_max < SPEED_LIMIT_KMH
# ============================================================

slow = samples[samples["v_max"] < SPEED_LIMIT_KMH].sort_values("km")

# Punkter der ligger tæt langs banen er samme kurve – også når de ligger på
# hvert sit spor (dobbeltspor), da kilometreringen er fælles for alle spor.
slow["place"] = (slow["km"].diff() > MERGE_GAP_M / 1000).cumsum()

places = []
for _, g in slow.groupby("place"):
    sharpest = g.loc[g["radius"].idxmin()]
    places.append({
        "km_start": g["km"].min(),
        "km_end":   g["km"].max(),
        "x":        sharpest["x"],
        "y":        sharpest["y"],
        "radius":   sharpest["radius"],
        "v_max":    sharpest["v_max"],
        "n_tracks": g["track"].nunique(),
    })
places = pd.DataFrame(places).sort_values("km_start", ignore_index=True)

places_geo = gpd.GeoSeries(
    gpd.points_from_xy(places["x"], places["y"]), crs="EPSG:32632"
).to_crs(epsg=4326)

# ============================================================
# 6) Slå nærmeste BTR-segment og OSM-strækningshastighed op
# ============================================================

def nearest_row(pt_utm: Point, gdf_utm: gpd.GeoDataFrame | None) -> pd.Series | None:
    """Nærmeste række inden for BTR_MAX_DIST_M, ellers None."""
    if gdf_utm is None or gdf_utm.empty:
        return None
    dists = gdf_utm.geometry.distance(pt_utm)
    if dists.min() > BTR_MAX_DIST_M:
        return None
    return gdf_utm.loc[dists.idxmin()]

# ============================================================
# 7) Udskriv resultater
# ============================================================

print(f"\nALLE STEDER HORSENS–AARHUS MED V_MAX UNDER {SPEED_LIMIT_KMH} KM/T "
      f"({len(places)} steder):\n")
print(f"{'#':>3}  {'km fra Horsens':>14}  {'Lat':>10}  {'Lon':>10}  {'Min. radius':>11}  "
      f"{'V_max':>10}  {'OSM-maks':>8}  {'Spor':>4}  {'BTR-afsnit':<18}  {'BTR-spor':<10}")
print("-" * 120)

for rank, (row, geom) in enumerate(zip(places.itertuples(), places_geo), 1):
    pt_utm = Point(row.x, row.y)

    osm_way = nearest_row(pt_utm, line_utm)
    osm_speed = "?"
    if osm_way is not None and pd.notna(osm_way.get("maxspeed")):
        osm_speed = str(osm_way["maxspeed"])

    section_name = "ukendt"
    track_name = "ukendt"
    segment = nearest_row(pt_utm, btr_utm)
    if segment is not None:
        section_name = str(segment.get("STRKAFS_NAVN") or "ukendt")
        track_name = str(segment.get("SPORNUMMER") or "ukendt")

    print(
        f"#{rank:2d}  "
        f"{row.km_start:6.2f}–{row.km_end:6.2f}  "
        f"{geom.y:10.6f}  "
        f"{geom.x:10.6f}  "
        f"{row.radius:9.0f} m  "
        f"{row.v_max:5.1f} km/t  "
        f"{osm_speed:>8}  "
        f"{row.n_tracks:4d}  "
        f"{section_name[:18]:<18}  "
        f"{track_name[:10]:<10}"
    )

print(f"\nNOTE: V_max beregnes med overhøjde D = {TRACK_CANT_MM:.0f} mm og "
      f"manglende overhøjde I = {DEFICIENCY_MM:.0f} mm.")
print("      Banedanmarks åbne BTR-spordata indeholder ikke overhøjde eller linjehastighed.")
print("      Hvis du kender faktisk overhøjde i sporet, skal TRACK_CANT_MM sættes til den værdi.")
print("      'OSM-maks' er den skiltede strækningshastighed fra OpenStreetMap (til sammenligning).")

# ============================================================
# 8) Plot
# ============================================================

fig, ax = plt.subplots(figsize=(11, 9))

if btr_utm is not None and not btr_utm.empty:
    btr_utm.plot(ax=ax, color="steelblue", linewidth=1.5, alpha=0.5)

sc = ax.scatter(
    samples["x"], samples["y"],
    c=samples["v_max"].clip(upper=250), cmap="RdYlGn",
    s=2, vmin=80, vmax=250
)

ax.scatter(
    places["x"], places["y"],
    facecolors="none", edgecolors="red", s=80, linewidths=1.5, zorder=5,
    label=f"V_max < {SPEED_LIMIT_KMH} km/t"
)

for rank, row in enumerate(places.itertuples(), 1):
    ax.annotate(
        f"#{rank}",
        xy=(row.x, row.y),
        xytext=(6, 6), textcoords="offset points",
        fontsize=7, color="darkred", fontweight="bold"
    )

for name, st in zip(["Horsens", "Aarhus H"], stations_utm):
    ax.plot(st.x, st.y, "ks", markersize=6)
    ax.annotate(name, xy=(st.x, st.y), xytext=(-10, -14), textcoords="offset points")

plt.colorbar(sc, ax=ax, label="V_max (km/t)")
ax.set_title(f"Horsens–Aarhus: V_max ud fra kurveradius "
             f"(D={TRACK_CANT_MM:.0f} mm, I={DEFICIENCY_MM:.0f} mm)")
ax.set_xlabel("X (UTM 32N, m)")
ax.set_ylabel("Y (UTM 32N, m)")
ax.set_aspect("equal")
ax.legend()
plt.tight_layout()
plt.show()
