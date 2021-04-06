# import necessary libraries and modules
from skytrip_config.config import SkyTripConfig

# Sabre Configuration Class
class SabreConfig:
    # ------- demo account info -------
    __use_demo = False
    __demo_client_id = b"example"
    __demo_cert_secret = b"example"
    # ------- client id -------
    __client_id = b"example"
    # ------- secret for production environment -------
    __prod_secret = b"example"
    # ------- secret for certification environment -------
    __cert_secret = b"example"
    # ------- server for production environment -------
    __prod_server = "https://example.com"
    # ------- server for certification environment -------
    __cert_server = "https://example.com"
    # APIs Object
    __APIs_obj = {
        'v1.offers.shop': ('POST', '/v1/offers/shop', 'Bargain Finder Max API'),
        # Revalidate Itinerary
        'v6.shop.flights.revalidate': ('POST', '/v6.1.0/shop/flights/revalidate', 'Revalidate Itinerary API'),
        # Create PNR (Passenger Name Record)
        'v2.passenger.records': ('POST', '/v2.3.0/passenger/records', 'Passenger Name Record API'),
        # Issue Air Ticket
        'v1.air.ticket': ('POST', '/v1.2.1/air/ticket', 'Enhanced Air Ticket API'),
    }

    # SkyTrip Config Instance
    __skytrip_conf = SkyTripConfig()

    # get PCC
    def get_PCC(self):
        """
        Getter method for getting PCC.
        return => string
        """
        client_id = self.get_client_id().decode()
        splitted_client_id = client_id.split(":")
        return splitted_client_id[2]

    # get client id
    def get_client_id(self):
        """
        Getter method for getting client id.
        return => string
        """
        if self.__use_demo == True and self.__skytrip_conf.get_is_production() == False:
            # return client id
            return self.__demo_client_id
        else:
            return self.__client_id

    # get client secret
    def get_client_secret(self):
        """
        Getter method for getting client secret based on environment.
        return => string
        """
        if self.__skytrip_conf.get_is_production() == True:
            return self.__prod_secret
        else:
            if self.__use_demo == True:
                return self.__demo_cert_secret
            else:
                return self.__cert_secret

    # get server
    def get_server(self):
        """
        Getter method for getting server based on environment.
        return => string
        """
        # ------- server for production environment -------
        if self.__skytrip_conf.get_is_production() == True:
            return self.__prod_server
        # ------- server for certification environment -------
        else:
            return self.__cert_server

    def get_APIs(self):
        APIs = self.__APIs_obj
        return APIs
