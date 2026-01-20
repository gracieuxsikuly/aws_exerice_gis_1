import geopandas as gpd
from matplotlib import pyplot as plt

pnvi=gpd.read_file("data1/pnvi.geojson")
# pnvi.plot()
# pnvi.to_crs(epsg=32735)
# buff_pnv=pnvi.buffer(2000)

# fig, axes =plt.subplots()
# buff_pnv.plot(ax=axes, facecolor="yellow")
# pnvi.plot(ax=axes,facecolor="blue")
# plt.show()
pnvi["envloppe"] = pnvi.buffer(2000)
pnvi_ndt = pnvi.set_geometry("envloppe")
pnvi_ndt.plot()
pnvi.plot()
plt.show()
# rectangle minimum envelopant la rdc

# rdc_province=gpd.read_file("data1/provinces.geojson")
# # rdc_pl=rdc_province.envelope.plot()
# # plt.show()
# rdc_all=rdc_province.union_all().envelope


# print("affichage des sommes")
# # print(rdc_all.bounds)
# # print(type(rdc_all))
# print("sommet de chaque province")
# print(rdc_province.envelope.bounds)
# rdc_all_gdf = gpd.GeoSeries(rdc_all)
# fig, axes =plt.subplots()
# rdc_all_gdf.plot(ax=axes, facecolor="yellow")
# rdc_province.boundary.plot(ax=axes,facecolor="red")
# plt.show()