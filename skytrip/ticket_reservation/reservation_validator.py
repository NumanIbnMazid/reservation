from skytrip.ticket_reservation.reservation_config import ReservationConfig
from skytrip.utils.common import SkyTripCommon
from skytrip.utils.helper import get_exception_message
import inspect


def validate_reservation_request(EventBodyData=None):
    """
    validate_reservation_request() => Validates Reservation Request Body.
    params => EventBodyData (request body)
    return => validated_request (Validated request Body)
    """

    __reservation_config = ReservationConfig()
    __skytrip_common = SkyTripCommon()
    result = {}

    try:
        # validate if exists user ID
        if EventBodyData.get("UserID", None) is None:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="UserID is required! Pass user ID with the request parameter."
                )
            )
        # validate if exists Data Source
        if EventBodyData.get("DataSource", None) is None:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="DataSource is required! Pass DataSource with the request parameter. // Available Options: 'B2C', 'B2B_AGENT', 'B2B_ADMIN' //"
                )
            )
        # validate if exists transaction ID
        if not EventBodyData.get("DataSource", None) in ["B2B", "B2B_AGENT", "B2B_ADMIN"] and EventBodyData.get("TransactionID", None) is None:
            raise ValueError(
                get_exception_message(
                    Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="TransactionID is required! Pass TransactionID with the request parameter."
                )
            )
        # validate flight segment
        FlightSegment = EventBodyData["RequestBody"].get("FlightSegment", [])
        for flight in FlightSegment:
            if flight["MarketingAirline"].get("Code", "") in __reservation_config.inactive_airlines:
                raise ValueError(
                    get_exception_message(
                        Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=f"Airline '{flight['MarketingAirline'].get('Code', '')}' is in inactive airlines configuration."
                    )
                )

        # sort passenger infos start
        passenger_sort_queue = __skytrip_common.available_passenger_types

        try:
            # get PassengerInfo from response
            PassengerInfo = EventBodyData["RequestBody"]["TargetItinerary"].get(
                "PassengerInfo", []
            )

            passenger_dict_tracker = {}
            sorted_passenger_info_list = []

            passenger_loop_index_tracker = 0

            for key in PassengerInfo:
                passenger_dict_tracker[key["PassengerType"]
                                       ] = passenger_loop_index_tracker
                passenger_loop_index_tracker += 1

            for key in passenger_sort_queue:
                if key in passenger_dict_tracker:
                    sorted_passenger_info_list.append(
                        PassengerInfo[passenger_dict_tracker[key]])

            for key in PassengerInfo:
                if key not in sorted_passenger_info_list:
                    sorted_passenger_info_list.append(key)

            # update event body data person name
            EventBodyData["RequestBody"]["TargetItinerary"]["PassengerInfo"] = sorted_passenger_info_list

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to sort Passenger Info!"
                )
            )

        # sort passenger infos end

        # sort person names start
        try:
            person_dict_tracker = {}
            sorted_PersonNames = []

            for idx, element in enumerate(EventBodyData["RequestBody"].get("PersonName", [])):

                # define passenger name number
                if element.get("NameNumber", None) is None:
                    element["NameNumber"] = str(idx + 1) + ".1"

                if element.get("PassengerType", None) in person_dict_tracker.keys():
                    person_dict_tracker[element.get(
                        "PassengerType", None)].append(idx)
                else:
                    person_dict_tracker[element.get(
                        "PassengerType", None)] = [idx]

            for key in passenger_sort_queue:
                if key in person_dict_tracker.keys():
                    for idx, element in enumerate(person_dict_tracker[key]):
                        sorted_PersonNames.append(
                            EventBodyData["RequestBody"].get(
                                "PersonName", [])[element]
                        )

            for key in EventBodyData["RequestBody"].get("PersonName", []):
                if key not in sorted_PersonNames:
                    sorted_PersonNames.append(key)

            # update event body data person name
            EventBodyData["RequestBody"]["PersonName"] = sorted_PersonNames

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to sort Person Name!"
                )
            )
        # sort person names ends

        # validate advance passenger
        for idx, advance_passenger in enumerate(EventBodyData["RequestBody"].get("AdvancePassenger", [])):
            EventBodyData["RequestBody"]["AdvancePassenger"][idx]["PersonName"]["GivenName"] = advance_passenger["PersonName"].get(
                "GivenName", "").replace(" ", "")
            EventBodyData["RequestBody"]["AdvancePassenger"][idx]["PersonName"]["Surname"] = advance_passenger["PersonName"].get(
                "Surname", "").replace(" ", "")

        # validate secure flight
        for idx, secure_flight in enumerate(EventBodyData["RequestBody"].get("SecureFlight", [])):
            EventBodyData["RequestBody"]["SecureFlight"][idx]["PersonName"]["GivenName"] = secure_flight["PersonName"].get(
                "GivenName", "").replace(" ", "")
            EventBodyData["RequestBody"]["SecureFlight"][idx]["PersonName"]["Surname"] = secure_flight["PersonName"].get(
                "Surname", "").replace(" ", "")

        # assign request body to result
        result = EventBodyData

    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to validate reservation request body!"
            )
        )

    # return final result
    return result
