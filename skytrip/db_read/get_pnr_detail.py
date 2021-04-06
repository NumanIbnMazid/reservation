# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_pnr_detail(RequestBody={}):
    """
    get_pnr_detail() => Retrieves pnr detail from database.
    params => RequestBody (object)
    """
    try:
        # define result placeholder
        result = None

        # create connection
        con = connect_db()
        # cursor
        cur = con.cursor(
            cursor_factory=DictCursor
        )

        # -------*******------- Fetch Records from "pnr" Table -------*******-------
        try:
            # Get User pnr Query
            cur.execute(
                "SELECT id, user_id, payment_id, pnr_no, is_production, route_1_origin_location_code, route_1_destination_location_code, route_1_departure_date, route_2_origin_location_code, route_2_destination_location_code, route_2_departure_date, route_3_origin_location_code, route_3_destination_location_code, route_3_departure_date, route_4_origin_location_code, route_4_destination_location_code, route_4_departure_date, cabin_class, total_amount, currency, is_ticketed, data_source, utils, sabre_token, created_at FROM pnr WHERE id='{}' AND user_id='{}'".format(
                    RequestBody.get("PNR-ID", None), RequestBody.get("UserID", None)
                )
            )

            # fetch user pnr
            pnr = cur.fetchone()

            # define target map
            target_map = {
                "ID": None,
                "UserID": None,
                "PaymentID": None,
                "PnrNo": None,
                "IsProduction": None,
                "Route1OriginLocationCode": None,
                "Route1DestinationLocationCode": None,
                "Route1DepartureDate": None,
                "Route2OriginLocationCode": None,
                "Route2DestinationLocationCode": None,
                "Route2DepartureDate": None,
                "Route3OriginLocationCode": None,
                "Route3DestinationLocationCode": None,
                "Route3DepartureDate": None,
                "Route4OriginLocationCode": None,
                "Route4DestinationLocationCode": None,
                "Route4DepartureDate": None,
                "CabinClass": None,
                "TotalAmount": None,
                "Currency": None,
                "IsTicketed": None,
                "DataSource": None,
                "Utils": None,
                "SabreToken": None,
                "CreatedAt": None,
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_detail_response(
                response=pnr, target_map=target_map
            )

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to SELECT PNR Detail from 'pnr' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to get PNR Detail!"
            )
        )
