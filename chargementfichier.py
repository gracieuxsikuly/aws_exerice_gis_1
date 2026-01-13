import logging
import json
from maclassetest import Maclasse

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
    file_content=response["Body"]
    jsonObject=json.loads(file_content.read())
    logging.info(jsonObject)
chargement_fichier()