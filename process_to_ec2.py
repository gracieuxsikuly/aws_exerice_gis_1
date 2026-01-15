import geopandas as gpd
from maclassetest import Maclasse
import os
import logging

con=Maclasse
s3=con.connexion_s3()
RAW_FOLDER ="raw"
PROCESS_FOLDER = "processed"
OUTPUT_FOLDER = "validated"
MES_FILES={
    "palmiers": "basedadaptationgeneralemutwangamangina.geojson",
    "routes" : "routes.geojsone",
    "zone" : "zones.geojson"
}
CRS_METRIQUE= "EPSG:32735"
LOG_DIR = "/tmp/logs"
LOG_FILE = f"{LOG_DIR}/execution.log"
os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(acstime)s-%(levelname)s-%(message)s"
)

logging.info("Demarage de notre scrypt")

def copy_raw_to_process(filename):
    """copier un fichier de mon dossier raw/ vers le dossier process/"""
    source_key=f"{RAW_FOLDER}/{filename}"
    dest_key =f"{PROCESS_FOLDER}/{filename}"   

    s3.copy_object(
        Bucket=con.BUCKET_NAME,
        CopySource={"Bucket": con.BUCKET_NAME,"Key": source_key},
        Key=dest_key
    )
    logging.info(f"Copie RAW vers PROCESSED: {filename}")
def download_from_process(filename):
    """telecharger le fichier depuis mon process vers un temp"""
    s3_key = f"{PROCESS_FOLDER}/{filename}"
    local_path=f"/tmp/{filename}"
    s3.download_file(con.BUCKET_NAME,s3_key,local_path)
    return local_path
def upload_to_output(local_path):
    """upload mon fichir local vers output"""
    filename=os.path.basename(local_path)
    s3_key=f"{OUTPUT_FOLDER}/{filename}"
    s3.upload_file(local_path,con.BUCKET_NAME,s3_key)

logging.info("copie des fichiers de raw vers process")
for file in MES_FILES:
    copy_raw_to_process(file)
palmiers_path=download_from_process("palmiers.geojson")
routes_path=download_from_process("routes.geojson")
zone_path=download_from_process("palmiers.geojson")
palmiers=gpd.read_file(palmiers_path)
routes = gpd.read_file(routes_path)
zones =gpd.read_file(zone_path)
logging.info("Fichiers charges avec success")
palmiers=palmiers.to_crs(CRS_METRIQUE)
routes=routes.to_crs(CRS_METRIQUE)
zones=zones.to_crs(CRS_METRIQUE)
logging.info("Reprojection terminee")
# """distance palmier route"""
palmiers["distance_route_m"]=palmiers.geometry.apply(
    lambda geom: routes.distance(geom).min()
)
palmiers_result = "/tmp/palmiers_distance.geojson"
palmiers.to_file(palmiers_result,driver="GEOJSON")
upload_to_output(palmiers_result)
# densite de palmiers par zone
palmiers_zone=gpd.sjoin(palmiers,zones,predicate="within")
densite=(
    palmiers_zone
    .groupby("index_right")
    .size()
    .reset_index(name="nb_palmiers")
)
zones["surface_km2"]= zones.geometry.area/1_000_000
zones = zones.merge(
    densite,
    left_index=True,
    right_on="index_right",
    how="left"
)
zones["nb_palmiers"]= zones["nb_palmiers"].fillna(0)
zones["densite_palmiers_km2"] =zones["nb_palmiers"]/zones["surface_km2"]
densite_result="/tmp/densite_palmiers.csv"
zones[["nb_palmiers","densite_palmiers_km2"]].to_csv(
    densite_result,
    index=False
)
upload_to_output(densite_result)
# charger le logs sur Ec2
upload_to_output(LOG_FILE)
logging.info("===== Fin de traitement=====")