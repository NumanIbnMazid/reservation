# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_package_information_detail(RequestBody={}):
    """
    get_media_detail() => Retrieves package_information detail from database.
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

        # -------*******------- Fetch Records from "setup_packageinformation" Table -------*******-------
        try:
            # Get Package Information Query
            cur.execute(
                "SELECT id, package_name, offer_rate, num_of_days, amount, cut_off_amount, image, summary, created_at, updated_at FROM setup_packageinformation WHERE id='{}'".format(
                    RequestBody.get("PackageInformationID", None)
                )
            )

            # fetch user medias
            package_information = cur.fetchone()

            # define target map
            target_map = {
                "ID": None,
                "PackageInformation": None,
                "OfferRate": None,
                "NumOfDays": None,
                "Amount": None,
                "CutOffAmount": None,
                "Image": None,
                "Summary": None,
                "CreatedAt": None,
                "UpdatedAt": None
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_detail_response(
                response=package_information, target_map=target_map
            )

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to SELECT Package Information Detail from 'setup_packageinformation' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to get Package Information Detail!"
            )
        )
