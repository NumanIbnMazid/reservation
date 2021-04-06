from skytrip.db_read.get_user_medias import get_user_medias
import json


data = {
    "UserID": 2
}

response = get_user_medias(RequestBody=data)


print(f"\n {'*' * 50} Get User Medias {'*' * 50} : \n\n Response: ", response, "\n\n")
