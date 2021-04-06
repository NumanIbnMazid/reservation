from skytrip.ticket_issue.issue_handler import IssueHandler
import json
from tester_helper import get_token, manage_book_info_json

true = True
false = False

json_dir = "Req_Res_Samples/responses/sabre/reservation_structured_response_sabre.json"

response_data = None

with open(json_dir) as f:
  response_data = json.load(f)

# Specify itinerary
root_node = response_data["body"]["responseData"].get("CreatePassengerNameRecordRS", {})

response_status = root_node["ApplicationResults"].get("status", "")
if response_status == "Complete":
    target_itinerary_id = root_node["ItineraryRef"].get("ID", "")
else:
    target_itinerary_id = None


data = {
    "ExistedToken": get_token(),
    "RequestBody": {
        "ItineraryID": target_itinerary_id
    }
}

event_body = data


def moduleRunner(testWithWhile=False, runAmount=7):
    """
    moduleRunner() => Skytrip Module Runner Function.
    params: testWithWhile (Boolean, default=False), runAmount (integer, default=7)
    """
    if testWithWhile == True:
        i = 0
        while i <= runAmount:
            modulehandler = IssueHandler(EventBodyData=event_body)
            response = modulehandler.sabre_issue_handler(
                generateJSON=True)
            print(f"\n {'*' * 50} Issue Response Data {'*' * 50} : \n\n",
                  response, "\n\n")
            i += 1
    else:
        modulehandler = IssueHandler(EventBodyData=event_body)
        response = modulehandler.sabre_issue_handler(generateJSON=True)
        print(f"\n {'*' * 50} Issue Response Data {'*' * 50} : \n\n",
              response, "\n\n")
    # return the response
    return response


# get actual response
response = moduleRunner(testWithWhile=False, runAmount=5)

# Update Book Info JSON File
if response["body"]["responseData"]["AirTicketRS"]["ApplicationResults"].get("status", None) == "Complete":
    # manage Book Info JSON
    manage_book_info_json(
        pnr_ID=response["body"]["responseData"]["AirTicketRS"]["Summary"][0]["Reservation"].get("content", None),
        response=response,
        info_node_name="ENHANCED AIR TICKET INFO",
        detail_node_name="ENHANCED AIR TICKET DETAIL",
    )
