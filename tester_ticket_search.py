from skytrip.ticket_search.search_handler import SearchHandler
from tester_helper import get_token
import json

true = True
false = False

# load req body util data
req_body_util_JSON = "UTILS/JSON_STORE/req-body-util.json"
req_body_util_data = None
with open(req_body_util_JSON) as f:
    req_body_util_data = json.load(f)

data = {
    "ExistedToken": get_token(),
    "RequireUTILS": false,
    "RequestBody": {
        "OriginDestinationInformation": [
            {
                "DepartureDateTime": "2021-04-17T23:00:00",
                "OriginLocation": {
                    "LocationCode": "DAC"
                },
                "DestinationLocation": {
                    "LocationCode": "DXB"
                },
                "RPH": "0"
            },
            # {
            #     "DepartureDateTime": "2021-03-26T20:00:00",
            #     "OriginLocation": {
            #         "LocationCode": "CXB"
            #     },
            #     "DestinationLocation": {
            #         "LocationCode": "DAC"
            #     },
            #     "RPH": "1"
            # }
        ],
        "PassengerTypeQuantity": [
            {
                "Code": "ADT",
                "Quantity": 1
            },
            # {
            #     "Code": "CNN",
            #     "Quantity": 1
            # },
            # {
            #     "Code": "INF",
            #     "Quantity": 1
            # }
        ],
        "TicketClass": "Y",
        "DirectFlightsOnly": false,
        "AvailableFlightsOnly": false
    }
}

event_body = data
response = None


def moduleRunner(testWithWhile=False, runAmount=7):
    """
    moduleRunner() => Skytrip Module Runner Function.
    params: testWithWhile (Boolean, default=False), runAmount (integer, default=7)
    """
    if testWithWhile == True:
        i = 0
        while i <= runAmount:
            moduleHandler = SearchHandler(EventBodyData=event_body)
            response = moduleHandler.sabre_search_handler(generateJSON=True)
            print(f"\n {'*' * 50} Search Response Data {'*' * 50} : \n\n", response, "\n\n")
            i += 1
    else:
        moduleHandler = SearchHandler(EventBodyData=event_body)
        response = moduleHandler.sabre_search_handler(generateJSON=True)
        print(f"\n {'*' * 50} Search Response Data {'*' * 50} : \n\n", response, "\n\n")
    # return the response
    return response


# get actual response
response = moduleRunner(testWithWhile=False, runAmount=5)


# Update JSON of book_info
if response.get("statusCode", "") == 200:
    try:
        with open(req_body_util_JSON, "w") as outfile:
            req_body_util_data["ticket_search"]["OriginDestinationInformation"] = event_body["RequestBody"].get("OriginDestinationInformation", [])
            req_body_util_data["ticket_search"]["LegDescription"] = response["body"]["responseData"].get("LegDescription", [])
            json.dump(req_body_util_data, outfile, indent=4)
    except Exception as E:
        raise Exception(str(E))
