# import necessary modules and libraries
import json
from skytrip.ticket_reservation.reservation_handler import ReservationHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for ticket reservation module
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the reservation response result from reservation handler function
        reservation_handler = ReservationHandler(EventBodyData=event_body)
        result = reservation_handler.sabre_reservation_handler()
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

