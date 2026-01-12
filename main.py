import boto3
import os
import logging

logging.basicConfig(level=logging.INFO)

# configuration de notre compte aws
AWS_PROFIL= "default"
AWS_REGION= "us-east-1"
BUCKET_NAME ="mbau-gracier"
# BUCKET_NAME ="mbau-gracieux-prive"
FOLDERS =["raw/","processed/","validated/"]
# dossier des me fichier
LOCAL_DIR = "data"
# Session aws pour la connexion
session=boto3.Session(profile_name=AWS_PROFIL,region_name=AWS_REGION)
s3=session.client('s3')
# DECLARATIONS DES MES FONCTIONS
def creation_bucket():
    # creation de notre bucket et nous allons activer le versionnage
    try:
        s3.create_bucket(Bucket=BUCKET_NAME)
        logging.info("bucket"+ BUCKET_NAME+ " est creer avec success")
        s3.put_bucket_versioning(
            Bucket=BUCKET_NAME,
            VersioningConfiguration={"Status": "Enabled"}
        )
        logging.info("versionning active")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        logging.warning("bucket"+ BUCKET_NAME + "est deja cree")

def upload_fichier():
    # création des dossiers S3
    for folder in FOLDERS:
        s3.put_object(Bucket=BUCKET_NAME, Key=folder)
    logging.info("dossiers créés ")
    # upload de mes fichiers sur mon bucket
    for filename in os.listdir(LOCAL_DIR):
        local_file = os.path.join(LOCAL_DIR, filename)
        if os.path.isfile(local_file):
            s3_key = f"raw/{filename}"
            s3.upload_file(local_file, BUCKET_NAME, s3_key)
            logging.info("fichier uploadé : s3://" + BUCKET_NAME+ "/"+s3_key)
# APPEL DES MES FONCTIONS
creation_bucket()
upload_fichier()