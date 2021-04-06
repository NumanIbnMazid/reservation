from skytrip.db_read.get_package_information_detail import get_package_information_detail
import json


data = {
    "PackageInformationID": 7
}

response = get_package_information_detail(RequestBody=data)


print(f"\n {'*' * 50} Get Package Information Detail {'*' * 50} : \n\n Response: ", response, "\n\n")
