import geopandas as gpd
from maclassetest import Maclasse
import os
import logging
from tabulate import tabulate

con=Maclasse()
s3=con.connexion_s3()
RAW_FOLDER ="raw"
PROCESS_FOLDER = "processed"
OUTPUT_FOLDER = "validated"
MES_FILES={
    "palmiers": "basedadaptationgeneralemutwangamangina.geojson",
    "routes" : "routes.geojson",
    "zone" : "Zoneculture.geojson"
}
CRS_METRIQUE= "EPSG:32735"
LOG_DIR = "/tmp/logs"
LOG_FILE = f"{LOG_DIR}/execution.log"
os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)

logging.info("Demarage de notre scrypt")
print("Demarage de notre scrypt")

def copy_raw_to_process(filename):
    """Copies a file from the raw folder to the processed folder in S3.
    Params:
        filename (str): Filename to be fetched from the raw folder and copied
            to the processed folder.
    Returns:
        None
    """
    source_key=f"{RAW_FOLDER}/{filename}"
    dest_key =f"{PROCESS_FOLDER}/{filename}"   

    s3.copy_object(
        Bucket=con.BUCKET_NAME,
        CopySource={"Bucket": con.BUCKET_NAME,"Key": source_key},
        Key=dest_key
    )
    logging.info(f"Copie RAW vers PROCESSED: {filename}")
    print(f"Copie RAW vers PROCESSED: {filename}")
def download_from_process(filename):
    """Downloads a file from the processed folder to a temporary local directory.
    Params:
        filename (str): Name of the file located in the processed folder.
    Returns:
        str: Local path of the downloaded file in the temporary directory.
    """
    s3_key = f"{PROCESS_FOLDER}/{filename}"
    local_path=f"/tmp/{filename}"
    s3.download_file(con.BUCKET_NAME,s3_key,local_path)
    return local_path
def upload_to_output(local_path):
    """Uploads a local file to the output folder in S3.
    Params:
        local_path (str): Local path of the file to be uploaded.
    Returns:
        None
    """
    filename=os.path.basename(local_path)
    s3_key=f"{OUTPUT_FOLDER}/{filename}"
    s3.upload_file(local_path,con.BUCKET_NAME,s3_key)

logging.info("copie des fichiers de raw vers process")
print("copie des fichiers de raw vers process")
for file in MES_FILES.values():
    copy_raw_to_process(file)
def processing_resultat():
    """
    Executes the geospatial processing pipeline for palm tree analysis.

    This function:
    - Downloads required GeoJSON files from the processed S3 folder
      (palms, roads, and cultivation zones)
    - Loads and reprojects all datasets to a metric CRS
    - Computes the distance between each palm tree and the nearest road
    - Exports the palm distance result to the S3 output folder
    - Calculates palm tree density per cultivation zone
    - Exports the density results as a CSV file

    Returns:
        str: Local path of the generated CSV file containing palm tree
             density per zone (number of palms, surface area in km²,
             and density per km²).
    """
    palmiers_path=download_from_process("basedadaptationgeneralemutwangamangina.geojson")
    routes_path=download_from_process("routes.geojson")
    zone_path=download_from_process("Zoneculture.geojson")
    palmiers=gpd.read_file(palmiers_path)
    routes = gpd.read_file(routes_path)
    zones =gpd.read_file(zone_path)
    logging.info("Fichiers charges avec success")
    print("Fichiers charges avec success")
    palmiers=palmiers.to_crs(CRS_METRIQUE)
    routes=routes.to_crs(CRS_METRIQUE)
    zones=zones.to_crs(CRS_METRIQUE)
    logging.info("Reprojection terminee")
    print("Reprojection terminee")
     # palmiers["distance_route_km"]=(palmiers.geometry.distance(routes,align=True))/1000
    # #  print(palmiers.columns)
    # palmiers["distance_route_km"] = (palmiers.geometry.apply(lambda geom: routes.distance(geom).min()) / 1000)
    # ---- distance palmier vers route la plus proche et le  type de route ----
    palmiers = gpd.sjoin_nearest(
        palmiers,
        routes[['highway', 'geometry']], 
        how="left",
        distance_col="distance_route_m"
    )
    palmiers["distance_route_km"] = palmiers["distance_route_m"] / 1000
    palmiers.rename(columns={"highway": "type_de_route"}, inplace=True)
    print("========IMPRESSION DE TOP 10 DE PALMIERS AVEC LA DISTANCE ET TYPE DE ROUTE==============")
    tableau = palmiers[["culture", "distance_route_km", "type_de_route"]].head(10).reset_index()
    print(tabulate(
        tableau,
        headers=["Palmier_ID", "Culture", "Distance à la route (km)", "Type de route"],
        tablefmt="grid",
        floatfmt=".3f"
    ))
    palmiers_result = "/tmp/palmiers_distance.geojson"
    # Supprimer le fichier s'il existe
    if os.path.exists(palmiers_result):
        os.remove(palmiers_result)
    palmiers.to_file(palmiers_result, driver="GeoJSON")
    upload_to_output(palmiers_result)
    # densite de palmiers par zone
    if "index_right" in zones.columns:
        zones = zones.rename(columns={"index_right": "zones_index_backup"})
    if "index_right" in palmiers.columns:
        palmiers = palmiers.rename(columns={"index_right": "palmiers_index_backup"})
    # S'assurer que l'index n'a pas de nom
    zones.index.name = None
    palmiers.index.name = None
    palmiers_zone = gpd.sjoin(palmiers, zones, predicate="within")
    densite = (
    palmiers_zone
    .groupby("index_right")
    .size()
    .reset_index(name="nb_palmiers")
    )
    zones["surface_km2"] = zones.geometry.area / 1_000_000
    zones = zones.merge(densite, left_index=True, right_on="index_right", how="left")
    zones["nb_palmiers"] = zones["nb_palmiers"].fillna(0)
    zones["densite_palmiers_km2"] = zones["nb_palmiers"] / zones["surface_km2"]

    resultat = zones[[
        "Designation",
        "nb_palmiers",
        "surface_km2",
        "densite_palmiers_km2"
    ]]

    print(
        tabulate(
            resultat,
            headers="keys",
            tablefmt="grid",
            floatfmt=".2f"
        )
    )
    densite_result="/tmp/densite_palmiers.csv"
    zones[["nb_palmiers", "surface_km2", "densite_palmiers_km2"]].to_csv(
        densite_result,
        index=False
    )
    return densite_result
upload_to_output(processing_resultat())
# charger le logs sur Ec2
upload_to_output(LOG_FILE)
logging.info("===== Fin de traitement=====")
print("===== Fin de traitement=====")