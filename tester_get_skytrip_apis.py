from skytrip.db_read.get_skytrip_apis import get_skytrip_apis
import json


data = {
    "APImoduleName": "TicketReservation"
}

response = get_skytrip_apis(RequestBody=data)


print(f"\n {'*' * 50} Get Skytrip APIS {'*' * 50} : \n\n Response: ", response, "\n\n")
