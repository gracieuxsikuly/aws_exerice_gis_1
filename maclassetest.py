import boto3
class Maclasse:
    #configuration de notre compte aws
    AWS_PROFIL="default"
    AWS_REGION = "us-east-1"
    BUCKET_NAME ="mbau-gracier"
    # BUCKET_NAME ="mbau-gracieux-prive"
    def connexion_s3(self):
        #session aws pour connexion
        session=boto3.Session(profile_name=self.AWS_PROFIL,region_name=self.AWS_REGION)
        return session.client('s3')