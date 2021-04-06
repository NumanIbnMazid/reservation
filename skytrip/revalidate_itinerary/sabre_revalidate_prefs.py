# import necessary libraries and modules
from skytrip_config.gds_config import SabreConfig
from skytrip.revalidate_itinerary.revalidate_config import RevalidateConfig
from skytrip.utils.common import SkyTripCommon
from skytrip.utils.helper import get_exception_message
import inspect
import datetime
from dateutil.parser import parse


# Sabre revalidate Prefs Class
class SabreRevalidatePrefs:
    seats_requested = 0
    __sabre_conf = SabreConfig()
    __revalidate_conf = RevalidateConfig()
    __skytrip_common = SkyTripCommon()

    def calculate_and_set_SeatsRequested(self, passengerObj):
        """
        calculate_SeatsRequested() => calculates total seats requested based on passenger type quantity.
        params => obj (passenger type quantity object)
        """
        if passengerObj.get("Code", "") in self.__skytrip_common.available_passenger_types:
            if passengerObj.get("Code", "") not in self.__revalidate_conf.passenger_types_to_skip_count:
                self.seats_requested += int(passengerObj.get("Quantity", "0"))
        else:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg=f"Invalid Passenger Type Code given: {passengerObj.get('Code', None)}! Available passenger type codes that configured in Skytrip are: {self.__skytrip_common.available_passenger_types}"
                )
            )

    def prepare_initial_request_body_data(self, RequestBody={}):
        """
        prepare_initial_request_body_data() => Preapares request body data
        Param: (RequestBody*) => containing user input values and existed token.
        """
        try:
            def calculate_date(date=None, increment=0):
                converted_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                return converted_date + datetime.timedelta(days=increment)

            def convert_utc_to_iso_datetime(date=None, utc_time=None):
                parsed_datetime = parse(date + " " + utc_time)
                iso_formatted_datetime = parsed_datetime.isoformat()
                formatted_datetime = iso_formatted_datetime[:-6]
                return formatted_datetime

            def get_booking_date_time(previous=7, departure_datetime=datetime.datetime.today()):
                result = datetime.datetime.now()
                return result.strftime("%Y-%m-%dT%H:%M:%S")

            # define inital cabin class
            cabin_class = None
            # define initial departure datetime
            departure_datetime = None
            # define initial variables
            assigned_date = ""
            ClassOfService = ""
            booking_codes = []

            # get Schedule Description from response
            ScheduleDescription = RequestBody["TargetItinerary"].get("ScheduleDescription", [])
            # get PassengerInfo from response
            PassengerInfo = RequestBody["TargetItinerary"].get("PassengerInfo", [])

            # Get origin destination information from request
            OriginDestinationInformation_Insert_Node = []
            OriginDestinationInformation = RequestBody.get("OriginDestinationInformation", [])

            # get LegDescription
            LegDescription = RequestBody.get("LegDescription", [])

            # define initial schedule index to track the schedule break point
            scheduleIndex = 0

            # ------------------- Generate ClassOfService Solution One -------------------
            for idx, SinglePassenger in enumerate(PassengerInfo):
                # get booking codes
                if idx == 0:
                    for fareDescription in SinglePassenger.get("FareDescription", []):
                        if type(fareDescription.get("Segment", None)) == list:
                            for segment in fareDescription.get("Segment", []):
                                booking_codes.append(segment.get("BookingCode", ""))

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
                        utc_time=ScheduleDescription[idx]["Arrival"].get("Time", "")
                    )

                    # assign departure_datetime for booking date
                    if idx == 0:
                        departure_datetime_root = departure_temp_datetime

                    Flight.append({
                        "Number": ScheduleDescription[idx]["Carrier"].get("OperatingFlightNumber", ""),
                        "DepartureDateTime": departure_datetime,
                        "ArrivalDateTime": arrival_datetime,
                        "Type": "A",
                        "ClassOfService": ClassOfService,
                        "OriginLocation": {
                            "LocationCode": ScheduleDescription[idx]["Departure"].get("Airport", "")
                        },
                        "DestinationLocation": {
                            "LocationCode": ScheduleDescription[idx]["Arrival"].get("Airport", "")
                        },
                        "Airline": {
                            "Operating": ScheduleDescription[idx]["Carrier"].get("OperatingCarrierCode", ""),
                            "Marketing": ScheduleDescription[idx]["Carrier"].get("MarketingCarrierCode", "")
                        },
                        "BookingDateTime": str(get_booking_date_time(previous=7, departure_datetime=departure_datetime_root))
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

                # assign flight to origin destination
                OriginDestination["Flight"] = Flight
                # insert into node
                OriginDestinationInformation_Insert_Node.append(OriginDestination)

            # ------------------- Passenger Informnation -------------------
            PassengerTypeQuantity_Insert_Node = []

            # get Schedule Description from response
            PassengerInfo = RequestBody["TargetItinerary"].get("PassengerInfo", [])

            for Passenger in PassengerInfo:
                PassengerTypeQuantity_Insert_Node.append(
                    {
                        "Code": Passenger.get("PassengerType", ""),
                        "Quantity": Passenger.get("PassengerNumber", None)
                    }
                )
            InitialRequestBodyData = {
                "OriginDestinationInformation": OriginDestinationInformation_Insert_Node,
                "PassengerTypeQuantity": PassengerTypeQuantity_Insert_Node,
                "TicketClass": ClassOfService,
                "DirectFlightsOnly": RequestBody.get("DirectFlightsOnly", {}),
                "AvailableFlightsOnly": RequestBody.get("AvailableFlightsOnly", {})
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

    # revalidate preference function
    def get_revalidate_preference(self, RequestBody={}):
        """
        Generate revalidate preferences (request body) based on user inputs
        Param: (RequestBody*) => containing user input values and existed token.
        """
        # define base structure of revalidate data
        request_structure = self.__revalidate_conf.get_revalidate_request_structure()

        try:
            
            # prepare initial request body data
            InitialRequestBodyData = self.prepare_initial_request_body_data(RequestBody=RequestBody)

            # ------ prepare revalidate data ------
            insert_node = request_structure["OTA_AirLowFareSearchRQ"]
            # ------ configure pseudo city code ------
            insert_node["POS"]["Source"][0]["PseudoCityCode"] = self.__sabre_conf.get_PCC()
            # ------ configure company name ------
            insert_node["POS"]["Source"][0]["RequestorID"]["CompanyName"]["Code"] = self.__revalidate_conf.requestor_id_company_code
            # prepare origin and destination information
            OriginDestinationInformation = InitialRequestBodyData.get("OriginDestinationInformation", [])
            # loop through origin destination information and insert in node
            for element in OriginDestinationInformation:
                # define initial TPA_Extensions
                element["TPA_Extensions"] = {}
                # get and remove flight node from origin destination information
                if element.get("Flight", None) is not None:
                    element["TPA_Extensions"]["Flight"] = element.get("Flight", [])
                    del element["Flight"]
                else:
                    raise ValueError(
                        get_exception_message(
                            Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                            msg="Missing required parameter(s): 'OriginDestinationInformation' -> 'Flight'"
                        )
                    )
                # insert information in revalidate data
                insert_node["OriginDestinationInformation"].append(element)
            # prepare passenger information data
            PassengerTypeQuantity = InitialRequestBodyData.get("PassengerTypeQuantity", [])
            # loop through PassengerTypeQuantity and insert in node
            for element in PassengerTypeQuantity:
                self.calculate_and_set_SeatsRequested(passengerObj=element)
                insert_node["TravelerInfoSummary"]["AirTravelerAvail"][0]["PassengerTypeQuantity"].append(element)
            # Insert Seats Requested
            insert_node["TravelerInfoSummary"]["SeatsRequested"].append(self.seats_requested)
            # prepare flight type information data
            if InitialRequestBodyData.get("DirectFlightsOnly", "") != "":
                insert_node["DirectFlightsOnly"] = InitialRequestBodyData.get("DirectFlightsOnly", False)
            if InitialRequestBodyData.get("AvailableFlightsOnly", "") != "":
                insert_node["AvailableFlightsOnly"] = InitialRequestBodyData.get("AvailableFlightsOnly", False)

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to generate revalidate preference!"
                )
            )

        # return the final prepared revalidate data
        return request_structure
