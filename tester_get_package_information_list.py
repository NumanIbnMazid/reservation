from skytrip.db_read.get_package_information_list import get_package_information_list
import json

response = get_package_information_list()

print(f"\n {'*' * 50} Get Package Information List {'*' * 50} : \n\n Response: ", response, "\n\n")
