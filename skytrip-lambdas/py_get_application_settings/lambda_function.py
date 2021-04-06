# import necessary modules and libraries
import json
from skytrip.db_read.get_application_settings import get_application_settings


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting skytrip application settings
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # Get skytrip application settings
        result = get_application_settings()
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
