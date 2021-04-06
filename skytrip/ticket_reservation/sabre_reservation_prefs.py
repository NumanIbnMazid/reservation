# import necessary libraries and modules
from skytrip_config.config import SkyTripConfig
from skytrip_config.gds_config import SabreConfig
from skytrip.utils.common import SkyTripCommon
from skytrip.ticket_reservation.reservation_config import ReservationConfig
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from skytrip.utils.helper import get_exception_message
import inspect
import datetime


class SabreReservationPrefs:

    __skytrip_conf = SkyTripConfig()
    __sabre_conf = SabreConfig()
    __skytrip_common = SkyTripCommon()
    __reservation_config = ReservationConfig()

    # App Vars
    number_of_passengers = 0

    def __init__(self):
        self.reservation_request_stucture = self.__reservation_config.get_reservation_request_structure()
        self.insert_node = self.reservation_request_stucture.get(
            "CreatePassengerNameRecordRQ", {})

    def calculate_age(self, dob):
        """
        calculate_age() => Calculates age from date of birth
        params => dob (date of birth)
        """
        today = datetime.date.today()
        dob = dob
        age = relativedelta(today, dob)

        return {
            "year": age.years,
            "month": age.months,
            "day": age.days,
            "all_month": (age.years * 12) + age.months
        }

    def struct_person_name(self, elements=[], node=[]):
        """
        struct_agency_info() => Structure Agency Info.
        """
        # define initial name reference and given name
        for idx, element in enumerate(elements):
            # define initial is infant placeholder
            is_infant = False

            if element.get("DateOfBirth", "") and element.get("Gender", ""):
                age = self.calculate_age(dob=parse(
                    element.get("DateOfBirth", "")
                ))

                gender = element.get('Gender', "")

                if age['year'] < self.__reservation_config.age_limit_inf:
                    is_infant = True
                    given_name = element.get("GivenName", "") + \
                        (" MSTR" if gender == "M" else " MISS")
                    name_reference = "I%s" % (age['all_month'] if len(
                        str(age['all_month'])) > 1 else "0" + str(age['all_month']))
                elif age['year'] < self.__reservation_config.age_limit_cnn:
                    given_name = element.get("GivenName", "") + \
                        (" MSTR" if gender == "M" else " MISS")
                    name_reference = "C%s" % (age['year'] if len(
                        str(age['year'])) > 1 else "0" + str(age['year']))
                elif age['year'] >= self.__reservation_config.age_limit_cnn:
                    given_name = element.get("GivenName", "") + \
                        (" MR" if gender == "M" else " MRS")
                    name_reference = ""
                else:
                    given_name = element.get("GivenName", "")
                    name_reference = ""
            else:
                missing_params = []
                required_params = {
                    "DateOfBirth": element.get("DateOfBirth", None),
                    "Gender": element.get("Gender", None),
                }
                message = ""
                for key, value in required_params.items():
                    if value is None:
                        missing_params.append(key)
                if len(missing_params) >= 1:
                    message = f"Missing Parameter(s): 'PersonName' => {missing_params}"

                raise Exception(
                    get_exception_message(
                        Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=message
                    )
                )

            target_insertion_node = {
                "NameNumber": element.get("NameNumber", "") if element.get("NameNumber", None) is not None else str(idx + 1) + ".1",
                "Infant": is_infant,
                "NameReference": name_reference,
                "PassengerType": element.get("PassengerType", ""),
                "GivenName": given_name,
                "Surname": element.get("Surname", "")
            }

            exec("self.insert_node" + node + ".append(target_insertion_node)")

    def struct_air_price(self, elements=[], node=[]):
        """
        struct_air_price() = > Structure Air Price Node based on passenger type.
        params => elements (passenger type objects), node (air price insertion node)
        """
        # exec("self.insert_node" + node + " = None")
        # exec("self.insert_node" + node + " = elements")

        # define initial passenger types
        passenger_types = []

        for idx, passenger in enumerate(elements):
            # if passenger.get("Code", "") in self.__skytrip_common.available_passenger_types and passenger.get("Code", "") not in self.__reservation_config.passenger_types_to_skip_count:
            if passenger.get("Code", "") in self.__skytrip_common.available_passenger_types:

                if passenger.get("Code", "") not in passenger_types:
                    # insert new passenger types to list
                    passenger_types.append(passenger.get("Code", None))

                    air_price_node = {
                        "PriceRequestInformation": {
                            "Retain": True,
                            "OptionalQualifiers": {
                                "FOP_Qualifiers": {
                                    "BasicFOP": {
                                        "Type": self.__reservation_config.basic_fop_type
                                    }
                                },
                                "PricingQualifiers": {
                                    "PassengerType": [
                                        {
                                            "Code": passenger.get("Code", ""),
                                            "Quantity": str(passenger.get("Quantity", ""))
                                        }
                                    ]
                                }
                            }
                        }
                    }
                    if passenger.get("PassengerTotalFare", 0) >= 1:
                        air_price_node["PriceComparison"] = {
                            "AmountSpecified": passenger.get("PassengerTotalFare", 0)
                        }
                    # insert single node into target insertion node
                    exec("self.insert_node" + node + ".append(air_price_node)")

    # struct node base
    def struct_node(self, elements=[], node=[]):
        """
        struct_node() => Structs Dynamic Nodes.
        """
        exec("self.insert_node" + node + " = None")
        exec("self.insert_node" + node + " = elements")

    def calculate_and_set_number_of_passengers(self, passengerObj):
        """
        calculate_and_set_number_of_passengers() => calculates total number of passengers based on passenger object.
        params => obj (passenger object)
        """
        if passengerObj.get("PassengerType", "") in self.__skytrip_common.available_passenger_types:
            if passengerObj.get("PassengerType", "") not in self.__reservation_config.passenger_types_to_skip_count:
                self.number_of_passengers += int(
                    passengerObj.get("PassengerNumber", "0")
                )
        else:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Invalid passenger type given! Available passenger types are {self.__skytrip_common.available_passenger_types}. Passenger type given : {passengerObj.get('PassengerType', '')}"
                )
            )

    def prepare_initial_request_body_data(self, RequestBody={}):
        """
        prepare_initial_request_body_data() => Preapares request body data
        Param: (RequestBody*) => containing user input values and existed token.
        """
        try:
            def calculate_date(date=None, increment=0):
                converted_date = datetime.datetime.strptime(
                    date, "%Y-%m-%d").date()
                return converted_date + datetime.timedelta(days=increment)

            def convert_utc_to_iso_datetime(date=None, utc_time=None):
                parsed_datetime = parse(date + " " + utc_time)
                iso_formatted_datetime = parsed_datetime.isoformat()
                formatted_datetime = iso_formatted_datetime[:-6]
                return formatted_datetime

            def get_booking_date_time(previous=7, departure_datetime=datetime.datetime.today()):
                result = datetime.datetime.now()
                return result.strftime("%Y-%m-%dT%H:%M:%S")

            def get_name_ref(element=None, prefix={"INF": "I", "CNN": "C"}, suffix=None, ageFirst=False, dob=None, gender=None):
                """
                get_name_ref() => Get Passenger Name Reference.
                """
                if dob is not None and gender is not None:
                    __reservation_config = ReservationConfig()
                    age = self.calculate_age(dob=parse(dob))

                    if age['year'] < __reservation_config.age_limit_inf:
                        given_name = element.get("GivenName", "") + \
                            (" MSTR" if gender == "M" else " MISS")
                        name_reference = "{0}{1}" if ageFirst == False else "{1}{0}".format(prefix.get("INF", ""), age['all_month'] if len(
                            str(age['all_month'])) > 1 else "0" + str(age['all_month']))
                    elif age['year'] < __reservation_config.age_limit_cnn:
                        given_name = element.get("GivenName", "") + \
                            (" MSTR" if gender == "M" else " MISS")
                        name_reference = "{0}{1}" if ageFirst == False else "{1}{0}".format(prefix.get("CNN", ""), age['year'] if len(
                            str(age['year'])) > 1 else "0" + str(age['year']))
                    elif age['year'] >= __reservation_config.age_limit_cnn:
                        given_name = element.get("GivenName", "") + \
                            (" MR" if gender == "M" else " MRS")
                        name_reference = ""
                    else:
                        given_name = element.get("GivenName", "")
                        name_reference = ""

                    return {
                        "GivenName": given_name,
                        "NameReference": name_reference
                    }
                else:
                    missing_params = []
                    required_params = {
                        "DateOfBirth": element.get("DateOfBirth", None),
                        "Gender": element.get("Gender", None),
                    }
                    message = ""
                    for key, value in required_params.items():
                        if value is None:
                            missing_params.append(key)
                    if len(missing_params) >= 1:
                        message = f"Missing Parameter(s): 'PersonName' => {missing_params}"

                    raise ValueError(
                        get_exception_message(
                            Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                0][2],
                            msg=message
                        )
                    )

            # define inital cabin class
            cabin_class = None
            # define initial departure datetime
            departure_datetime = None
            # define initial variables
            assigned_date = ""
            ClassOfService = ""
            booking_codes = []
            passenger_types = []
            passeger_insert_node = []
            secure_flight_insert_node = []
            service_insert_node = []
            # define initial passenger name number index
            num_index = -1
            adult_passenger_name_numbers = []
            passIndexCounter = 0

            # get Schedule Description from response
            ScheduleDescription = RequestBody["TargetItinerary"].get(
                "ScheduleDescription", [])
            # get PassengerInfo from response
            PassengerInfo = RequestBody["TargetItinerary"].get(
                "PassengerInfo", [])

            # Get origin destination information from request
            OriginDestinationInformation_Insert_Node = []
            OriginDestinationInformation = RequestBody.get(
                "OriginDestinationInformation", [])

            # get LegDescription
            LegDescription = RequestBody.get("LegDescription", [])

            # define initial schedule index to track the schedule break point
            scheduleIndex = 0

            # ------------------- Generate ClassOfService -------------------
            for idx, SinglePassenger in enumerate(PassengerInfo):
                # get booking codes
                if idx == 0:
                    for fareDescription in SinglePassenger.get("FareDescription", []):
                        if type(fareDescription.get("Segment", None)) == list:
                            for segment in fareDescription.get("Segment", []):
                                booking_codes.append(
                                    segment.get("BookingCode", ""))

            # ------------------- Generate Passenger Information -------------------

            # Store adult passenger name numbers into list
            for idx, element in enumerate(RequestBody.get("PersonName", [])):
                # store adult passenger name numbers to use in service for INFANT Message
                if element.get("PassengerType", None) == "ADT":
                    adult_passenger_name_numbers.append(
                        element.get("NameNumber", None))

            for idx, info in enumerate(RequestBody["TargetItinerary"].get(
                "PassengerInfo", []
            )):
                # Update total passenger quantity
                self.calculate_and_set_number_of_passengers(passengerObj=info)

                # get booking codes
                if idx == 0:
                    for fareDescription in info.get("FareDescription", []):
                        if type(fareDescription.get("Segment", None)) == list:
                            for segment in fareDescription.get("Segment", []):
                                booking_codes.append(
                                    segment.get("BookingCode", ""))

                # loop according to passenger number
                for passenger_index in range(0, int(info.get("PassengerNumber", 1))):
                    # passenger info
                    if info.get("PassengerType", "") not in passenger_types:
                        # insert new passenger types
                        passenger_types.append(info.get("PassengerType", None))
                        single_passenger_info = {
                            "Code": info.get("PassengerType", ""),
                            "Quantity": str(info.get("PassengerNumber", "")),
                            "PassengerTotalFare": info["PassengerTotalFare"].get("TotalFare", 0)
                        }
                        passeger_insert_node.append(single_passenger_info)

                    # ------------------- Generate Service -------------------
                    if info.get("PassengerType", "") == "INF":
                        # name reference ex: 3INFT
                        inf_name_ref = get_name_ref(
                            element=RequestBody.get("PersonName", [])[passIndexCounter], prefix={'INF': 'INFT', 'CNN': 'CNN'}, ageFirst=True, dob=RequestBody.get("PersonName", [])[passIndexCounter].get("DateOfBirth", ""), gender=RequestBody.get("PersonName", [])[passIndexCounter].get("Gender", "")
                        ).get("NameReference", "")

                        # date of birth ex: 02JUN19
                        datetime_obj = parse(RequestBody.get("PersonName", [])[
                                             passIndexCounter].get("DateOfBirth", ""))
                        formatted_date = datetime_obj.strftime(
                            "%d%b%y").upper()

                        gender_title = "MSTR" if RequestBody.get("PersonName", [])[passIndexCounter].get(
                            "Gender", "") == "M" else "MISS"

                        # adult name number field ex: 1.1
                        adult_passenger_name_number = None
                        if len(adult_passenger_name_numbers) >= 1:
                            # Insert Adult Passenger Name Number Node in Infant passenger info node
                            if passenger_index + 1 <= len(adult_passenger_name_numbers):
                                adult_passenger_name_number = adult_passenger_name_numbers[
                                    passenger_index]
                            else:
                                adult_passenger_name_number = adult_passenger_name_numbers[-1]

                        else:
                            raise Exception(
                                get_exception_message(
                                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                                        0][2],
                                    msg="There's no adult passenger found! Requires at least 1 adult passenger."
                                )
                            )

                        inf_single_service = {
                            "SSR_Code": "INFT",
                            "Text": f"{RequestBody.get('PersonName', [])[passIndexCounter].get('GivenName', '').upper()}/{RequestBody.get('PersonName', [])[passIndexCounter].get('Surname', '').upper()} {gender_title}/{formatted_date}",
                            "PersonName": {
                                "NameNumber": adult_passenger_name_number
                            },
                        }
                        # insert into service node
                        service_insert_node.append(inf_single_service)

                    if info.get("PassengerType", "") == "CNN":
                        # date of birth ex: 02JUN19
                        datetime_obj = parse(RequestBody.get("PersonName", [])[
                                             passIndexCounter].get("DateOfBirth", ""))
                        formatted_date = datetime_obj.strftime(
                            "%d%b%y").upper()
                        cnn_single_service = {
                            "SSR_Code": "CHLD",
                            "Text": formatted_date,
                            "PersonName": {
                                "NameNumber": RequestBody.get("PersonName", [])[passIndexCounter].get("NameNumber", "")
                            }
                        }
                        # insert into service node
                        service_insert_node.append(cnn_single_service)

                    passIndexCounter += 1

            for PersonName in RequestBody.get("PersonName", []):
                # ------------------- Generate Secure Flight -------------------
                single_secure_flight = {
                    "PersonName": {
                        "NameNumber": PersonName.get("NameNumber", ""),
                        "GivenName": PersonName.get("GivenName", ""),
                        "Surname": PersonName.get("Surname", ""),
                        "DateOfBirth": PersonName.get("DateOfBirth", ""),
                        "Gender": PersonName.get("Gender", "")
                    },
                    "SegmentNumber": "A",
                    "VendorPrefs": {
                        "Airline": {
                            "Hosted": False
                        }
                    }
                }
                secure_flight_insert_node.append(single_secure_flight)

            # ------------------- Generate Additional Service -------------------
            for Service in RequestBody.get("Service", []):
                service_insert_node.append(Service)

            # ------------------- Generate Origin Destination Informnation -------------------

            for index, OriginDestination in enumerate(OriginDestinationInformation):
                # define Flight insertion node
                Flight = []
                # loop through schedule description
                for idx in range(scheduleIndex, len(ScheduleDescription) + 1):

                    for leg in LegDescription:
                        if ScheduleDescription[idx]["Departure"].get("Airport", "") == leg.get("DepartureLocation", ""):
                            assigned_date = leg.get("DepartureDate", "")

                    # Assign main ClassOfService
                    ClassOfService = booking_codes[index]

                    # departure temp datetime
                    departure_temp_datetime = calculate_date(
                        date=assigned_date, increment=ScheduleDescription[idx]["Departure"].get(
                            "DateAdjustment", 0))
                    # get departure datetime
                    departure_datetime = convert_utc_to_iso_datetime(
                        date=str(departure_temp_datetime), utc_time=ScheduleDescription[idx]["Departure"].get("Time", ""))
                    # get arrival datetime
                    arrival_datetime = convert_utc_to_iso_datetime(
                        date=str(calculate_date(date=str(departure_temp_datetime),
                                                increment=ScheduleDescription[idx]["Arrival"].get(
                            "DateAdjustment", 0))),
                        utc_time=ScheduleDescription[idx]["Arrival"].get(
                            "Time", "")
                    )

                    # assign departure_datetime for booking date
                    if idx == 0:
                        departure_datetime_root = departure_temp_datetime

                    OriginDestinationInformation_Insert_Node.append({
                        "DepartureDateTime": str(departure_datetime),
                        "ArrivalDateTime": str(arrival_datetime),
                        "FlightNumber": str(ScheduleDescription[idx]["Carrier"].get("MarketingFlightNumber", "")),
                        "NumberInParty": str(self.number_of_passengers),
                        "ResBookDesigCode": ClassOfService,
                        "Status": "NN",
                        "OriginLocation": {
                            "LocationCode": ScheduleDescription[idx]["Departure"].get("Airport", "")
                        },
                        "DestinationLocation": {
                            "LocationCode": ScheduleDescription[idx]["Arrival"].get("Airport", "")
                        },
                        "MarketingAirline": {
                            "Code": ScheduleDescription[idx]["Carrier"].get("MarketingCarrierCode", ""),
                            "FlightNumber": str(ScheduleDescription[idx]["Carrier"].get("MarketingFlightNumber", ""))
                        }
                    })

                    # increment schedule index
                    scheduleIndex += 1

                    # dynamically manage assigned date
                    if str(departure_datetime)[:10] != assigned_date:
                        assigned_date = str(departure_datetime)[:10]
                    if str(arrival_datetime)[:10] != assigned_date:
                        assigned_date = str(arrival_datetime)[:10]

                    # crossmatch logic (millionire logic) => check if Leg Destination matches Schedule Destination
                    if OriginDestination["DestinationLocation"].get("LocationCode", None) in [ScheduleDescription[idx]["Arrival"].get("Airport", ""), ScheduleDescription[idx]["Arrival"].get("City", "")]:
                        # break the loop if arrives to destination
                        break

            # Preapare Initial Request Body Data
            InitialRequestBodyData = {
                "ContactNumber": RequestBody.get("ContactNumber", []),
                "Email": RequestBody.get("Email", []),
                "PersonName": RequestBody.get("PersonName", []),
                "FlightSegment": OriginDestinationInformation_Insert_Node,
                "PassengerType": passeger_insert_node,
                "AdvancePassenger": RequestBody.get("AdvancePassenger", []),
                "SecureFlight": secure_flight_insert_node,
                "Service": service_insert_node,
            }

            return InitialRequestBodyData

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to generate initial request body data!"
                )
            )

    # search preference function
    def get_reservation_preference(self, RequestBody=None):
        """
        Generate reservation preferences (request body) based on user inputs
        Param: (RequestBody*) => containing user input values and existed token.
        """
        try:
            # prepare initial request body data
            InitialRequestBodyData = self.prepare_initial_request_body_data(
                RequestBody=RequestBody)

            self.struct_node(
                elements=self.__sabre_conf.get_PCC(), node='["targetCity"]'
            )
            # Insert Agency Info
            agency_info = self.__skytrip_conf.get_agency_info()
            agency_info["Ticketing"] = {
                "TicketType": self.__reservation_config.TicketType
            }
            self.struct_node(
                elements=agency_info, node='["TravelItineraryAddInfo"]["AgencyInfo"]'
            )
            # get contact numbers
            ContactNumber = InitialRequestBodyData.get("ContactNumber", [])
            # struct contact numbers
            self.struct_node(
                elements=ContactNumber, node='["TravelItineraryAddInfo"]["CustomerInfo"]["ContactNumbers"]["ContactNumber"]'
            )
            # get email
            Email = InitialRequestBodyData.get("Email", [])
            # struct contact numbers
            self.struct_node(
                elements=Email, node='["TravelItineraryAddInfo"]["CustomerInfo"]["Email"]'
            )
            # get person names
            PersonNames = InitialRequestBodyData.get("PersonName", [])
            self.struct_person_name(
                elements=PersonNames, node='["TravelItineraryAddInfo"]["CustomerInfo"]["PersonName"]'
            )
            # get flight segments
            FlightSegments = InitialRequestBodyData.get("FlightSegment", [])
            self.struct_node(
                elements=FlightSegments, node='["AirBook"]["OriginDestinationInformation"]["FlightSegment"]'
            )
            # struct air price
            PassengerType = InitialRequestBodyData.get("PassengerType", [])
            self.struct_air_price(
                elements=PassengerType, node='["AirPrice"]'
            )

            # get advance passenger segments
            AdvancePassenger = InitialRequestBodyData.get(
                "AdvancePassenger", [])
            self.struct_node(
                elements=AdvancePassenger, node='["SpecialReqDetails"]["SpecialService"]["SpecialServiceInfo"]["AdvancePassenger"]'
            )

            # struct secure flight
            SecureFlight = InitialRequestBodyData.get("SecureFlight", [])
            self.struct_node(
                elements=SecureFlight, node='["SpecialReqDetails"]["SpecialService"]["SpecialServiceInfo"]["SecureFlight"]'
            )

            # get service segments
            Service = InitialRequestBodyData.get("Service", [])
            self.struct_node(
                elements=Service, node='["SpecialReqDetails"]["SpecialService"]["SpecialServiceInfo"]["Service"]'
            )

            # construct post processing
            self.struct_node(
                elements=self.__skytrip_common.get_app_signature(), node='["PostProcessing"]["EndTransaction"]["Source"]["ReceivedFrom"]'
            )

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to generate reservation preference!"
                )
            )

        # return structed reservation structure
        return self.reservation_request_stucture
