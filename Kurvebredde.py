import osmnx as ox
import geopandas as gpd
import numpy as np
import requests
import pandas as pd
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ============================================================
# KONFIGURATION
# ============================================================

BBOX           = (9.7, 55.75, 10.3, 56.1)   # west, south, east, north
THRESHOLD_M    = 5_000                        # kurver under denne radius vises
GAUGE_MM       = 1_435
TRACK_CANT_MM  = 180                            # Sæt faktisk overhøjde her, hvis den kendes
DEFICIENCY_MM  = 150                          # Banedanmark standard (personvogne)
G              = 9.81

# Banedanmarks aktuelle åbne BTR-spordata.
# Den tidligere ArcGIS-URL til strækningsregisteret er ikke længere gyldig.
BTR_URL = (
    "https://gis.bane.dk/server/rest/services"
    "/OD/BTR_SPORDATA_M_OD/FeatureServer/0/query"
)

# ============================================================
# 1) Hent jernbanegeometri (OSM)
# ============================================================

rail = ox.features_from_bbox(bbox=BBOX, tags={"railway": ["rail"]})
rail = rail[rail.geometry.type == "LineString"]
rail = rail.set_crs(epsg=4326, allow_override=True)
rail_utm = rail.to_crs(epsg=32632)

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
            print("⚠ BTR-forespørgsel returnerede ingen data — falder tilbage til D=0.")
            return None

        return gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
    except Exception as e:
        print(f"⚠ BTR-forespørgsel fejlede ({e}) — falder tilbage til D=0.")
        return None

btr = fetch_btr_segments(BBOX)

# ============================================================
# 3) Sammenhæng mellem hastighed, radius og overhøjde
#    V² = g·R·(D+I)/G
#    D_req = V²·G/(g·R) - I
#    V_max = 3.6·√(g·R·(D+I)/G)
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
    D_mm = (V**2 * (GAUGE_MM/1000) / (G * radius_m) - DEFICIENCY_MM/1000) * 1000
    return max(D_mm, 0.0)

def max_speed_kmh(radius_m: np.ndarray | float, cant_mm: float = TRACK_CANT_MM) -> np.ndarray | float:
    """Beregn v_max ud fra radius og kendt/antaget overhøjde."""
    D = cant_mm / 1000
    I = DEFICIENCY_MM / 1000
    G_m = GAUGE_MM / 1000
    return 3.6 * np.sqrt(G * radius_m * (D + I) / G_m)

# ============================================================
# 4) Vektoriseret kurveradius per segment
# ============================================================

def segment_radii(coords: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if len(coords) < 3:
        return np.empty(0), np.empty((0, 2))
    p1, p2, p3 = coords[:-2], coords[1:-1], coords[2:]
    a = np.linalg.norm(p2 - p1, axis=1)
    b = np.linalg.norm(p3 - p2, axis=1)
    c = np.linalg.norm(p3 - p1, axis=1)
    s = (a + b + c) / 2
    area = np.sqrt(np.maximum(s*(s-a)*(s-b)*(s-c), 1e-12))
    return (a * b * c) / (4 * area), p2

all_radii, all_points = [], []
for line in rail_utm.geometry:
    r, pts = segment_radii(np.array(line.coords))
    if len(r):
        all_radii.append(r)
        all_points.append(pts)

radii  = np.concatenate(all_radii)
points = np.vstack(all_points)

# ============================================================
# 5) Filtrér og find top-10
# ============================================================

mask     = radii < THRESHOLD_M
radii_f  = radii[mask]
points_f = points[mask]

k       = min(10, len(radii_f))
top_idx = np.argpartition(radii_f, k-1)[:k]
top_idx = top_idx[np.argsort(radii_f[top_idx])]

# ============================================================
# 6) Konverter top-10 til lat/lon
# ============================================================

top_geo = gpd.GeoSeries(
    [Point(p) for p in points_f[top_idx]], crs="EPSG:32632"
).to_crs(epsg=4326)

# ============================================================
# 7) Slå nærmeste BTR-segment op
# ============================================================

def lookup_btr_segment(pt_wgs84: Point, btr_gdf: gpd.GeoDataFrame) -> pd.Series | None:
    """Finder nærmeste BTR-segment og returnerer hele rækken."""
    if btr_gdf is None or btr_gdf.empty:
        return None
    btr_utm = btr_gdf.to_crs(epsg=32632)
    pt_utm  = gpd.GeoSeries([pt_wgs84], crs=4326).to_crs(epsg=32632).iloc[0]
    dists   = btr_utm.geometry.distance(pt_utm)
    return btr_utm.loc[dists.idxmin()]

# ============================================================
# 8) Udskriv resultater
# ============================================================

print("\nTOP 10 SKARPESTE KURVER:\n")
print(f"{'#':>3}  {'Lat':>10}  {'Lon':>10}  {'Radius':>10}  "
      f"{'BTR-afsnit':<18}  {'Spor':<10}  {'Cant':>8}  {'V_max':>8}")
print("-" * 100)

for rank, (geom, i) in enumerate(zip(top_geo, top_idx), 1):
    r = radii_f[i]
    segment = lookup_btr_segment(geom, btr)
    section_name = "ukendt"
    track_name = "ukendt"
    if segment is not None:
        section_name = str(segment.get("STRKAFS_NAVN") or "ukendt")
        track_name = str(segment.get("SPORNUMMER") or "ukendt")

    v_max = max_speed_kmh(r, cant_mm=TRACK_CANT_MM)

    print(
        f"#{rank:2d}  "
        f"{geom.y:10.6f}  "
        f"{geom.x:10.6f}  "
        f"{r:8.1f} m  "
        f"{section_name[:18]:<18}  "
        f"{track_name[:10]:<10}  "
        f"{TRACK_CANT_MM:6.0f} mm  "
        f"{v_max[0] if hasattr(v_max, '__len__') else v_max:6.1f} km/t"
    )

print("\nNOTE: Banedanmarks aktuelle åbne BTR-spordata indeholder ikke linjehastighed.")
print(f"      V_max beregnes derfor med TRACK_CANT_MM = {TRACK_CANT_MM:.0f} mm.")
print("      Hvis du kender faktisk overhøjde i sporet, skal TRACK_CANT_MM sættes til den værdi.")

# ============================================================
# 9) Plot
# ============================================================

fig, ax = plt.subplots(figsize=(11, 7))

sc = ax.scatter(
    points_f[:, 0], points_f[:, 1],
    c=radii_f, cmap="RdYlGn",
    s=2, vmin=0, vmax=THRESHOLD_M
)

# Plot BTR-segmenter hvis tilgængelige
if btr is not None:
    btr_utm = btr.to_crs(epsg=32632)
    btr_utm.plot(ax=ax, color="steelblue", linewidth=1.5,
                 alpha=0.5, label="BTR-spordata")

ax.scatter(
    points_f[top_idx, 0], points_f[top_idx, 1],
    c="red", s=60, zorder=5, label="Top 10 skarpeste"
)

# Annoteringer
for geom, i in zip(top_geo, top_idx):
    r = radii_f[i]
    v          = max_speed_kmh(r, cant_mm=TRACK_CANT_MM)
    v_val      = v[0] if hasattr(v, "__len__") else v
    pt_utm     = gpd.GeoSeries([geom], crs=4326).to_crs(32632).iloc[0]
    ax.annotate(
        f"{v_val:.0f} km/t",
        xy=(pt_utm.x, pt_utm.y),
        xytext=(6, 6), textcoords="offset points",
        fontsize=7, color="darkred", fontweight="bold"
    )

plt.colorbar(sc, ax=ax, label="Kurveradius (m)")
ax.set_title(f"Horsens–Aarhus: Kurveradius og V_max (D={TRACK_CANT_MM:.0f} mm)")
ax.set_xlabel("X (UTM)")
ax.set_ylabel("Y (UTM)")
ax.legend()
plt.tight_layout()
plt.show()
