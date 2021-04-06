# import necessary modules and libraries
import json
from skytrip.ticket_search.search_handler import SearchHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for ticket search module
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the search response result from search handler function
        search_handler = SearchHandler(EventBodyData=event_body)
        result = search_handler.sabre_search_handler()
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
