from skytrip.db_read.get_application_settings import get_application_settings
import json

response = get_application_settings()

print(f"\n {'*' * 50} Get Skytrip Application Settings {'*' * 50} : \n\n Response: ", response, "\n\n")
