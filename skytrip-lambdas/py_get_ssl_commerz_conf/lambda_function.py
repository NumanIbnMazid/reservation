# import necessary modules and libraries
import json
from skytrip.db_read.get_ssl_commerz_conf import get_ssl_commerz_conf


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting visa information detail
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # Get visa information detail
        result = get_ssl_commerz_conf()
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
