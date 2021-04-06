
# import necessary libraries and modules
from skytrip_config.config import SkyTripConfig
from skytrip_config.gds_config import SabreConfig
from skytrip.utils.common import SkyTripCommon
from skytrip.ticket_issue.issue_config import IssueConfig
from skytrip.utils.helper import get_exception_message
import inspect

# Sabre Ticket Issue Class
class SabreTicketIssuePrefs:
    __skytrip_conf = SkyTripConfig()
    __sabre_conf = SabreConfig()
    __skytrip_common = SkyTripCommon()
    __issue_config = IssueConfig()

    def __init__(self):
        self.ticket_issue_request_structure = self.__issue_config.get_ticket_issue_request_structure()
        self.insert_node = self.ticket_issue_request_structure.get(
            "AirTicketRQ", ""
        )

    def struct_target_city(self):
        """
        struct_target_city() => Structure target City from Sabre PCC
        """
        self.insert_node["targetCity"] = self.__sabre_conf.get_PCC()

    def struct_designate_printer(self):
        """
        struct_designate_printer() => Structure Designate Printer Based on Sabre Preference
        """
        self.insert_node["DesignatePrinter"] = {
            "Printers": {
                "Ticket": {
                    "CountryCode": self.__issue_config.ticket_country_code
                },
                "Hardcopy": {
                    "LNIATA": self.__issue_config.lniata_code
                }
            }
        }

    def struct_itinerary(self, itinID=None):
        """
        struct_itinerary() => Structure Itinerary ID from event body
        params => itinID (Itinerary ID from PNR Response)
        """
        self.insert_node["Itinerary"]["ID"] = itinID

    def struct_ticketing(self):
        """
        struct_ticketing() => Structure ticketing param
        """
        quote = {
            "NameSelect": [
                {
                    "NameNumber": 1
                }
            ],
            "Record": [
                {
                    "Number": 1
                }
            ]
        }
        self.insert_node["Ticketing"].append(
            {
                "PricingQualifiers": {
                    "PriceQuote": [quote]
                }
            }
        )

    def struct_end_transaction_source(self):
        """
        struct_end_transaction_source() => Structure End Transaction Source
        """
        self.insert_node["PostProcessing"]["EndTransaction"]["Source"]["ReceivedFrom"] = self.__skytrip_common.get_app_signature()


    def get_ticket_issue_preference(self, EventBodyData={}):
        """
        get_ticket_issue_preference() => Gets Ticket Issue preference
        params => EventBodyData (Request Body)
        return => generated ticket issue request body
        """
        try:
            # struct target city
            self.struct_target_city()
            # struct designate printer
            self.struct_designate_printer()
            # struct itinerary ID
            self.struct_itinerary(itinID=EventBodyData.get("ItineraryID", ""))
            # struct price quote
            self.struct_ticketing()
            # struct end transaction source
            self.struct_end_transaction_source()
        
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg=f"Failed to generate issue preference!"
                )
            )

        # return structed structure
        return self.ticket_issue_request_structure
