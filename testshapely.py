import shapely as sp
from shapely.validation import explain_validity
import matplotlib.pyplot as plt
import geopandas as gpd
triangle = sp.Polygon([
    (0, 0),
    (0, 1),
    (1, 1),
])

print("triangle valide ? :", triangle.is_valid)
print("test valide :", explain_validity(triangle))

# gdf = gpd.GeoDataFrame(geometry=[triangle])
# gdf.plot()
# plt.show()
carre=sp.Polygon([
    (20,50),
    (20,60),
    (10,90),
    (20,40),
])
print(sp.bounds(carre))
print(sp.area(carre))
# print("test valide :", explain_validity(carre))
# gdf=gpd.GeoDataFrame(geometry=[carre])
# gdf.plot()
# plt.show()
# forme_invalide = Polygon([
#     (0, 0),
#     (1, 0),
#     (0, 1),
#     (1, 1)
# ])
# print("forme_invalide valide ? :",forme_invalide.is_valid)
# print("test valide :", explain_validity(forme_invalide))
# gdf=gpd.GeoDataFrame(geometry=[forme_invalide])
# gdf.plot()
# plt.show()

point1 = sp.Point(90, 100)
point2 = sp.Point(40, 70)
dst=sp.distance(point1,point2)
print(dst)
print("notre centroide",sp.centroid(carre))
lign=[((0, 0), (1, 1)), ((-1, 0), (1, 0))]
mult=sp.MultiLineString(lign)

gdf=gpd.GeoDataFrame(geometry=[mult])
gdf.plot()
plt.show()