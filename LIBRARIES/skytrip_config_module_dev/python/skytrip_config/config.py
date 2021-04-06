
# Skytrip Configuration Class
class SkyTripConfig:
    # ------- define if in production or certification -------
    __is_production = False

    # ------- database definations -------
    db_name = "example_db"
    db_host = "example_db_host.com"
    db_port = "1234"
    db_user = "example"
    db_password = "example"

    def get_is_production(self):
        """
        Getter method for getting if the site is in production mode or not
        return => boolean
        """
        return self.__is_production

    def get_agency_info(self):
        AddressLine = "Skytrip"
        CityName = "Dhaka"
        CountryCode = "BD"
        PostalCode = "1234"
        StateCode = ""
        StreetNmbr = "Example Address"

        # prepare agency data
        agency_data = {
            "Address": {
                "AddressLine": AddressLine,
                "CityName": CityName,
                "CountryCode": CountryCode,
                "PostalCode": PostalCode,
                "StateCountyProv": {
                    "StateCode": StateCode
                },
                "StreetNmbr": StreetNmbr
            }
        }
        return agency_data
