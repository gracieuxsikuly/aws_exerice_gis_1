import shapely as sp
from shapely.validation import explain_validity
import matplotlib.pyplot as plt
import geopandas as gpd
from pathlib import Path
import os


data_folder = Path("data1")
provinces_file = data_folder / "provinces.geojson"
pnvi_file = data_folder / "pnvi.geojson"
fichier_final = data_folder / "province_avec_distance_au_parc.geojson"

provinces=gpd.read_file(provinces_file)
pnvi=gpd.read_file(pnvi_file)


centroid_prov=provinces.centroid
centroid_pnvi=pnvi.centroid
provinces["distance_parc_m"] =(centroid_prov.geometry.distance(centroid_pnvi.iloc[0]))/1000
provinces["superficie_km2"]=(provinces.geometry.area)/1000000
if os.path.exists(fichier_final):
    os.remove(fichier_final)
    provinces.to_file(fichier_final,driver="GEOJSON")
print(f"Nouvelle couche créée avec succès : {fichier_final}")
print("EHCANTILLON DE MON RESULTAT")
prov_dst=gpd.read_file(fichier_final)
print(prov_dst.head(6))