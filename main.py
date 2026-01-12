import boto3
import os
import logging
import json

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
        ma_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyDeleteForOthers",
                "Effect": "Deny",
                "Principal": "*",
                "Action": [
                     "s3:DeleteObject",
                    "s3:DeleteObjectVersion"
                ],
                "Resource": f"arn:aws:s3:::{BUCKET_NAME}/raw/*",
                "Condition": {
                "ArnNotLike": {
                     "aws:PrincipalArn": "arn:aws:sts::341395375209:assumed-role/AWSReservedSSO_PowerUserAccess_e336dee556ef96ac/*"
                }
            }
            },
         
        ]
    }
 # Create a bucket policy
        # Appliquer la policy sur le bucket
        response = s3.put_bucket_policy(
            Bucket=BUCKET_NAME,           
            Policy=json.dumps(ma_policy) 
        )
        # activation de la policy
        # s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=bucket_policy)
        # bucket_policy = json.dumps(bucket_policy)
        logging.info(response)
    except s3.exceptions.BucketAlreadyExists as e:
        logging.warning(f"Error: {e.response['Error']['Code']}")
    # except s3.exceptions.BucketAlreadyOwnedByYou:
    #     logging.warning("bucket"+ BUCKET_NAME + "est deja cree")

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