from skytrip.db_read.get_media_detail import get_media_detail
import json


data = {
    "MediaID": 63,
    "UserID": 25
}

response = get_media_detail(RequestBody=data)


print(f"\n {'*' * 50} Get Media Detail {'*' * 50} : \n\n Response: ", response, "\n\n")
