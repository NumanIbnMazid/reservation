"""
File for handling common stuffs of Skytrip Library
"""


class SkyTripCommon():
    __app_signature = "SKYTRIP WEB"

    available_passenger_types = [
        "ADT", "CNN", "INF"
    ]

    def get_app_signature(self):
        """
        get_app_signature() => Getter method for getting App Signature
        """
        return self.__app_signature