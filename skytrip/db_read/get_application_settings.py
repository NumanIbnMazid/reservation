# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_application_settings():
    """
    get_application_settings() => Retrieves Skytrip Application Settings.
    params => RequestBody (object)
    """
    # -------*******------- Fetch Application Settings from "setup_applicationsetting" Table -------*******-------
    try:
        # define result placeholder
        result = None

        # create connection
        con = connect_db()
        # cursor
        cur = con.cursor(
            cursor_factory=DictCursor
        )
        # Get Application Settings Query
        cur.execute(
            "SELECT id, application_name, is_production, skytrip_address, application_domain_url, facebook_app_id, google_client_id, created_at, updated_at FROM setup_applicationsetting LIMIT 1"
        )

        # fetch Application Settings
        skytrip_settings = cur.fetchone()

        # define target map
        target_map = {
            "ID": None,
            "ApplicationName": None,
            "IsProduction": None,
            "SkytripAddress": None,
            "ApplicationDomainURL": None,
            "FacebookAppID": None,
            "GoogleClientID": None,
            "CreatedAt": None,
            "UpdatedAt": None
        }

        # DB Read Helper Instance
        db_read_helper = DBreadHelper()

        # assign result from map response
        result = db_read_helper.map_detail_response(
            response=skytrip_settings, target_map=target_map
        )

        # return the result
        return result

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to SELECT Application Settings from 'setup_applicationsetting' Table!"
            )
        )