# import necessary modules and libraries
import json
from skytrip.user_media.media_upload_handler import MediaUploadHandler


# lambda handler function
def lambda_handler(event, context):
    """
    lambda_handler for user media module
    """
    # define initial status code and headers
    statusCode = 400
    try:
        # get the body params
        if type(event) == dict:
            event_body = event.get('body', event)
        else:
            event_body = json.loads(event).get('body', {})
        # generate and store the user media upload response result from media upload handler function
        media_upload_handler = MediaUploadHandler(EventBodyData=event_body)
        result = media_upload_handler.upload_media()
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
