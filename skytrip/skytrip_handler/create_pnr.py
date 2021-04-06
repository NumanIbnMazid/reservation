# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper
from skytrip.db_read.get_skytrip_apis import get_skytrip_apis
import requests
import warnings


def create_pnr(RequestBody={}):
    """
    create_pnr() => Creates PNR.
    params => RequestBody (object)
    """
    # -------*******------- Fetch Payment Information from "payment" Table -------*******-------
    try:
        # if common pnr made false, then the pnr will only create for B2C with payment check
        commonPNR = True
        # define result placeholder
        result = None

        # create connection
        con = connect_db()
        # cursor
        cur = con.cursor(
            cursor_factory=DictCursor
        )

        # payment check holder
        passedPaymentCheck = False
        # payment id placeholder
        paymentID = None

        if commonPNR == True:

            # ------- Select Payment from Database -------

            if not RequestBody["DataSource"] in ["B2B", "B2B_AGENT", "B2B_ADMIN"] and RequestBody["TransactionID"] is not None and not RequestBody["TransactionID"] == "":

                try:
                    # Get payment ID
                    cur.execute(
                        "SELECT id FROM payment WHERE tran_id='{}'".format(
                            RequestBody.get("TransactionID", None)
                        )
                    )

                    payment = cur.fetchone()

                    # assign payment id
                    paymentID = payment["id"]
                    passedPaymentCheck = True

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to SELECT payment from 'payment' Table!"
                        )
                    )
        
        else:

            try:
                # Get payment ID
                cur.execute(
                    "SELECT id FROM payment WHERE tran_id='{}'".format(
                        RequestBody.get("TransactionID", None)
                    )
                )

                payment = cur.fetchone()

                # assign payment id
                paymentID = payment["id"]
                passedPaymentCheck = True

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg="Failed to SELECT payment from 'payment' Table!"
                    )
                )

        # ----------------------- Create PNR -----------------------
        def call_pnr_api(request_body=None, api_data=None):
            """
            call the pnr api and returns pnr response
            """
            headers = {
                'content-type': "application/json",
                'x-api-key': api_data["APIkey"]
            }
            params = {
                'body': request_body
            }

            pnr_api_response = requests.post(
                api_data["APIendpoint"], request_body, headers=headers
            )

            print("XXXXXXXXXXXXXXXXXXX", pnr_api_response)

            response = pnr_api_response.json()

            # return the response
            return response


        if passedPaymentCheck == True:
            # Get PNR API Information
            pnr_api_info_data_body = {
                "APImoduleName": "TicketReservation"
            }
            pnrAPIdata = get_skytrip_apis(RequestBody=pnr_api_info_data_body)

            # call for pnr creation
            pnr_response = call_pnr_api(
                request_body=RequestBody,
                api_data=pnrAPIdata
            )

            return pnr_response


        else:
            raise Exception(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed payment check! Can't create PNR!"
                )
            )


    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to Create PNR!"
            )
        )
