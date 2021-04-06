
# skytrip ticket revalidate config class

class RevalidateConfig:
    # class variables for ticket revalidate
    passenger_types_to_skip_count = ["INF"]
    requestor_id_company_code = "TN"

    def get_skytrip_revalidate_itinerary_response_standard_structure(self):
        """
        Getter method for getting standard structure for skytrip revalidate response
        return => object
        """
        structure = {
            "statusCode": None,
            "body": {
                "token": None,
                "responseData": {
                    "Messages": [],
                    "Statistics": {
                        "ItineraryCount": ""
                    },
                    "LegDescription": [],
                    "Itineraries": []
                },
                "UTILS": {
                    "Sabre": None,
                    "Galileo": None,
                    "Amadeous": None
                }
            }
        }
        return structure


    def get_revalidate_request_structure(self):
        """
        get_revalidate_request_structure() => returns revalidate itinerary Request Structure.
        """
        structure = {
            "OTA_AirLowFareSearchRQ": {
                "OriginDestinationInformation": [],
                "POS": {
                    "Source": [
                        {
                            "PseudoCityCode": "",
                            "RequestorID": {
                                "CompanyName": {
                                    "Code": ""
                                },
                                "ID": "1",
                                "Type": "1"
                            }
                        }
                    ]
                },
                "TPA_Extensions": {
                    "IntelliSellTransaction": {
                        "RequestType": {
                            "Name": "200ITINS"
                        }
                    }
                },
                "TravelPreferences": {
                    "TPA_Extensions": {
                        "DataSources": {
                            "ATPCO": "Enable",
                            "LCC": "Disable",
                            "NDC": "Disable"
                        },
                        "NumTrips": {}
                    }
                },
                "TravelerInfoSummary": {
                    "AirTravelerAvail": [
                        {
                            "PassengerTypeQuantity": []
                        }
                    ],
                    "SeatsRequested": []
                },
                # "AvailableFlightsOnly": True,
                # "DirectFlightsOnly": True,
                "Version": "1"
            }
        }
        return structure
