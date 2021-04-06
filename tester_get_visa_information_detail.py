from skytrip.db_read.get_visa_information_detail import get_visa_information_detail
import json


data = {
    "VisaInformationID": 4
}

response = get_visa_information_detail(RequestBody=data)


print(f"\n {'*' * 50} Get Visa Information Detail {'*' * 50} : \n\n Response: ", response, "\n\n")
