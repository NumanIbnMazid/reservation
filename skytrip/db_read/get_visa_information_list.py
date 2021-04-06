# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_visa_information_list():
    """
    get_visa_information_list() => Retrieves Visa Information from database.
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

        # -------*******------- Fetch Records from "setup_visainformation" Table -------*******-------
        try:
            # Get User Medias Query
            cur.execute(
                "SELECT id, code, country, information, created_by_id, created_at, updated_at FROM setup_visainformation"
            )

            # fetch visa information list
            visa_information_list = cur.fetchall()

            # define target map
            target_map = {
                "ID": None,
                "Code": None,
                "Country": None,
                "Information": None,
                "CreatedByUserID": None,
                "CreatedAt": None,
                "UpdatedAt": None
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_response(
                response=visa_information_list, target_map=target_map
            )

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to SELECT Visa Information from 'setup_visainformation' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to get Visa Information!"
            )
        )
