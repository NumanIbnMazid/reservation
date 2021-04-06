# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_ssl_commerz_conf():
    """
    get_ssl_commerz_conf() => Retrieves ssl commerz configuration from database.
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

        # -------*******------- Fetch Records from "setup_sslcommerzconf" Table -------*******-------
        try:
            # Get ssl commerz conf Query
            cur.execute(
                "SELECT id, store_id, store_password, created_by_id, created_at, updated_at FROM setup_sslcommerzconf ORDER BY created_at DESC LIMIT 1"
            )

            # fetch ssl commerz conf
            ssl_commerz_conf = cur.fetchone()

            # define target map
            target_map = {
                "ID": None,
                "StoreID": None,
                "StorePassword": None,
                "CreatedByUserID": None,
                "CreatedAt": None,
                "UpdatedAt": None
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_detail_response(
                response=ssl_commerz_conf, target_map=target_map
            )

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to SELECT SSL Commerz Configuration from 'setup_sslcommerzconf' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to get SSL Commerz Configuration!"
            )
        )
