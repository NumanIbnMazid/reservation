# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
from dateutil.parser import parse
import inspect
from skytrip_config.config import SkyTripConfig
from psycopg2.extras import DictCursor
import json
import datetime


class DBhandler:

    def prepare_pnr_data_map(self, request=None, response=None):
        """
        prepare_pnr_data_map() => Preapares Data Map to insert data in 'pnr' table.
        params => request (object, EventBodyData), response (object, PNR response object)
        """

        try:

            response_root = response["body"]["responseData"].get("CreatePassengerNameRecordRS", {})
            request_root = request.get("RequestBody", {})

            # -- PNR Number
            pnr_no = response_root["ItineraryRef"].get("ID", None)
            # -- ROUTE -> ONE (1)
            route_1_origin_location_code = request_root["OriginDestinationInformation"][0]["OriginLocation"].get(
                "LocationCode", None
            )
            route_1_destination_location_code = request_root["OriginDestinationInformation"][0]["DestinationLocation"].get(
                "LocationCode", None
            )
            route_1_departure_date = parse(
                request_root["OriginDestinationInformation"][0].get(
                    "DepartureDateTime", None
                )
            )
            # -- ROUTE -> TWO (2)
            if len(request_root["OriginDestinationInformation"]) >= 2:
                route_2_origin_location_code = request_root["OriginDestinationInformation"][1]["OriginLocation"].get(
                    "LocationCode", ""
                )
                route_2_destination_location_code = request_root["OriginDestinationInformation"][1]["DestinationLocation"].get(
                    "LocationCode", ""
                )
                route_2_departure_date = parse(
                    request_root["OriginDestinationInformation"][1].get(
                        "DepartureDateTime", ""
                    )
                )
            else:
                route_2_origin_location_code, route_2_destination_location_code, route_2_departure_date = None, None, None
            # -- ROUTE -> THREE (3)
            if len(request_root["OriginDestinationInformation"]) >= 3:
                route_3_origin_location_code = request_root["OriginDestinationInformation"][2]["OriginLocation"].get(
                    "LocationCode", ""
                )
                route_3_destination_location_code = request_root["OriginDestinationInformation"][2]["DestinationLocation"].get(
                    "LocationCode", ""
                )
                route_3_departure_date = parse(
                    request_root["OriginDestinationInformation"][2].get(
                        "DepartureDateTime", ""
                    )
                )
            else:
                route_3_origin_location_code, route_3_destination_location_code, route_3_departure_date = None, None, None
            # -- ROUTE -> FOUR (4)
            if len(request_root["OriginDestinationInformation"]) >= 4:
                route_4_origin_location_code = request_root["OriginDestinationInformation"][3]["OriginLocation"].get(
                    "LocationCode", ""
                )
                route_4_destination_location_code = request_root["OriginDestinationInformation"][3]["DestinationLocation"].get(
                    "LocationCode", ""
                )
                route_4_departure_date = parse(
                    request_root["OriginDestinationInformation"][3].get(
                        "DepartureDateTime", ""
                    )
                )
            else:
                route_4_origin_location_code, route_4_destination_location_code, route_4_departure_date = None, None, None
            # -- Carrier Code
            carrier_code = request_root["TargetItinerary"]["ScheduleDescription"][0]["Carrier"].get(
                "OperatingCarrierCode", None
            )
            # -- Flight Number
            flight_number = request_root["TargetItinerary"]["ScheduleDescription"][0]["Carrier"].get(
                "OperatingFlightNumber", None
            )
            # -- Cabin Class
            cabin_class = request_root["TargetItinerary"]["PassengerInfo"][0]["FareDescription"][0]["Segment"][0].get(
                "CabinClass", None
            )
            # -- Total Amount
            total_amount = request_root["TargetItinerary"]["TotalFare"].get(
                "TotalFare", None
            )
            # -- Currency
            currency = request_root["TargetItinerary"]["TotalFare"].get(
                "FareCurrency", None
            )

            # prepare data dictionary
            data_map = {
                # -- PNR Number
                "pnr_no": pnr_no,
                # -- ROUTE -> (1)
                "route_1_origin_location_code": route_1_origin_location_code,
                "route_1_destination_location_code": route_1_destination_location_code,
                "route_1_departure_date": route_1_departure_date,
                # -- ROUTE -> (2)
                "route_2_origin_location_code": route_2_origin_location_code,
                "route_2_destination_location_code": route_2_destination_location_code,
                "route_2_departure_date": route_2_departure_date,
                # -- ROUTE -> (3)
                "route_3_origin_location_code": route_3_origin_location_code,
                "route_3_destination_location_code": route_3_destination_location_code,
                "route_3_departure_date": route_3_departure_date,
                # -- ROUTE -> (4)
                "route_4_origin_location_code": route_4_origin_location_code,
                "route_4_destination_location_code": route_4_destination_location_code,
                "route_4_departure_date": route_4_departure_date,
                "carrier_code": carrier_code,
                "flight_number": flight_number,
                "cabin_class": cabin_class,
                "total_amount": total_amount,
                "currency": currency,
            }

            # return the data map
            return data_map

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to prepare data map for PNR Database!"
                )
            )

    def prepare_pnr_details_data_map_list(self, request=None):
        """
        prepare_pnr_details_data_map_list() => Preapares Data Map to insert data in 'pnr_details' table.
        params => request (object, EventBodyData)
        """
        try:

            data_map_list = []

            request_root = request.get("RequestBody", {})

            PersonName = request_root.get("PersonName", [])
            ContactNumber = request_root.get("ContactNumber", [])
            Email = request_root.get("Email", [])
            AdvancePassenger = request_root.get("AdvancePassenger", [])
            
            for idx, Person in enumerate(PersonName):
                if Person["NameNumber"]:
                    # -- Passenger Personal Information
                    passenger_name_number = Person.get("NameNumber", None)
                    passenger_given_name = Person.get("GivenName", None)
                    passenger_surname = Person.get("Surname", None)

                    # Placeholders
                    passenger_email, passenger_contact = None, None
                    passport_number, passport_issuing_country, passport_nationality_country, passport_expiration_date = None, None, None, None
                    visa_number, visa_applicable_country, visa_place_of_birth, visa_place_of_issue, visa_issue_date, visa_expiration_date = None, None, None, None, None, None

                    for Em in Email:
                        if Em.get("NameNumber", None) == Person["NameNumber"]:
                            passenger_email = Em.get("Address", None)

                    for Contact in ContactNumber:
                        if Contact.get("NameNumber", None) == Person["NameNumber"]:
                            passenger_contact = Contact.get("Phone", None)

                    passenger_dob = Person.get("DateOfBirth", None)
                    passenger_gender = Person.get("Gender", None)
                    passenger_type = Person.get("PassengerType", None)

                    for VisaPass in AdvancePassenger:
                        if VisaPass["PersonName"].get("NameNumber", None) == Person["NameNumber"]:
                            if VisaPass["Document"].get("Type", None) == "P":
                                # -- Passport Information
                                passport_number = VisaPass["Document"].get("Number", None)
                                passport_issuing_country = VisaPass["Document"].get("IssueCountry", None)
                                passport_nationality_country = VisaPass["Document"].get("NationalityCountry", None)
                                passport_expiration_date = VisaPass["Document"].get("ExpirationDate", None)

                            if VisaPass["Document"].get("Type", None) == "V":
                                # -- Visa Information
                                visa_number = VisaPass["Document"].get("NameNumber", None)
                                visa_applicable_country = VisaPass["Document"]["Visa"].get("ApplicableCountry", None)
                                visa_place_of_birth = VisaPass["Document"]["Visa"].get("PlaceOfBirth", None)
                                visa_place_of_issue = VisaPass["Document"]["Visa"].get("PlaceOfIssue", None)
                                visa_issue_date = VisaPass["Document"]["Visa"].get("IssueDate", None)
                                visa_expiration_date = VisaPass["Document"]["Visa"].get("ExpirationDate", None)

                    data_map_list.append(
                        {
                            "passenger_name_number": passenger_name_number,
                            "passenger_given_name": passenger_given_name,
                            "passenger_surname": passenger_surname,
                            "passenger_email": passenger_email,
                            "passenger_contact": passenger_contact,
                            "passenger_dob": passenger_dob,
                            "passenger_gender": passenger_gender,
                            "passenger_type": passenger_type,
                            "passport_number": passport_number,
                            "passport_issuing_country": passport_issuing_country,
                            "passport_nationality_country": passport_nationality_country,
                            "passport_expiration_date": passport_expiration_date,
                            "visa_number": visa_number,
                            "visa_applicable_country": visa_applicable_country,
                            "visa_place_of_birth": visa_place_of_birth,
                            "visa_place_of_issue": visa_place_of_issue,
                            "visa_issue_date": visa_issue_date,
                            "visa_expiration_date": visa_expiration_date
                        }
                    )
                    
                else:
                    raise ValueError(
                        get_exception_message(
                            Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg="Person NameNumber is required!"
                        )
                    )

            # return data map list
            return data_map_list



        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to prepare data map for PNR Details Database!"
                )
            )

    def insert_data(self, request=None, response=None):
        """
        insert_data() => Inserts data into AWS RDS Database.
        params => response (object, PNR Response)
        """
        
        try:
            # pnr id placeholder
            pnr_id = None
            
            # create connection
            con = connect_db()
            # cursor
            cur = con.cursor(
                cursor_factory=DictCursor
            )

            # -------*******------- Insert Data in 'pnr' table -------*******-------
            try:

                # ------- Select Payment from Database -------

                payment_id = None

                if not request["DataSource"] in ["B2B", "B2B_AGENT", "B2B_ADMIN"] and request["TransactionID"] is not None and not request["TransactionID"] == "":

                    try:
                        # Get payment ID
                        cur.execute(
                            "SELECT id FROM payment WHERE tran_id='{}'".format(
                                request.get("TransactionID", None)
                            )
                        )

                        payment = cur.fetchone()

                        # assign payment id
                        payment_id = payment["id"]

                    except Exception as E:
                        raise Exception(
                            get_exception_message(
                                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                    0][2],
                                msg="Failed to SELECT payment from 'payment' Table!"
                            )
                        )

                # prepare data
                sql_pnr_data_map = self.prepare_pnr_data_map(request=request, response=response)

                # get production status
                skytrip_conf = SkyTripConfig()
                is_production = skytrip_conf.get_is_production()
                # get sabre token
                sabre_token = json.dumps(request.get('ExistedToken', {}))
                # get utils
                utils = json.dumps(request.get('Utils', {}))

                # Field Count => 25
                cur.execute(
                    "INSERT INTO pnr(user_id, payment_id, pnr_no, is_production, is_ticketed, data_source, route_1_origin_location_code, route_1_destination_location_code, route_1_departure_date, route_2_origin_location_code, route_2_destination_location_code, route_2_departure_date, route_3_origin_location_code, route_3_destination_location_code, route_3_departure_date, route_4_origin_location_code, route_4_destination_location_code, route_4_departure_date, carrier_code, flight_number, cabin_class, total_amount, currency, utils, sabre_token) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
                    (
                        request.get("UserID", None),
                        payment_id,
                        sql_pnr_data_map.get("pnr_no", None),
                        is_production,
                        False,
                        str(request.get("DataSource", None)),
                        sql_pnr_data_map.get("route_1_origin_location_code", None),
                        sql_pnr_data_map.get("route_1_destination_location_code", None),
                        sql_pnr_data_map.get("route_1_departure_date", None),
                        sql_pnr_data_map.get("route_2_origin_location_code", None),
                        sql_pnr_data_map.get("route_2_destination_location_code", None),
                        sql_pnr_data_map.get("route_2_departure_date", None),
                        sql_pnr_data_map.get("route_3_origin_location_code", None),
                        sql_pnr_data_map.get("route_3_destination_location_code", None),
                        sql_pnr_data_map.get("route_3_departure_date", None),
                        sql_pnr_data_map.get("route_4_origin_location_code", None),
                        sql_pnr_data_map.get("route_4_destination_location_code", None),
                        sql_pnr_data_map.get("route_4_departure_date", None),
                        sql_pnr_data_map.get("carrier_code", None),
                        sql_pnr_data_map.get("flight_number", None),
                        sql_pnr_data_map.get("cabin_class", None),
                        sql_pnr_data_map.get("total_amount", None),
                        sql_pnr_data_map.get("currency", None),
                        utils,
                        sabre_token,
                    )
                )

                # Commit the pnr transaction
                con.commit()

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed to insert Data in 'pnr' Table!"
                    )
                )

            # -------*******------- Insert Data in 'pnr_details' table -------*******-------
            
            try:

                # get inserted PNR row
                inserted_pnr_row = cur.fetchone()
                # get PNR ID
                pnr_id = inserted_pnr_row['id']
                # get data map
                sql_pnr_details_data_map = self.prepare_pnr_details_data_map_list(request=request)

                # insert data in pnr details table for every individual passenger
                for SQLpnrDetails in sql_pnr_details_data_map:
                    # Field Count => 19
                    cur.execute(
                        "INSERT INTO pnr_details(pnr_id, passenger_name_number, passenger_given_name, passenger_surname, passenger_email, passenger_contact, passenger_dob, passenger_gender, passenger_type, passport_number, passport_issuing_country, passport_nationality_country, passport_expiration_date, visa_number, visa_applicable_country, visa_place_of_birth, visa_place_of_issue, visa_issue_date, visa_expiration_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                        (
                            pnr_id,
                            SQLpnrDetails.get("passenger_name_number", None),
                            SQLpnrDetails.get("passenger_given_name", None),
                            SQLpnrDetails.get("passenger_surname", None),
                            SQLpnrDetails.get("passenger_email", None),
                            SQLpnrDetails.get("passenger_contact", None),
                            SQLpnrDetails.get("passenger_dob", None),
                            SQLpnrDetails.get("passenger_gender", None),
                            SQLpnrDetails.get("passenger_type", None),
                            SQLpnrDetails.get("passport_number", None),
                            SQLpnrDetails.get("passport_issuing_country", None),
                            SQLpnrDetails.get("passport_nationality_country", None),
                            SQLpnrDetails.get("passport_expiration_date", None),
                            SQLpnrDetails.get("visa_number", None),
                            SQLpnrDetails.get("visa_applicable_country", None),
                            SQLpnrDetails.get("visa_place_of_birth", None),
                            SQLpnrDetails.get("visa_place_of_issue", None),
                            SQLpnrDetails.get("visa_issue_date", None),
                            SQLpnrDetails.get("visa_expiration_date", None)
                        )
                    )

                    # Commit each pnr_details transaction
                    # con.commit()

                # Commit the whole pnr_details transaction
                con.commit()

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed to insert Data in 'pnr_details' Table!"
                    )
                )

            # -------*******------- Insert Data in 'pnr_carrier_code_stats' table -------*******-------

            try:
                # Get Number of PNRs for the carrier
                cur.execute(
                    "SELECT * FROM pnr_carrier_code_stats WHERE carrier_code='{}'".format(
                        sql_pnr_data_map.get("carrier_code", None)
                    )
                )

                carrier_data = cur.fetchone()

                if carrier_data is not None:
                    # assign number_of_pnrs
                    number_of_pnrs = carrier_data["number_of_pnrs"]
                    # assign pnr_list
                    carrier_pnr_list = carrier_data["pnr_list"]
                    carrier_pnr_list.append(sql_pnr_data_map.get("pnr_no", None))

                    if number_of_pnrs >= 0:
                        try:
                            number_of_pnrs = number_of_pnrs + 1
                            # Update Existing carrier information
                            cur.execute(
                                "UPDATE pnr_carrier_code_stats SET number_of_pnrs='{}', pnr_list='{}' WHERE carrier_code='{}'".format(
                                    number_of_pnrs,
                                    json.dumps(carrier_pnr_list),
                                    sql_pnr_data_map.get("carrier_code", None)
                                )
                            )
                            # Commit the whole pnr_carrier_code_stats transaction
                            con.commit()
                        except Exception as E:
                            raise Exception(
                                get_exception_message(
                                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                        0][2],
                                    msg="Failed to update Data in 'pnr_carrier_code_stats' Table!"
                                )
                            )
                else:
                    try:
                        number_of_pnrs = 1
                        carrier_pnr_list = json.dumps([sql_pnr_data_map.get("pnr_no", None)])
                        # insert data in pnr details table for every individual passenger
                        # Field Count => 3
                        cur.execute(
                            "INSERT INTO pnr_carrier_code_stats(carrier_code, number_of_pnrs, pnr_list) values(%s,%s,%s);",
                            (
                                sql_pnr_data_map.get("carrier_code", None),
                                number_of_pnrs,
                                carrier_pnr_list
                            )
                        )

                        # Commit the whole pnr_carrier_code_stats transaction
                        con.commit()

                    except Exception as E:
                        raise Exception(
                            get_exception_message(
                                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                    0][2],
                                msg="Failed to insert Data in 'pnr_carrier_code_stats' Table!"
                            )
                        )

            except Exception as E:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                            0][2],
                        msg="Failed Database trtansaction in 'pnr_carrier_code_stats' table!"
                    )
                )
            
            # Commit the whole transaction
            # con.commit()

            # close connection
            con.close()

            # return pnr id
            return pnr_id
        
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to insert Data in Database!"
                )
            )
