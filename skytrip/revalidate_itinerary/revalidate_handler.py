# import necessary modules and libraries
from skytrip.revalidate_itinerary.sabre_revalidate_prefs import SabreRevalidatePrefs
from skytrip.gds_handler import SabreHandler
from skytrip.revalidate_itinerary.sabre_revalidate_structure_adapter import SabreRevalidateStructureAdapter
from skytrip.revalidate_itinerary.revalidate_config import RevalidateConfig
from skytrip.utils.helper import generate_json, get_root_exception_message, finalize_response
import inspect


class RevalidateHandler:
    # initialize default if requires utils
    require_utils = False
    # create sabre handler instance
    __sabre_handler = SabreHandler()
    # sabre revalidate preference
    __sabre_revalidate_prefs = SabreRevalidatePrefs()

    def __init__(self, EventBodyData=None):
        self.event_body_data = EventBodyData

    # handler function
    def sabre_revalidate_handler(self, generateJSON=False):
        """
        revalidate handler for Revalidate Itinerary Module
        params => generateJSON (boolean)
        """
        # define main response placeholder
        sabre_response = None
        result = None

        try:
            # ------------------- *** get main response from Sabre *** -------------------
            # get main response from sabre
            sabre_response = self.__sabre_handler.get_sabre_response(
                EventBodyData=self.event_body_data, request_pref_func=self.__sabre_revalidate_prefs.get_revalidate_preference, endpoint_identifier='v6.shop.flights.revalidate', generateJSON=generateJSON
            )

            # ------------------- *** adopt Sabre response with Skytrip standard structure *** -------------------
            # ticket revalidate response structure
            __revalidate_config = RevalidateConfig()
            revalidate_response_structure = __revalidate_config.get_skytrip_revalidate_itinerary_response_standard_structure()
            # get if requires utils
            self.require_utils = self.event_body_data.get("RequireUTILS", False)
            # Adopt structure
            structure_adapter = SabreRevalidateStructureAdapter(
                response=sabre_response, revalidate_response_structure=revalidate_response_structure, require_utils=self.require_utils
            )
            # get structured revalidate response
            result = structure_adapter.build_structure()
            
        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            # assign exceptions to result
            result = get_root_exception_message(
                Ex=E, gdsResponse=sabre_response, appResponse=result, file=__file__,
                parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to revalidate itinerary!"
            )
        
        # ------------------- *** validate structure and finalize response *** -------------------
        finalized_response = finalize_response(response=result)

        # ------------------- *** generate JSON file of Skytrip structured response *** -------------------
        if generateJSON == True:
            generate_json(
                gds="sabre", isReq=False, filename="revalidate_structured_response_sabre.json", data=finalized_response
            )

        # return finalized response
        return finalized_response