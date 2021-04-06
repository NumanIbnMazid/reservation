# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
from dateutil.parser import parse
import inspect
from skytrip_config.config import SkyTripConfig
from psycopg2.extras import DictCursor


class DBhandler:

    def prepare_ticket_issue_data_map(self, request=None, response=None):
        """
        prepare_ticket_issue_data_map() => Preapares Data Map to insert data in 'ticket_issue' table.
        params => request (object, EventBodyData), response (object, Issue response object)
        """

        try:

            response_root = response["body"]["responseData"].get("AirTicketRS", {})
            request_root = request.get("RequestBody", {})

            # -- PNR Number
            pnr_no = request_root.get("ItineraryID", None)

            # prepare data dictionary
            data_map = {
                # -- PNR Number
                "pnr_no": pnr_no
            }

            # return the data map
            return data_map

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to prepare data map for 'pnr' table!"
                )
            )


    def insert_data(self, request=None, response=None):
        """
        insert_data() => Inserts data into AWS RDS Database.
        params => response (object, PNR Response)
        """

        try:
            # pnr id placeholder
            issued_ticket_id = None
            # create connection
            con = connect_db()
            # cursor
            cur = con.cursor(
                cursor_factory=DictCursor
            )

            # -------*******------- Insert Data in 'ticket_issue' table -------*******-------
            try:
                # prepare data
                sql_pnr_data_map = self.prepare_ticket_issue_data_map(
                    request=request, response=response
                )

                try:
                    # Get PNR ID
                    cur.execute(
                        "SELECT id FROM pnr WHERE pnr_no='{}'".format(
                            sql_pnr_data_map.get("pnr_no", None)
                        )
                    )

                    PNR = cur.fetchone()

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to SELECT PNR from 'pnr' Table!"
                        )
                    )

                try:
                    # Field Count => 1
                    cur.execute("INSERT INTO ticket_issue(pnr_id) values(%s) RETURNING id;",
                        (PNR["id"],)
                    )

                    # Commit the issue ticket transaction
                    con.commit()
                    # get inserted issued ticket row
                    inserted_issue_row = cur.fetchone()
                    # get Issue ID
                    issued_ticket_id = inserted_issue_row['id']

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to INSERT data in 'issue_ticket' Table!"
                        )
                    )

                # Update PNR is_ticketed status
                try:
                    cur.execute(
                        "UPDATE pnr SET is_ticketed={} WHERE pnr_no='{}'".format(
                            True, sql_pnr_data_map.get("pnr_no", None)
                        )
                    )

                    # Commit the issue ticket transaction
                    con.commit()

                except Exception as E:
                    raise Exception(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Failed to UPDATE pnr 'is_ticketed' status!"
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
            return issued_ticket_id

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Database Transaction Failed!"
                )
            )
