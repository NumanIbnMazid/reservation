# import necessary modules and libraries
import json
from skytrip.ticket_issue.issue_handler import IssueHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for ticket issue module
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the ticket issue response result from issue handler function
        issue_handler = IssueHandler(EventBodyData=event_body)
        result = issue_handler.sabre_issue_handler()
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
