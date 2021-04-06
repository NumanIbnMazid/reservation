# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_user_medias(RequestBody={}):
    """
    get_user_medias() => Retrieves User Medias for a specific user from database.
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

        # -------*******------- Fetch Records from "user_media" Table -------*******-------
        try:
            # Get User Medias Query
            cur.execute(
                "SELECT id, media_category, media_s3_url, user_id, created_at FROM user_media WHERE user_id='{}'".format(
                    RequestBody.get("UserID", None)
                )
            )

            # fetch user medias
            user_medias = cur.fetchall()

            # define target map
            target_map = {
                "ID": None,
                "MediaCategory": None,
                "MediaS3URL": None,
                "UserID": None,
                "CreatedAt": None,
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_response(
                response=user_medias, target_map=target_map
            )

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to SELECT User Medias from 'user_media' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to get User Medias!"
            )
        )
