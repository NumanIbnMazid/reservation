
# skytrip ticket reservation config class

class ReservationConfig:

    # fop config
    basic_fop_type = "INV"
    # agency Config
    TicketType = "7TAW"
    # age limit config
    age_limit_inf = 2
    age_limit_cnn = 12
    # passenger type config
    passenger_types_to_skip_count = ["INF"]
    # Airline Config
    inactive_airlines = ["FZ"]

    def get_reservation_request_structure(self):
        """
        get_reservation_request_structure() => returns PNR Search Request Structure.
        """
        structure = {
            "CreatePassengerNameRecordRQ": {
                "version": "2.3.0",
                "targetCity": "",
                "haltOnAirPriceError": False,
                "TravelItineraryAddInfo": {
                    "AgencyInfo": {},
                    "CustomerInfo": {
                        "ContactNumbers": {
                            "ContactNumber": []
                        },
                        "Email": [],
                        "PersonName": []
                    }
                },
                "AirBook": {
                    "HaltOnStatus": [
                        {
                            "Code": "HL"
                        },
                        {
                            "Code": "KK"
                        },
                        {
                            "Code": "LL"
                        },
                        {
                            "Code": "NN"
                        },
                        {
                            "Code": "NO"
                        },
                        {
                            "Code": "UC"
                        },
                        {
                            "Code": "US"
                        }
                    ],
                    "OriginDestinationInformation": {
                        "FlightSegment": []
                    },
                    "RedisplayReservation": {
                        "NumAttempts": 10,
                        "WaitInterval": 300
                    }
                },
                "AirPrice": [],
                "SpecialReqDetails": {
                    # "AddRemark": {
                    #     "RemarkInfo": {
                    #         "FOP_Remark": {
                    #             "Type": ""
                    #         }
                    #     }
                    # },
                    "SpecialService": {
                        "SpecialServiceInfo": {
                            "AdvancePassenger": [],
                            "SecureFlight": [],
                            "Service": []
                        }
                    }
                },
                "PostProcessing": {
                    # "ARUNK": {},
                    "EndTransaction": {
                        "Source": {
                            "ReceivedFrom": ""
                        }
                    },
                    "RedisplayReservation": {
                        "waitInterval": 100
                    }
                }
            }
        }
        # return structure
        return structure
