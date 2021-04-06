

class UserMediaConfig:
    # ------- S3 User AWS Credential -------
    __USER = "s3access"
    __ACCESS_KEY = "CdAhbNeu6fpLh4CdHySn1zlWf93FWHuwIorceUeq"
    __SECRET_KEY = "AKIAUEU2BDSTRSO5PYWX"
    # ------- Bucket Information -------
    bucket_name = "skytripb2cmedia"
    bucket_url = "s3://skytripb2cmedia/"

    def get_s3_user(self):
        """
        get_s3_user => Getter method for getting S3 Username
        return => string
        """
        return self.__USER

    def get_s3_access_key(self):
        """
        get_s3_access_key => Getter method for getting S3 Access Key
        return => string
        """
        return self.__ACCESS_KEY

    def get_s3_secret_key(self):
        """
        get_s3_user => Getter method for getting S3 Secret Key
        return => string
        """
        return self.__SECRET_KEY
