from skytrip.db_read.get_pnr_detail import get_pnr_detail
import json


data = {
    "PNR-ID": 384,
    "UserID": 1
}

response = get_pnr_detail(RequestBody=data)


print(f"\n {'*' * 50} Get PNR Detail {'*' * 50} : \n\n Response: ", response, "\n\n")
