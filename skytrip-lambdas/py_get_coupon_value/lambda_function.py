# import necessary modules and libraries
import json
from skytrip.db_read.get_coupon_value import get_coupon_value


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting coupon value
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # Get coupon value
        result = get_coupon_value(RequestBody=event_body)
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
