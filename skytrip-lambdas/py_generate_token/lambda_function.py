# import necessary modules and libraries
from skytrip.generate_token import SabreToken

# lambda handler
def lambda_handler(event, context):
    """
    lambda handler for generate token module
    """
    # define initial status code
    statusCode = 400

    try:
        # Sabre Token class instance
        sabre = SabreToken()
        # get and store the token form Sabre Token class method
        response = sabre.get_token()
        # update the status code
        statusCode = 200
    except Exception as E:
        response = str(E)

    # return the response
    return {
        'statusCode': statusCode,
        'body': response
    }
