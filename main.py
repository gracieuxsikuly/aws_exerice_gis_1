import boto3
import os
from io import BytesIO
import geopandas as gpd

# configuration de notre compte aws
AWS_PROFIL= "compteprive"
AWS_REGION= "us-east-1"
BUCKET_NAME ="s3-palmiers-projects"
FOLDERS =["raw/","processed/","validated/"]
# fichier a uploader sur s3
LOCAL_FILE= "data/AviationDB_V01.gpkg"
RAW_KEY= "raw/"+os.path.basename(LOCAL_FILE)
# Session aws pour la connexion
session=boto3.Session(profile_name=AWS_PROFIL,region_name=AWS_REGION)
s3=session.client('s3')
# creation de notre bucket et nous allons activer le versionnage
try:
    s3.create_bucket(Bucket=BUCKET_NAME)
    print(f"bucket{BUCKET_NAME} est creer avec success")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"bucket {BUCKET_NAME} est deja cree")
    s3.put_bucket_versioning(
        Bucket=BUCKET_NAME,
        VersioningConfiguration={'status':'enabled'}
    )
print('versionning active')
# on creer la structure des mes dossiers
for folder in FOLDERS:
    s3.put_object(Bucket=BUCKET_NAME,key=folder)
print(f"les dossiers creer: {FOLDERS}")
# upload des fichiers dans le dossier
if os.path.isfile(LOCAL_FILE):
    s3.upload_file(LOCAL_FILE,BUCKET_NAME,RAW_KEY)
    print(f'fichier uploader: s3//{BUCKET_NAME}/{RAW_KEY}')
else:
    print(f'fichier introuvable {LOCAL_FILE}')