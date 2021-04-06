from skytrip.db_read.get_visa_information_list import get_visa_information_list
import json

response = get_visa_information_list()


print(f"\n {'*' * 50} Get Visa Information List {'*' * 50} : \n\n Response: ", response, "\n\n")
