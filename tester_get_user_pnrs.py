from skytrip.db_read.get_user_pnrs import get_user_pnrs
import json


data = {
    "UserID": 1
}

response = get_user_pnrs(RequestBody=data)


print(f"\n {'*' * 50} Get User PNRs {'*' * 50} : \n\n Response: ", response, "\n\n")
