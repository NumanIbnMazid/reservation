# import necessary modules and libraries
from skytrip.ticket_reservation.sabre_reservation_prefs import SabreReservationPrefs
from skytrip.gds_handler import SabreHandler
from skytrip.ticket_reservation.reservation_validator import validate_reservation_request
from skytrip.utils.helper import generate_json, get_root_exception_message, finalize_response
import inspect
from skytrip.ticket_reservation.db_handler import DBhandler
# remove JSON
import json # remove JSON Dependency after removing fake finalized response


#  Reservation handler Class
class ReservationHandler:
    # create sabre handler instance
    __sabre_handler = SabreHandler()

    def __init__(self, EventBodyData=None):
        self.event_body_data = EventBodyData

    # handler function
    def sabre_reservation_handler(self, generateJSON=False):
        """
        sabre_reservation_handler for PNR (Passenger Name Record) Module
        params => generateJSON (boolean)
        return => object
        """
        # define actual result placeholder
        result = None
        try:
            # ------------------- *** validate request body *** -------------------
            validated_request_body = validate_reservation_request(
                EventBodyData=self.event_body_data
            )

            # ------------------- *** get main response from Sabre *** -------------------
            # sabre reservation prefs
            __sabre_reservation_prefs = SabreReservationPrefs()
            # get result and assign to result variable
            result = self.__sabre_handler.get_sabre_response(
                EventBodyData=validated_request_body, request_pref_func=__sabre_reservation_prefs.get_reservation_preference, endpoint_identifier='v2.passenger.records', generateJSON=generateJSON
            )

            # ------------------- *** validate structure and finalize response *** -------------------
            finalized_response = finalize_response(response=result)

            # ------------------- *** insert PNR data into Database *** -------------------
            # FAKE RESPONSE
            # reservation_structured_JSON = "UTILS/REQ-RES-SAMPLE-STORE/responses/sabre/reservation_structured_response_sabre.json"
            # with open(reservation_structured_JSON) as f:
            #     finalized_response = json.load(f)

            if finalized_response.get("statusCode", None) == 200 and finalized_response["body"]["responseData"]["CreatePassengerNameRecordRS"]["ApplicationResults"].get("status", None) == "Complete":
                db_handler = DBhandler()
                db_pnr_id = db_handler.insert_data(
                    request=validated_request_body,
                    response=finalized_response
                )
                # insert DBpnrID in finalized response
                finalized_response["body"]["responseData"]["DBpnrID"] = db_pnr_id

            # ------------------- *** generate JSON file of Skytrip structured response *** -------------------
            if generateJSON == True:
                generate_json(
                    gds="sabre", isReq=False, filename="reservation_structured_response_sabre.json", data=finalized_response
                )

            # return finalized response
            return finalized_response

        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            # assign exceptions to result
            return get_root_exception_message(
                Ex=E, gdsResponse=result, appResponse=None, file=__file__,
                parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to reserve itinerary!"
            )
