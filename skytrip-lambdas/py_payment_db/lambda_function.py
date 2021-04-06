# import necessary modules and libraries
import json
from skytrip.db_payment.db_payment_handler import DBpaymentHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for payment database management
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the db response from db payment handler
        db_payment_handler = DBpaymentHandler(
            EventBodyData=event_body
        )

        result = db_payment_handler.insert_data_in_payment()
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
