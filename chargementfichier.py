import logging
from maclassetest import Maclasse
import geopandas as gpd
import matplotlib.pyplot as plt
from tabulate import tabulate
from io import BytesIO

logging.basicConfig(level=logging.INFO)
# instance de ma classe
con=Maclasse()
s3=con.connexion_s3()
# BUCKET_NAME ="mbau-gracieux-prive"
def chargement_fichier():
    s3_key = "raw/basedadaptationgeneralemutwangamangina.geojson"
    response = s3.get_object(
    Bucket=con.BUCKET_NAME,
    Key=s3_key,
    )
    contenu_data=response["Body"].read()
    gdf=gpd.read_file(BytesIO(contenu_data))
    # j'affiche l'echantillons de 3 entites
    logging.info(
    "\n%s",
    tabulate(
        gdf[["culture", "geometry"]].head(3),
        headers="keys",
        tablefmt="grid",
        showindex=False
    ))
# mon resultat de la validation
    MonResultat = [
    ["CRS", gdf.crs],
    ["Type géométrie",(gdf.geometry.geom_type.unique())],
    ["Nombre d'entités", len(gdf)],
    ["Géométries valides", f"{gdf.is_valid.sum()} / {len(gdf)}"],
    ]
    # affichage
    logging.info(
    "\n%s",
    tabulate(
        MonResultat,
        headers=["Information", "Valeur"],
        tablefmt="grid"
    ))
    gdf.plot()
    plt.show()
chargement_fichier()