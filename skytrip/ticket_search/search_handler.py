# import necessary modules and libraries
from skytrip.ticket_search.sabre_search_prefs import SabreSearchPrefs
from skytrip.gds_handler import SabreHandler
from skytrip.ticket_search.sabre_structure_adapter import SabreStructureAdapter
from skytrip.ticket_search.search_config import SearchConfig
from skytrip.utils.helper import generate_json, get_root_exception_message, finalize_response
import inspect


class SearchHandler:
    # initialize default if requires utils
    require_utils = False
    # create sabre handler instance
    __sabre_handler = SabreHandler()
    # sabre search preference
    __sabre_search_prefs = SabreSearchPrefs()

    def __init__(self, EventBodyData=None):
        self.event_body_data = EventBodyData

    # handler function
    def sabre_search_handler(self, generateJSON=False):
        """
        Search handler for BFM (Bargain Finder Max) Module
        params => generateJSON (boolean)
        """
        # define main response placeholder
        sabre_response = None
        result = None

        try:
            # ------------------- *** get main response from Sabre *** -------------------
            # get main response from sabre
            sabre_response = self.__sabre_handler.get_sabre_response(
                EventBodyData=self.event_body_data, request_pref_func=self.__sabre_search_prefs.get_search_preference, endpoint_identifier='v1.offers.shop', generateJSON=generateJSON
            )

            # ------------------- *** adopt Sabre response with Skytrip standard structure *** -------------------
            # ticket search response structure
            __search_config = SearchConfig()
            search_response_structure = __search_config.get_skytrip_ticket_search_response_standard_structure()
            # get if requires utils
            self.require_utils = self.event_body_data.get("RequireUTILS", False)
            # Adopt structure
            structure_adapter = SabreStructureAdapter(
                response=sabre_response, search_response_structure=search_response_structure, require_utils=self.require_utils
            )
            # get structured search response
            result = structure_adapter.build_structure()
        
        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            # assign exceptions to result
            result = get_root_exception_message(
                Ex=E, gdsResponse=sabre_response, appResponse=result, file=__file__, 
                parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to fetch search result!"
            )
        
        # ------------------- *** validate structure and finalize response *** -------------------
        finalized_response = finalize_response(response=result)

        # ------------------- *** generate JSON file of Skytrip structured response *** -------------------
        if generateJSON == True:
            generate_json(
                gds="sabre", isReq=False, filename="search_structured_response_sabre.json", data=finalized_response
            )
            
        # return finalized response
        return finalized_response
