
# skytrip ticket Issue config class

class IssueConfig():
    lniata_code = "4F44A9"
    ticket_country_code = "BD"

    def get_ticket_issue_request_structure(self):
        """
        get_ticket_issue_request_structure() => gets sabre ticket issue structure
        return => object (sabre ticket issue structure object)
        """
        structure = {
            "AirTicketRQ": {
                "version": "1.2.1",
                "targetCity": "",
                "DesignatePrinter": None,
                "Itinerary": {
                    "ID": ""
                },
                "Ticketing": [],
                "PostProcessing": {
                    "EndTransaction": {
                        "Source": {
                            "ReceivedFrom": ""
                        }
                    }
                }
            }
        }

        return structure
