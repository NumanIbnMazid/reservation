# import necessary modules and libraries
from skytrip.ticket_issue.sabre_ticket_issue_prefs import SabreTicketIssuePrefs
from skytrip.gds_handler import SabreHandler
from skytrip.utils.helper import generate_json, get_root_exception_message, finalize_response
import inspect
from skytrip.ticket_issue.db_handler import DBhandler
# remove JSON
import json  # remove JSON Dependency after removing fake finalized response


#  Reservation handler Class
class IssueHandler:
    # create sabre handler instance
    __sabre_handler = SabreHandler()
    # sabre ticket prefs
    __sabre_ticket_issue_prefs = SabreTicketIssuePrefs()

    def __init__(self, EventBodyData=None):
        self.event_body_data = EventBodyData

    # handler function
    def sabre_issue_handler(self, generateJSON=False):
        """
        sabre_issue_handler() => For Enhanced Air Ticket Module of Sabre
        params => generateJSON (boolean)
        return => object
        """
        # define main result placeholder
        result = None
        try:
            # ------------------- *** get main response from Sabre *** -------------------
            # get result
            result = self.__sabre_handler.get_sabre_response(
                EventBodyData=self.event_body_data, request_pref_func=self.__sabre_ticket_issue_prefs.get_ticket_issue_preference, endpoint_identifier='v1.air.ticket', generateJSON=generateJSON
            )

            # ------------------- *** validate structure and finalize response *** -------------------
            finalized_response = finalize_response(response=result)

            # ------------------- *** insert Issued Ticket data into Database *** -------------------
            # FAKE RESPONSE
            # reservation_structured_JSON = "UTILS/REQ-RES-SAMPLE-STORE/responses/sabre/ticket_issue_structured_response_sabre.json"
            # with open(reservation_structured_JSON) as f:
            #     finalized_response = json.load(f)

            if finalized_response.get("statusCode", None) == 200 and finalized_response["body"]["responseData"]["AirTicketRS"]["ApplicationResults"].get("status", None) == "Complete":
                db_handler = DBhandler()
                db_issued_ticket_id = db_handler.insert_data(
                    request=self.event_body_data,
                    response=finalized_response
                )
                # insert DBpnrID in finalized response
                finalized_response["body"]["responseData"]["DBissuedTicketID"] = db_issued_ticket_id

            # ------------------- *** generate JSON file of Skytrip structured response *** -------------------
            if generateJSON == True:
                generate_json(
                    gds="sabre", isReq=False, filename="issue_structured_response_sabre.json", data=finalized_response
                )

            # return finalized response
            return finalized_response

        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            # assign exceptions to result
            result = get_root_exception_message(
                Ex=E, gdsResponse=result, appResponse=None, file=__file__,
                parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to issue air ticket!"
            )
