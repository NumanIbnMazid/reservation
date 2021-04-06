# import necessary modules and libraries
from skytrip.SabreAPI import Sabre
from abc import ABC, abstractmethod
from skytrip.utils.helper import get_exception_message, generate_json
import inspect
from copy import deepcopy

# Module handler Abstract Class
class ModuleHandlerBone(ABC):
    # Abstract method for get token
    @abstractmethod
    def get_target_files_for_json_sample(self):
        """
        Method used to get target files to generate JSON samples.
        """
        pass


# handler class
class SabreHandler:
    status_code = 400

    module_map_list = [
        {
            "EndpointIdentifier": "v1.offers.shop", "SabreModuleName": "BargainFinderMax", "SkytripModuleName": "search", "ResponseValidator": None
        },
        {
            "EndpointIdentifier": "v6.shop.flights.revalidate", "SabreModuleName": "RevalidateItinerary", "SkytripModuleName": "revalidate", "ResponseValidator": None
        },
        {
            "EndpointIdentifier": "v2.passenger.records", "SabreModuleName": "CreatePassengerNameRecord", "SkytripModuleName": "reservation", "ResponseValidator": "['CreatePassengerNameRecordRS']['ApplicationResults'].get('status', None) == 'Complete'"
        },
        {
            "EndpointIdentifier": "v1.air.ticket", "SabreModuleName": "EnhancedAirTicket", "SkytripModuleName": "issue", "ResponseValidator": "['AirTicketRS']['ApplicationResults'].get('status', None) == 'Complete'"
        },
    ]

    def call_API(self, sabre_instance=None, endpoint_identifier=None):
        print(
            f"\n *** '{__file__.split('/')[-2]}/{__file__.split('/')[-1]}' ===> {inspect.stack()[0][3]}() ***"
        )
        pass

    def __call_sabre(self, sabre_instance=None, endpoint_identifier=None):
        """
        __call_sabre() => Calls Sabre class for getting response.
        params => sabre_instance (Sabre Class Instance)
        return => object/string
        """
        # define main sabre response placeholder
        sabre_response = None

        try:
            # Ticket Search (Bargain Finder Max - BFM)
            if endpoint_identifier == 'v1.offers.shop':
                sabre_response = sabre_instance.api.v1.offers.shop()
                # update status code
                if type(sabre_response) == dict:
                    self.status_code = 200

            # Itinerary Revalidate (Revalidate Itinerary)
            elif endpoint_identifier == 'v6.shop.flights.revalidate':
                sabre_response = sabre_instance.api.v6.shop.flights.revalidate()
                # update status code
                if type(sabre_response) == dict:
                    self.status_code = 200

            # Ticket Reservation (Create Passenger Name Record - PNR)
            elif endpoint_identifier == 'v2.passenger.records':
                sabre_instance.set_request_params("?mode=create")
                sabre_response = sabre_instance.api.v2.passenger.records()
                # update status code
                if type(sabre_response) == dict and sabre_response["CreatePassengerNameRecordRS"]["ApplicationResults"].get("status", None) == "Complete":
                    self.status_code = 200

            # Issue Air Ticket (Enhanced Air Ticket)
            elif endpoint_identifier == 'v1.air.ticket':
                sabre_response = sabre_instance.api.v1.air.ticket()
                # update status code
                if type(sabre_response) == dict and sabre_response["AirTicketRS"]["ApplicationResults"].get("status", None) == "Complete":
                    self.status_code = 200

            else:
                sabre_response = "Invalid Endpoint Identifier!"


        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to call Sabre!"
                )
            )

        # return main response
        return sabre_response

    def format_request(self, EventBodyData=None, request_pref_func=None):
        """
        format_request() => Formats requests for Sabre.
        params => EventBodyData (object), request_pref_func (func_name)
        return => object
        """
        # define initial formatted request
        formatted_req = {}
        try:
            RequestBodyCopy = deepcopy(EventBodyData)
            request_body = RequestBodyCopy.get("RequestBody", {})
            # initialize data list
            data_list = [request_body]
            # map function to synchronize and generate request parameters
            for index, pref_result in enumerate(map(request_pref_func, data_list)):
                if index == 0:
                    formatted_req = pref_result
                    break

        # handle exceptions
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to format request body!"
                )
            )

        return formatted_req

    def get_sabre_response(self, EventBodyData=None, request_pref_func=None, endpoint_identifier=None, generateJSON=False):
        """
        get_sabre_response() => Gets Response from Sabre Server.
        params => EventBodyData (object), request_pref_func (func_name), endpoint_identifier (string)
        return => object
        """
        # define main response placeholder
        result = None
        formatted_request = None
        try:
            # ------------------- *** format request body *** -------------------
            formatted_request = self.format_request(EventBodyData=EventBodyData, request_pref_func=request_pref_func)

            # ------------------- *** generate JSON file of formatted request body *** -------------------
            if generateJSON == True:
                for module_map in self.module_map_list:
                    if endpoint_identifier == module_map.get("EndpointIdentifier", None):
                        generate_json(
                            gds="sabre", isReq=True, filename=f"{module_map.get('SkytripModuleName', '').lower()}_request_sabre.json", data=formatted_request
                        )
                        break

            # ------------------- *** get main response by calling sabre API *** -------------------
            # ------------------- *** Manage Token *** -------------------
            existed_token = {}
            try:
                existed_token = EventBodyData.get("ExistedToken", {})
            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=f"Invalid Token! Token: {existed_token}"
                    )
                )
            # Create Sabre() class instance
            sabre = Sabre(ExistedToken=existed_token, RequestBody=formatted_request)
            # call sabre and get response
            response = self.__call_sabre(sabre_instance=sabre, endpoint_identifier=endpoint_identifier)

            # ------------------- *** generate JSON File of Sabre raw response *** -------------------
            if generateJSON == True:
                for module_map in self.module_map_list:
                    if endpoint_identifier == module_map.get("EndpointIdentifier", None):
                        generate_json(
                            gds="sabre", isReq=False, filename=f"{module_map.get('SkytripModuleName', '').lower()}_original_response_sabre.json", data=response
                        )
                        break
                
            # ------------------- *** preapare result *** -------------------
            result = {
                "token": sabre.token,
                "responseData": response
            }
        
            # ------------------- *** return statement *** -------------------
            if EventBodyData.get("RequestLOG", None) == True:
                return {
                    'statusCode': self.status_code,
                    'body': result,
                    "RequestLOG": {
                        "logStartHighlighter": "***-!-!-!-!-!-!S!-!-!T!-!-!A!-!-!R!-!-!T!-!-!-!-!-!-***",
                        "formattedRequest": formatted_request,
                        "requestBody": EventBodyData,
                        "logEndHighlighter": "***-!-!-!-!-!-!E!-!-!N!-!-!D!-!-!-!-!-!-***"
                    }
                }
                
            return {
                'statusCode': self.status_code,
                'body': result
            }

        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to get response from Sabre!"
                )
            )
