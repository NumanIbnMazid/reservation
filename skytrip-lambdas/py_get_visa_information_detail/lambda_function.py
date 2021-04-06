# import necessary modules and libraries
import json
from skytrip.db_read.get_visa_information_detail import get_visa_information_detail


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting visa information detail
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # Get visa information detail
        result = get_visa_information_detail(RequestBody=event_body)
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
