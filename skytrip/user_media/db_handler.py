# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor


class DBhandler:

    def prepare_user_media_data_map(self, request=None, response=None):
        """
        prepare_user_media_data_map() => Preapares Data Map to insert data in 'user_media' table.
        params => request (object, EventBodyData), response (object, Issue response object)
        """

        try:

            response_root = response["body"].get(
                "responseData", {}
            )

            # -- user_id
            user_id = request.get("UserID", None)
            # -- media_category
            media_category = request.get("MediaCategory", None)
            # -- media_s3_url
            media_s3_url = response_root.get("MediaS3URL", None)

            # prepare data dictionary
            data_map = {
                "user_id": user_id,
                "media_category": media_category,
                "media_s3_url": media_s3_url
            }

            # return the data map
            return data_map

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to prepare data map for 'user_media' table!"
                )
            )

    def insert_data(self, request=None, response=None):
        """
        insert_data() => Inserts data into AWS RDS Database.
        params => response (object, user_media_upload Response)
        """

        try:
            # pnr id placeholder
            uploaded_media_db_id = None
            # create connection
            con = connect_db()
            # cursor
            cur = con.cursor(
                cursor_factory=DictCursor
            )

            # -------*******------- Insert Data in 'ticket_issue' table -------*******-------
            try:
                # prepare data
                sql_user_media_data_map = self.prepare_user_media_data_map(
                    request=request, response=response
                )
                user_id = None

                try:
                    # Get User ID
                    cur.execute(
                        "SELECT id FROM skytrip_user WHERE id='{}'".format(
                            sql_user_media_data_map.get("user_id", None)
                        )
                    )

                    user = cur.fetchone()
                    user_id = user["id"]

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to SELECT User from 'skytrip_user' Table!"
                        )
                    )

                try:
                    # Field Count => 1
                    cur.execute(
                        "INSERT INTO user_media(user_id, media_category, media_s3_url) values(%s,%s,%s) RETURNING id;",
                        (user_id, 
                        sql_user_media_data_map.get("media_category", None), 
                        sql_user_media_data_map.get("media_s3_url", None),
                        )
                    )

                    # Commit the issue ticket transaction
                    con.commit()
                    # get inserted uploaded media row
                    inserted_media_row = cur.fetchone()
                    # get Issue ID
                    uploaded_media_db_id = inserted_media_row['id']

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to INSERT data in 'user_media' Table!"
                        )
                    )

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed Database Transaction!"
                    )
                )

            # close connection
            con.close()

            # return issued ticket id
            return uploaded_media_db_id

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Database Transaction Failed!"
                )
            )
