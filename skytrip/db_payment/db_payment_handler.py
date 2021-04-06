# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message, finalize_response
from dateutil.parser import parse
import inspect


class DBpaymentHandler:

    def __init__(self, EventBodyData=None):
        # define event body data
        self.event_body = EventBodyData


    def insert_data_in_payment(self):
        """
        insert_data_in_payment() => Inserts payment data in database
        """
        try:
            try:
                
                # create connection
                con = connect_db()
                # cursor
                cur = con.cursor()

                # -------*******------- Insert Data in 'payment' table -------*******-------
                # Field Count => 4
                cur.execute(
                    "INSERT INTO payment(user_email, tran_id, transaction_log, total_amt) values(%s,%s,%s,%s) RETURNING id;",
                    (
                        self.event_body.get("user_email", None),
                        self.event_body.get("tran_id", None),
                        self.event_body.get("transaction_log", None),
                        float(self.event_body.get("amount", None)) if not self.event_body.get("amount", None) == "" else 0.0
                    )
                )
                # Commit the payment transaction
                con.commit()

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed to insert data in 'payment' table!"
                    )
                )

            try:
                
                # -------*******------- Insert Data in 'payment_details' table -------*******-------
                # get inserted Payment row
                inserted_payment_row = cur.fetchone()
                # get PAYMENT ID
                # payment_id = inserted_payment_row['id']
                payment_id = inserted_payment_row[0]

                # Field Count => 21
                cur.execute(
                    "INSERT INTO payment_details(payment_id, amount, card_type, store_amount, card_no, bank_tran_id, status, tran_date, currency, card_issuer, card_brand, card_issuer_country, card_issuer_country_code, store_id, verify_sign, verify_key, cus_fax, currency_type, currency_amount, currency_rate, base_fair) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    (
                        inserted_payment_row, 
                        float(self.event_body.get("amount", None)) if not self.event_body.get("amount", None) == "" else 0.0,
                        self.event_body.get("card_type", None),
                        float(self.event_body.get("store_amount", "")) if not self.event_body.get("store_amount", "") == "" else 0.0,
                        self.event_body.get("card_no", None),
                        self.event_body.get("bank_tran_id", None),
                        self.event_body.get("status", None),
                        self.event_body.get("tran_date", None),
                        self.event_body.get("currency", None),
                        self.event_body.get("card_issuer", None),
                        self.event_body.get("card_brand", None),
                        self.event_body.get("card_issuer_country", None),
                        self.event_body.get("card_issuer_country_code", None),
                        self.event_body.get("store_id", None),
                        self.event_body.get("verify_sign", None),
                        self.event_body.get("verify_key", None),
                        self.event_body.get("cus_fax", None),
                        self.event_body.get("currency_type", None),
                        float(self.event_body.get("currency_amount", None)) if not self.event_body.get("currency_amount", None) == "" else 0.0,
                        float(self.event_body.get("currency_rate", None)) if not self.event_body.get("currency_rate", None) == "" else 0.0,
                        float(self.event_body.get("base_fair", None)) if not self.event_body.get("base_fair", None) == "" else 0.0
                    )
                )

                # Commit the payment transaction
                con.commit()

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed to insert data in 'payment_details' table!"
                    )
                )

             # ------------------- *** validate structure and finalize response *** -------------------
            result = {
                "statusCode": 200,
                "body": {
                    "responseData": {
                        "paymentID": payment_id
                    }
                }
            }
            finalized_response = finalize_response(response=result)
            
            # return finalized_response
            return finalized_response

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to insert data in Database!"
                )
            )

