# import the necessary modules and libraries
from skytrip_config.gds_config import SabreConfig
import base64
import time
import warnings
import requests


# Sabre Token Class
class SabreToken():
    # class variables
    __token = None
    # Sabre configuration class's instance
    __sabre_conf = SabreConfig()
    # Get Client ID, Client Secret and Server
    __client_id = __sabre_conf.get_client_id()
    __client_secret = __sabre_conf.get_client_secret()
    __server = __sabre_conf.get_server()
    # auth URL
    auth_URL = '/v2/auth/token'

    # Sabre token class constructor
    def __init__(self):
        super(SabreToken, self).__init__()

    # Encode client credentials
    def encode_credentials(self):
        """
        Encode client credentials (Client ID, Client Secret)
        """
        encoded_credentials = base64.b64encode(base64.b64encode(
            self.__client_id) + ":".encode() + base64.b64encode(self.__client_secret))
        # print("\n sabreAPI.py => Line: 117, Encoded Credentials : \n", encoded_credentials)
        return encoded_credentials

    # def is_valid(self):
    #     """
    #     Check validity of token against expire date
    #     """
    #     self.last_check = time.time()
    #     if self.__token is not None and self.__token != "" and self.__token['expires'] < self.last_check:
    #         return True
    #     return False

    # Get token
    def get_token(self):
        """
        Get authorization bearer token.
        """
        __encoded_credentials = self.encode_credentials()
        headers = {
            'Authorization': 'Basic ' + __encoded_credentials.decode(),
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            'grant_type': 'client_credentials',
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = requests.post(self.__server + self.auth_URL, headers=headers, data=params)
            # print("\n sabreAPI.py => Line: 98, JSON Data : \n", r.json())
            # print("\n sabreAPI.py => Line: 99, Status Code : \n", r.status_code)
        assert r.status_code == 200, 'Expecting 200 answer, got {} instead. [{}]'.format(r.status_code, r.json())
        self.__token = r.json()
        # assign expires information
        self.__token['expires'] = time.time() + self.__token['expires_in']

        # print("\n sabreAPI.py => Line: 110, Token Value : \n", self.__token)

        # return the token
        return self.__token
