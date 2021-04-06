from skytrip.db_read.get_ssl_commerz_conf import get_ssl_commerz_conf
import json

response = get_ssl_commerz_conf()


print(f"\n {'*' * 50} Get SSL Commerz Conf {'*' * 50} : \n\n Response: ", response, "\n\n")
