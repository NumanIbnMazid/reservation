# import necessary modules and libraries
import json
from skytrip.revalidate_itinerary.revalidate_handler import RevalidateHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for revalidate itinerary module
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the revalidate response from revalidate handler
        revalidate_handler = RevalidateHandler(EventBodyData=event_body)
        result = revalidate_handler.sabre_revalidate_handler()
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
