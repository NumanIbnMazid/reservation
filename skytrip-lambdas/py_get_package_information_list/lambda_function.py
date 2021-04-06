# import necessary modules and libraries
import json
from skytrip.db_read.get_package_information_list import get_package_information_list


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting package information list
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # Get package information list
        result = get_package_information_list()
        # define status code, headers and response
        if type(result) == dict:
            statusCode = result.get("statusCode", statusCode)
            response = result.get("body", "")
        else:
            response = result
    except Exception as E:
        response = str(E)

    # return the response
    return {
        'statusCode': statusCode,
        'body': response
    }
