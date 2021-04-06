from skytrip_config.config import SkyTripConfig
import json
import datetime


def get_token():
    try:
        token_dict = {}
        token_json_dir = "UTILS/JSON_STORE/tokens.json"
        token_dict = {}
        with open(token_json_dir) as f:
            token_dict = json.load(f)
        # get production status
        skytrip_conf = SkyTripConfig()
        is_production = skytrip_conf.get_is_production()

        # print production status
        print(f"\n\n *** (tester_helper) => IS_PRODUCTION : {is_production} *** \n\n")

        # return existed tokens
        return token_dict["Production"] if is_production == True else token_dict["Certification"]

    except Exception as E:
        raise Exception(
            f"***Error*** (tester_helper.py) => get_token() : An Exception Occured! Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )

def is_production():
    try:
        # get production status
        skytrip_conf = SkyTripConfig()
        is_production = skytrip_conf.get_is_production()

        # return production status
        return is_production

    except Exception as E:
        raise Exception(
            f"***Error*** (tester_helper.py) => is_production() : An Exception Occured! Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )


def manage_book_info_json(pnr_ID=None, response=None, info_node_name=None, detail_node_name=None):

    if is_production() == True:
        pnr_ID = response["body"]["responseData"]["CreatePassengerNameRecordRS"]["ItineraryRef"].get("ID", None)
        existing_book_info_data = None
        existing_book_detail_data = None

        # get book info existing JSON
        book_info_json = "UTILS/JSON_STORE/book-info.json"
        # get book detail existing JSON
        book_detail_json = "UTILS/JSON_STORE/book-detail.json"

        # Get book info data JSON
        with open(book_info_json) as f:
            existing_book_info_data = json.load(f)
        # Get book detail data JSON
        with open(book_detail_json) as f:
            existing_book_detail_data = json.load(f)

        # Update JSON of book_info
        with open(book_info_json, "w") as outfile:
            existing_book_info_data[info_node_name].append(
                {
                    pnr_ID: str(datetime.datetime.now())
                }
            )
            json.dump(existing_book_info_data, outfile, indent=4)

        # Update JSON of book_detail
        with open(book_detail_json, "w") as outfile:
            existing_book_detail_data[detail_node_name].append(
                {
                    pnr_ID: {
                        str(datetime.datetime.now()): response
                    }
                }
            )
            json.dump(existing_book_detail_data, outfile, indent=4)
