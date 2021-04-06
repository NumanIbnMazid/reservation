from skytrip.revalidate_itinerary.revalidate_handler import RevalidateHandler
import json
import datetime
from dateutil.parser import parse
from tester_helper import get_token


true = True
false = False

# load req body util data
req_body_util_JSON = "UTILS/JSON_STORE/req-body-util.json"
req_body_util_data = None
with open(req_body_util_JSON) as f:
    req_body_util_data = json.load(f)

response_json_dir = "Req_Res_Samples/responses/sabre/search_structured_response_sabre.json"
request_json_dir = "Req_Res_Samples/requests/sabre/search_request_sabre.json"
final_json_file = "UTILS/JSON_STORE/revalidate-tester-requestBody.json"

response_data = None
request_data = None

with open(response_json_dir) as f:
  response_data = json.load(f)

with open(request_json_dir) as f:
  request_data = json.load(f)


# define request and response root
request_root = request_data.get("OTA_AirLowFareSearchRQ", {})
response_root = response_data["body"].get("responseData", {})

# get itineraries from response
itineraries = response_root.get("Itineraries", [])

target_itinerary = {}

skip_airlines = ["GF", "FZ"]
skip_airlines.remove("GF")
specific_airline_code = "BG"

# Specify itinerary
target_itinerary_id = 1
disallow_connected = False
specific_airline = False
only_definedID_airline = True

for itinerary in itineraries:
    if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") not in skip_airlines:
        if disallow_connected == True:
            if len(itinerary.get("ScheduleDescription", [])) == 1:
                if specific_airline == True:
                    if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") == specific_airline_code:
                        target_itinerary_id = itinerary.get("ID", "")
                        target_itinerary = itinerary
                elif only_definedID_airline == True:
                    if itinerary.get("ID", 0) == target_itinerary_id:
                        target_itinerary_id = itinerary.get("ID", "")
                        target_itinerary = itinerary
                else:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
        else:
            if specific_airline == True:
                if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") == specific_airline_code:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
            elif only_definedID_airline == True:
                if itinerary.get("ID", 0) == target_itinerary_id:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
            else:
                target_itinerary_id = itinerary.get("ID", "")
                target_itinerary = itinerary


data = {
    "ExistedToken": get_token(),
    "RequestLOG": false,
    "RequireUTILS": false,
    "RequestBody": {
        "OriginDestinationInformation": req_body_util_data["ticket_search"].get("OriginDestinationInformation", []),
        "DirectFlightsOnly": false,
        "AvailableFlightsOnly": false,
        "LegDescription": req_body_util_data["ticket_search"].get("LegDescription", []),
        "TargetItinerary": target_itinerary
    }
}


with open(final_json_file, "w") as outfile:
    target_json_data = {
        "RequestBody": data,
        "TargetItineraryID": target_itinerary_id,
        "LegDescription": req_body_util_data["ticket_search"].get("LegDescription", []),
        "TargetItinerary": target_itinerary
    }
    json.dump(target_json_data, outfile, indent=4)


event_body = data


def moduleRunner(testWithWhile=False, runAmount=7):
    """
    moduleRunner() => Skytrip Module Runner Function.
    params: testWithWhile (Boolean, default=False), runAmount (integer, default=7)
    """
    if testWithWhile == True:
        i = 0
        while i <= runAmount:
            modulehandler = RevalidateHandler(EventBodyData=event_body)
            response = modulehandler.sabre_revalidate_handler(generateJSON=True)
            print(f"\n {'*' * 50} Revalidate Response Data {'*' * 50} : \n\n",
                  response, "\n\n")
            i += 1
    else:
        modulehandler = RevalidateHandler(EventBodyData=event_body)
        response = modulehandler.sabre_revalidate_handler(generateJSON=True)
        print(f"\n {'*' * 50} Revalidate Response Data {'*' * 50} : \n\n",
              response, "\n\n")
    # return the response
    return response


# get actual response
response = moduleRunner(testWithWhile=False, runAmount=5)
