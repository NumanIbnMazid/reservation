# import necessary modules and libraries
from skytrip.generate_token import SabreToken
from skytrip_config.config import SkyTripConfig
from skytrip.utils.helper import create_dirs_files
import json
import os


def manage_json(response={}):

    try:
        token_json_dir = "UTILS/JSON_STORE/tokens.json"

        if os.path.exists(token_json_dir):
            token_dict = {}
            with open(token_json_dir) as f:
                token_dict = json.load(f)

            # get production status
            skytrip_conf = SkyTripConfig()
            is_production = skytrip_conf.get_is_production()

            print(f"\n\n *** IS_PRODUCTION : {is_production} *** \n\n")

            # prepare data containing tokens
            if is_production == True:
                token_dict["Production"] = response
            else:
                token_dict["Certification"] = response

            # generate files
            with open(token_json_dir, "w") as outfile:
                json.dump(token_dict, outfile, indent=4)
        else:
            # create directories and files
            create_dirs_files(filename=token_json_dir, create_init=False)
            # define json structure
            json_structure = {
                "Certification": {},
                "Production": {}
            }
            # create json file
            with open(token_json_dir, "w") as outfile:
                json.dump(json_structure, outfile, indent=4)
            # recursive call
            manage_json(response=response)

    except Exception as E:
        raise Exception(
            f"***Error*** (tester_generate_token.py) => manage_json() : An Exception Occured! Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )



# Sabre Token class instance
sabre = SabreToken()
response = sabre.get_token()
print(response)


# manage json
manage_json(response=response)
