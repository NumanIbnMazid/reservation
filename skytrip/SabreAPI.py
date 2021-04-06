# import necessary modules and libraries
import time
import requests
import types
import re
import warnings
import json
from abc import ABC, abstractmethod
from skytrip_config.gds_config import SabreConfig


# SabreBone Abstract Class for Sabre
class SabreBone(ABC):
    # Abstract method for get token
    @abstractmethod
    def get_token(self):
        """
        Method used to retrieve token required for making reequest to the API endpoint.
        """
        pass
    
    # Abstract method for call method
    @abstractmethod
    def call_method(self):
        """
        Method used to synchronize the necessary request parameters (hearders, body etc.) and make request to the endpoint based on the request type.
        """
        pass


# Sabre Class
class Sabre(SabreBone, object):
    # class variables
    # inital token => None
    token = None
    # initial request params
    __request_params = ""
    # SabreConfig class (containing sabre credentials) instance to access the sabre credentials
    __sabre_conf = SabreConfig()
    # get sabre server
    server = __sabre_conf.get_server()
    # Define the necessary API endpoints
    APIs = __sabre_conf.get_APIs()

    # constructor (initialization method) for the Sabre class
    def __init__(self, ExistedToken=None, RequestBody=None):
        # instance variables
        self.ExistedToken = ExistedToken
        self.RequestBody = RequestBody

        # Container class
        class Container(object):
            def __call__(self, *args, **kwargs):
                return self._call(self.endpoint, *args, **kwargs)

        # Container class instance
        self.api = Container()

        for api_name, (method, endpoint, description) in self.APIs.items():
            parts = api_name.split('.')
            obj = self.api
            for part in parts:
                if getattr(obj, part, None) is None:
                    setattr(obj, part, Container())
                obj = getattr(obj, part)
            
            def fn(s, endpoint, *args, **kwargs):
                e = endpoint
                if '{' in endpoint:
                    e = endpoint.format(**kwargs)
                    for arg in re.findall(r'{(\w+)}', endpoint):
                        del kwargs[arg]

                if method == 'GET':
                    kwargs = {"params": kwargs}
                else:
                    kwargs = {"data": kwargs}
                if self.__request_params != "":
                    e = e + self.__request_params
                
                # print("\n sabreAPI.py => Line: 89, (e) : \n", e)
                
                result = self.call_method(
                    method.lower(), self.server + e, *args, **kwargs)
                assert result.status_code == 200, u"Got a {} (eou are not authxpecting 200): {}".format(
                    result.status_code, result.json())
                return result.json()

            obj.endpoint = endpoint
            obj._call = types.MethodType(fn, Container)  # , Container

    # setter method for request params
    def set_request_params(self, params):
        """
        Set request query parameters.
        Params: (*params => String)
        """
        self.__request_params = params

    # Check validity of token
    def is_valid(self):
        """
        Check validity of token against expire date
        """
        self.last_check = time.time()
        if self.token is not None and self.token != "" and self.token['expires'] < self.last_check:
            return True
        return False

    # Get token
    def get_token(self):
        """
        Get authorization bearer token.
        """
        if self.is_valid():
            return self.token
        else:
            self.token = self.ExistedToken
        # print("\n sabreAPI.py => Line: 110, Token Value : \n", self.token)

        return self.token

    # Call the API
    def call_method(self, method, *args, **kwargs):
        """
        Call the API with potential parameters
        - Headers => Authorization(Token), Content-Type
        - data => body
        """
        if kwargs is None:
            kwargs = {}
        # get the headers
        kwargs['headers'] = kwargs.get('headers', {})
        # update and prepare request headers and body
        kwargs['headers'].update(
            Authorization='Bearer ' + self.get_token()[u'access_token']
        )
        kwargs['headers']['accept'] = 'application/json'
        kwargs['headers']['Content-Type'] = 'application/json'
        # print("\n sabreAPI.py => Line: 131, Search Data : \n", self.RequestBody)
        kwargs['data'] = json.dumps(self.RequestBody)
        # print("\n sabreAPI.py => Line: 150, Kwargs : \n", kwargs)
        # print("\n sabreAPI.py => Line: 151, kwargs['data'] : \n", kwargs['data'])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return getattr(requests, method)(*args, **kwargs)

    # Get method
    def get(self, *args, **kwargs):
        """
        Synchronize Get method with the call method
        """
        return self.call_method('get', *args, **kwargs)

    # Post method
    def post(self, *args, **kwargs):
        """
        Synchronize Post method with the call method
        """
        return self.call_method('post', *args, **kwargs)

    # API list
    def api_list(self):
        for api_name, (method, endpoint, description) in self.APIs.items():
            print("\n sabreAPI.py => Line: 165, api_list : \n", )
            print(u"{}: {} (endpoint: {} {})".format(
                api_name, description, method, endpoint))
