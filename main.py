import os
import logging
from maclassetest import Maclasse

logging.basicConfig(level=logging.INFO)
con=Maclasse()
s3=con.connexion_s3()

FOLDERS =["raw/","processed/","validated/"]
# dossier des me fichier
LOCAL_DIR = "data"

# DECLARATIONS DES MES FONCTIONS
def creation_bucket():
    # creation de notre bucket et nous allons activer le versionnage
    try:
        s3.create_bucket(Bucket=con.BUCKET_NAME)
        logging.info("bucket"+ con.BUCKET_NAME+ " est creer avec success")
        s3.put_bucket_versioning(
            Bucket=con.BUCKET_NAME,
            VersioningConfiguration={"Status": "Enabled"}
        )
        logging.info("versionning active")
         # Create a bucket policy
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
                "Resource": f"arn:aws:s3:::{con.BUCKET_NAME}/raw/*",
                "Condition": {
                "ArnNotLike": {
                     "aws:PrincipalArn": "arn:aws:sts::341395375209:assumed-role/AWSReservedSSO_PowerUserAccess_e336dee556ef96ac/*"
                }
            }
            },
         
        ]
    }
        # Appliquer la policy sur le bucket
        # response = s3.put_bucket_policy(
        #     Bucket=BUCKET_NAME,           
        #     Policy=json.dumps(ma_policy) 
        # )
        # logging.info(response)
    except s3.exceptions.BucketAlreadyExists as e:
        logging.warning(f"Error: {e.response['Error']['Code']}")
    # except s3.exceptions.BucketAlreadyOwnedByYou:
    #     logging.warning("bucket"+ BUCKET_NAME + "est deja cree")

def upload_fichier():
    # création des dossiers S3
    for folder in FOLDERS:
        s3.put_object(Bucket=con.BUCKET_NAME, Key=folder)
    logging.info("dossiers créés ")
    # upload de mes fichiers sur mon bucket
    for filename in os.listdir(LOCAL_DIR):
        local_file = os.path.join(LOCAL_DIR, filename)
        if os.path.isfile(local_file):
            s3_key = f"raw/{filename}"
            s3.upload_file(local_file, con.BUCKET_NAME, s3_key)
            logging.info("fichier uploadé : s3://" + con.BUCKET_NAME+ "/"+s3_key)

# APPEL DES MES FONCTIONS
creation_bucket()
upload_fichier()