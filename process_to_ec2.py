import boto3
import geopandas as gpd
from pathlib import Path
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
LOG_DIR ="/tmp/logs"
os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(
    filename=f"{LOG_DIR}/execution.log",
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
    
