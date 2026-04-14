# ============================================================
# PRÆCIS KURVEANALYSE: Horsens -> Aarhus
# ============================================================
# Denne kode henter OpenStreetMap jernbanedata, filtrerer
# korrekt strækning og beregner kurveradius i UTM (meter)
# ============================================================

import osmnx as ox
import geopandas as gpd
import numpy as np
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1) Hent jernbanedata
# ------------------------------------------------------------

place = "Denmark"
tags = {"railway": ["rail"]}

gdf = ox.features_from_place(place, tags)

# Bounding box (Horsens -> Aarhus)
bbox = (55.75, 56.1, 9.7, 10.3)
rail = gdf.cx[bbox[2]:bbox[3], bbox[0]:bbox[1]]

# Kun linjer
rail = rail[rail.geometry.type == "LineString"]

# ------------------------------------------------------------
# 2) Konverter til UTM (meter!)
# ------------------------------------------------------------

rail = rail.set_crs(epsg=4326)
rail_utm = rail.to_crs(epsg=32632)  # UTM zone 32N (Danmark)

# ------------------------------------------------------------
# 3) Saml koordinater
# ------------------------------------------------------------

coords = []
for line in rail_utm.geometry:
    coords.extend(list(line.coords))

coords = np.array(coords)

# ------------------------------------------------------------
# 4) Kurveradius funktion
# ------------------------------------------------------------

def curvature_radius(p1, p2, p3):
    a = np.linalg.norm(p2 - p1)
    b = np.linalg.norm(p3 - p2)
    c = np.linalg.norm(p3 - p1)

    s = (a + b + c) / 2
    area = np.sqrt(max(s*(s-a)*(s-b)*(s-c), 1e-12))

    if area == 0:
        return np.inf

    return (a*b*c) / (4*area)

# ------------------------------------------------------------
# 5) Beregn radius langs banen
# ------------------------------------------------------------

radii = []
points = []

for i in range(1, len(coords)-1):
    r = curvature_radius(coords[i-1], coords[i], coords[i+1])
    radii.append(r)
    points.append(coords[i])

radii = np.array(radii)
points = np.array(points)

# ------------------------------------------------------------
# 6) Filtrér ekstreme værdier
# ------------------------------------------------------------

# Fjern urealistisk store værdier (lige strækninger)
mask = radii < 5000  # kun relevante kurver
radii_filtered = radii[mask]
points_filtered = points[mask]

# ------------------------------------------------------------
# 7) Find top 10 værste kurver
# ------------------------------------------------------------

idx = np.argsort(radii_filtered)
top10 = idx[:10]

# Konverter tilbage til lat/lon
points_geo = gpd.GeoSeries(
    [LineString([p]) for p in points_filtered],
    crs="EPSG:32632"
).to_crs(epsg=4326)

print("\nTOP 10 VÆRSTE KURVER:\n")

for i in top10:
    pt = points_geo.iloc[i].coords[0]
    lat, lon = pt[1], pt[0]
    r = radii_filtered[i]

    print(f"Lat: {lat:.6f}, Lon: {lon:.6f}, Radius: {r:.1f} m")

# ------------------------------------------------------------
# 8) Plot resultat
# ------------------------------------------------------------

plt.figure()
plt.scatter(points_filtered[:,0], points_filtered[:,1], s=1)
plt.title("Kurver langs Horsens-Aarhus")
plt.xlabel("X (UTM)")
plt.ylabel("Y (UTM)")
plt.show()

# ============================================================
# NOTE:
# - Dette er ~ingeniørniveau hvis datakilden er præcis
# - For 100% præcision: brug Banedanmark LandXML
# ============================================================
