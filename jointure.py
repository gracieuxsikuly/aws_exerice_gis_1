import shapely.geometry as sp
import geopandas as gpd
import matplotlib.pyplot as plt


# mes lignes
line_a = sp.LineString([(0, 0), (4, 4)])
line_b = sp.LineString([(0, 4), (4, 0)])
# mes polys
poly1 = sp.Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
poly2 = sp.Polygon([(2, 2), (6, 2), (6, 6), (2, 6)])
# mes points
point_1 = sp.Point(1, 1)
point_2 = sp.Point(4, 2)



# intersects, within, contains, overlaps, touches, covers, covered_by, equals, disjoint, crosses

print("=== TESTS LIGNES ===")
print("line_a intersects line_b :", line_a.intersects(line_b))
print("line_a within line_b :", line_a.within(line_b))
print("line_a containts line_b    :", line_a.contains(line_b))
print("line_a overlaps line_b    :", line_a.overlaps(line_b))
print("line_a touches line_b    :", line_a.touches(line_b))
print("line_a coverd line_b    :", line_a.covers(line_b))
print("line_a covered_by line_b    :", line_a.covered_by(line_b))
print("line_a equals line_b    :", line_a.equals(line_b))
print("line_a disjoint line_b   :", line_a.disjoint(line_b))
print("line_a crosses line_b    :", line_a.crosses(line_b))

print("=== TESTS POLYGONES ===")
print("poly1 intersects poly2 :", poly1.intersects(poly2))
print("poly1 within poly2 :", poly1.within(poly2))
print("poly1 containts poly2    :", poly1.contains(poly2))
print("poly1 overlaps poly2    :", poly1.overlaps(poly2))
print("poly1 touches poly2    :", poly1.touches(poly2))
print("poly1 coverd point_1    :", poly1.covers(point_1))
print("poly1 covered_by poly2    :", poly1.covered_by(poly2))
print("poly1 equals poly2    :", poly1.equals(poly2))
print("poly1 disjoint poly2   :", poly1.disjoint(poly2))
print("poly1 crosses poly2    :", poly1.crosses(poly2))

print("\n=== TESTS POINTS ===")
print("point_1 intersects point_2 :", point_1.intersects(point_2))
print("point_1 within point_2 :", point_1.within(point_2))
print("point_1 containts point_2    :", point_1.contains(point_2))
print("point_1 overlaps point_2    :", point_1.overlaps(point_2))
print("point_1 touches point_2    :", point_1.touches(point_2))
print("point_1 coverd point_2    :", point_1.covers(point_2))
print("point_1 covered_by point_2    :", point_1.covered_by(point_2))
print("point_1 equals point_2    :", point_2.equals(point_2))
print("point_1 disjoint poly2   :", point_1.disjoint(poly2))
print("point_1 crosses point_2    :", point_1.crosses(point_2))
print("point_1 within poly1 :", point_1.within(poly1))
print("point_2 touches poly1 :", point_2.touches(poly1))
gdf_polygons = gpd.GeoDataFrame({"name": ["poly1", "poly2"]}, geometry=[poly1, poly2])
gdf_lines = gpd.GeoDataFrame({"name": ["line_a", "line_b"]}, geometry=[line_a, line_b])
gdf_points = gpd.GeoDataFrame(
    {
        "name": [
            "point_1",
            "point_2",
        ]
    },
    geometry=[point_1, point_2],
)
fig, ax = plt.subplots(figsize=(8, 8))
# couleurs de mes polygones kkkkkkk
gdf_polygons.plot(ax=ax, alpha=0.4, edgecolor="black", cmap="Set2")
# couleurs de mes lignes apa sasa
gdf_lines.plot(ax=ax, color=["red", "blue", "green"], linewidth=2)
# couleurs de mes points hahahahaha taille 80
gdf_points.plot(ax=ax, color=["orange", "purple"], markersize=80)
ax.set_title("KA EXERCICE KETU AKAA", fontsize=14)
ax.set_aspect("equal")
plt.show()
