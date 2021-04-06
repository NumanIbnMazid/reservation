# import necessary modules and libraries
import json
from skytrip.db_read.get_skytrip_apis import get_skytrip_apis


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for getting skytrip api
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # Get skytrip api
        result = get_skytrip_apis(RequestBody=event_body)
        # define status code, headers and response
        if type(result) == dict:
            statusCode = 200
            response = result
        else:
            response = result
    except Exception as E:
        response = str(E)

    # return the response
    return {
        'statusCode': statusCode,
        'body': response
    }
