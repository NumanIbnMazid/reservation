# import necessary libraries and modules
from skytrip_config.gds_config import SabreConfig
from skytrip.ticket_search.search_config import SearchConfig
from skytrip.utils.common import SkyTripCommon
from skytrip.utils.helper import get_exception_message
import inspect


# Sabre Search Prefs Class
class SabreSearchPrefs:
    seats_requested = 0
    __sabre_conf = SabreConfig()
    __search_conf = SearchConfig()
    __skytrip_common = SkyTripCommon()

    def calculate_and_set_SeatsRequested(self, passengerObj):
        """
        calculate_SeatsRequested() => calculates total seats requested based on passenger type quantity.
        params => obj (passenger type quantity object)
        """
        if passengerObj.get("Code", "") in self.__skytrip_common.available_passenger_types:
            if passengerObj.get("Code", "") not in self.__search_conf.passenger_types_to_skip_count:
                self.seats_requested += int(passengerObj.get("Quantity", "0"))
        else:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2], 
                    msg=f"Invalid Passenger Type Code given: {passengerObj.get('Code', None)}! Available passenger type codes that configured in Skytrip are: {self.__skytrip_common.available_passenger_types}"
                )
            )

    # search preference function
    def get_search_preference(self, RequestBody={}):
        """
        Generate search preferences (request body) based on user inputs
        Param: (RequestBody*) => containing user input values and existed token.
        """
        # define base structure of search data
        request_structure = self.__search_conf.get_search_request_structure()

        try:

            # ------- get all the fields from request body -------
            TicketClass = {}
            if RequestBody.get("TicketClass", "") != "":
                TicketClass = {
                    "CabinPref": {
                        "Cabin": RequestBody["TicketClass"]
                    }
                }

            # ------ prepare search data ------
            insert_node = request_structure["OTA_AirLowFareSearchRQ"]
            # ------ configure pseudo city code ------
            insert_node["POS"]["Source"][0]["PseudoCityCode"] = self.__sabre_conf.get_PCC()
            # ------ configure company name ------
            insert_node["POS"]["Source"][0]["RequestorID"]["CompanyName"]["Code"] = self.__search_conf.requestor_id_company_code
            # prepare origin and destination information
            OriginDestinationInformation = RequestBody.get("OriginDestinationInformation", [])
            # loop through origin destination information and insert in node
            for element in OriginDestinationInformation:
                if TicketClass:
                    element["TPA_Extensions"] = TicketClass
                # insert information in search data
                insert_node["OriginDestinationInformation"].append(element)
            # prepare passenger information data
            PassengerTypeQuantity = RequestBody.get("PassengerTypeQuantity", [])
            # loop through PassengerTypeQuantity and insert in node
            for element in PassengerTypeQuantity:
                self.calculate_and_set_SeatsRequested(passengerObj=element)
                insert_node["TravelerInfoSummary"]["AirTravelerAvail"][0]["PassengerTypeQuantity"].append(element)
            # Insert Seats Requested
            insert_node["TravelerInfoSummary"]["SeatsRequested"].append(self.seats_requested)
            # prepare flight type information data
            if RequestBody.get("DirectFlightsOnly", "") != "":
                insert_node["DirectFlightsOnly"] = RequestBody.get("DirectFlightsOnly", False)
            if RequestBody.get("AvailableFlightsOnly", "") != "":
                insert_node["AvailableFlightsOnly"] = RequestBody.get("AvailableFlightsOnly", False)
            
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to generate search preference!"
                )
            )

        # return the final prepared search data
        return request_structure
