# import necessary libraries and modules
from skytrip.utils.helper import get_exception_message
import inspect

# structure adapter class
class SabreRevalidateStructureAdapter:
    """
    SabreRevalidateStructureAdapter => Structures the Sabre Revalidate Itinerary Module"s Response data in SkyTrip Standard format
    """
    # define root node placeholder
    __root_node = None
    # define child nodes placeholder
    common_child_node_list = ["scheduleDescs", "fareComponentDescs", "baggageAllowanceDescs", "legDescs"]
    scheduleDescs, fareComponentDescs, baggageAllowanceDescs, legDescs, itineraries = None, None, None, None, None
    # define extracted reference parent node"s placeholder
    extracted_scheduleDescs, extracted_fareComponentDescs,  extracted_baggageAllowanceDescs, extracted_legDescs = None, None, None, None
    # define itineraries node in structure
    itineraries_node_in_structure = None

    # StructureAdapter constructor
    def __init__(self, response, revalidate_response_structure, require_utils=True):
        # set response
        self.response = response
        # set revalidate response structure
        self.revalidate_response_structure = revalidate_response_structure
        self.require_utils = require_utils

    # Main build method
    def build_structure(self):
        """
        build_structure() => Main build method.
        Returns Structured Response (object).
        """
        structured_response = None

        try:
            # set root node from response
            self.set_root_node()
            # set child node from response
            self.set_child_nodes(child_nodes=self.common_child_node_list)
            # extract reference parent nodes
            self.extract_reference_parent_nodes(extract_nodes=self.common_child_node_list)
            # set itineraries node in structure
            self.set_itineraries_node_in_structure()
            # get structured response
            structured_response = self.assign_nodes_to_structure()

        except Exception as E:
            if type(self.__root_node) == dict and self.__root_node["statistics"].get("itineraryCount", None) < 1:
                structured_response = self.__root_node
            else:
                raise Exception(
                    get_exception_message(
                        Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=f"Failed to build structure!"
                    )
                )
            
        # return final structured response
        return structured_response

    def set_root_node(self):
        """
        set_root_node() => Setter method to set root node of sabre response.
        """
        # set main root node
        self.__root_node = self.response["body"]["responseData"].get("groupedItineraryResponse", {})

    def set_child_nodes(self, child_nodes=None):
        """
        set_child_nodes(*child_nodes=list) => Setter method to set child nodes of sabre response.
        """
        # loop through child nodes
        for node in child_nodes:
            # define node variable matching node placeholder
            node_var = "self." + node
            # set child nodes to node placeholder
            exec("%s = %s" % (node_var, self.__root_node.get(node, [])))

        self.itineraries = self.__root_node["itineraryGroups"][0].get("itineraries", [])

    def set_itineraries_node_in_structure(self):
        """
        set_itineraries_node_in_structure() => Setter method to set main itinerary node of SkyTrip Standard Structure
        """
        # get standard structure
        structure = self.get_structure()
        # set itinerary node
        self.itineraries_node_in_structure = structure["body"]["responseData"].get("Itineraries", [])

    def assign_nodes_to_structure(self):
        """
        assign_nodes_to_structure() => Assigns structured response to SkyTrip structure.
        return => structured response (object).
        """
        # get structure
        structure = self.get_structure()
        # assign nodes
        # assign response status code to structure
        structure["statusCode"] = self.response.get("statusCode", "")
        structure["body"]["token"] = self.response["body"].get("token", "")
        # assign messages
        structure["body"]["responseData"]["Messages"] = self.__root_node.get(
            "messages", []
        )
        # assign itinerary count
        structure["body"]["responseData"]["Statistics"]["ItineraryCount"] = self.__root_node["statistics"].get(
            "itineraryCount", 0
        )
        # generate leg description
        self.generate_leg_description(structure=structure)
        # generate itinerary
        self.generate_itinerary(itineraries_list=self.itineraries)
        # assign itinerary node to structure
        structure["body"]["responseData"]["Itineraries"] = self.itineraries_node_in_structure
        # check if requires utils data
        if self.require_utils == True:
            # assign utils to structure
            structure["body"]["UTILS"]["Sabre"] = self.response["body"].get("responseData", {})
        else:
            del structure["body"]["UTILS"]
        # return synchronized structure
        return structure

    def extract_reference_parent_nodes(self, extract_nodes=None):
        """
        extract_reference_parent_nodes(*extract_nodes=list) => Sets and extracts reference parent nodes.
        """
        # loop through extract nodes
        for node in extract_nodes:
            # generate variables matching extracted placeholders
            extracted_var = "self.extracted_" + node
            # extract parent nodes and assign to extracted placeholders
            exec("%s = %s" % (extracted_var, dict((e["id"], x) for x, e in enumerate(self.__root_node[node]))))

    def get_structure(self):
        """
        get_structure() => Gets SkyTrip Standard Ticket revalidate Response Structure.
        return => structure (object)
        """
        # define structure
        structure = self.revalidate_response_structure
        # return structure
        return structure

    def generate_leg_description(self, structure={}):
        """
        generate_leg_description(*structure=object) => Generates leg description from sabre response
        """
        # iterate through sabre response leg description
        for leg_description in self.__root_node["itineraryGroups"][0]["groupDescription"].get("legDescriptions", []):
            # assign single leg description to structure
            structure["body"]["responseData"]["LegDescription"].append(
                {
                    "DepartureDate": leg_description.get("departureDate", ""),
                    "DepartureLocation": leg_description.get("departureLocation", ""),
                    "ArrivalLocation": leg_description.get("arrivalLocation", "")
                }
            )

    def generate_itinerary(self, itineraries_list=None):
        """
        generate_itinerary(*itineraries_list=list) => Generates structured itineraries from sabre itineraries
        """
        # loop through itineraries list
        for itinerary in itineraries_list:
            # generate schedules
            generated_schedules = self.generate_schedules(itinerary_legs=itinerary.get("legs", []))
            # generate passenger info
            generated_passenger_infos = self.generate_passenger_infos(
                passenger_info_list=itinerary["pricingInformation"][0]["fare"].get("passengerInfoList", [])
            )
            # Total fare is getting from pricing information -> fare
            totalFare = itinerary["pricingInformation"][0]["fare"].get("totalFare", {})
            # assign formatted itineraries
            formatted_itineraries = {
                "ID": itinerary.get("id", ""),
                "GDS": "Sabre",
                "ScheduleDescription": generated_schedules,
                "PassengerInfo": generated_passenger_infos,
                # "TotalFare": {
                #     "FareCurrency": totalFare.get("currency", ""),
                #     "TotalFare": totalFare.get("totalPrice", ""),
                #     "BaseFare": totalFare.get("baseFareAmount", ""),
                #     "Tax": totalFare.get("totalTaxAmount", ""),
                #     "TaxCurrency": totalFare.get("currency", ""),
                # }
                "TotalFare": totalFare
            }

            # Add formatted itinerary to itineraries node in structure
            self.itineraries_node_in_structure.append(formatted_itineraries)

    def generate_schedules(self, itinerary_legs=None):
        """
        generate_schedules(*itinerary_legs=list) => Generates structured schedules from itinerary legs
        return => schedules (list)
        """
        # Define schedules placeholder
        schedules = []
        for leg in itinerary_legs:
            # Leg item where leg description reference available
            # Check if leg is not missing in leg description
            if leg.get("ref", "") in self.extracted_legDescs:
                # Iterate schedules if leg description not empty
                for schedule_ref in self.legDescs[self.extracted_legDescs[leg["ref"]]].get("schedules", []):
                    # schedule item which is declared in leg description
                    # Check if referenced schedule item in schedule description
                    if schedule_ref.get("ref", "") in self.extracted_scheduleDescs:
                        # Iterate schedules to generate custom schedule info list
                        schedule = self.scheduleDescs[self.extracted_scheduleDescs[schedule_ref.get("ref", "")]]
                        # Add newly formatted schedule in schedule list
                        # Add a dictionary object by defining keys and values dynamically
                        schedules.append(
                            {
                                "NoOfStoppage": schedule.get("stopCount", ""),
                                "ETicketable": schedule.get("eTicketable", ""),
                                "TotalDistanceInMiles": schedule.get("totalMilesFlown", ""),
                                "Departure": {
                                    "Airport": schedule["departure"].get("airport", ""),
                                    "City": schedule["departure"].get("city", ""),
                                    "Country": schedule["departure"].get("country", ""),
                                    "Time": schedule["departure"].get("time", ""),
                                    "Terminal": schedule["departure"].get("terminal", ""),
                                    "DateAdjustment": schedule_ref.get("departureDateAdjustment", 0)
                                },
                                "Arrival": {
                                    "Airport": schedule["arrival"].get("airport", ""),
                                    "City": schedule["arrival"].get("city", ""),
                                    "Country": schedule["arrival"].get("country", ""),
                                    "Time": schedule["arrival"].get("time", ""),
                                    "Terminal": schedule["arrival"].get("terminal", ""),
                                    "DateAdjustment": schedule["arrival"].get("dateAdjustment", 0)
                                },
                                "Carrier": {
                                    "OperatingCarrierCode": schedule["carrier"].get("operating", ""),
                                    "OperatingFlightNumber": schedule["carrier"].get("operatingFlightNumber", ""),
                                    "MarketingCarrierCode": schedule["carrier"].get("marketing", ""),
                                    "MarketingFlightNumber": schedule["carrier"].get("marketingFlightNumber", "")
                                }
                            }
                        )
        # return structured schedules
        return schedules

    def generate_passenger_infos(self, passenger_info_list=None):
        """
        generate_passenger_infos(*passenger_info_list=list) => Generates structured schedules from itinerary legs
        return => passenger_infos (list)
        """
        # Define passenger info placeholder
        passenger_infos = []
        # Iterate into passenger info list for this itinerary  to format passenger information
        for passenger in passenger_info_list:
            # generate fare descriptions
            generated_fare_descriptions = self.generate_fare_descriptions(passenger_obj=passenger)
            # generate baggage infos
            generated_baggage_info_list = self.generate_baggage_infos(passenger_obj=passenger)
            # generate passenger total fare
            generated_passenger_total_fare = self.generate_passenger_total_fare(passenger_obj=passenger)
            # get passenger info node
            passenger_info = passenger.get("passengerInfo", {})
            # insert generated nodes in passenger infos
            passenger_infos.append(
                {
                    "PassengerType": passenger_info.get("passengerType", ""),
                    "PassengerNumber": passenger_info.get("passengerNumber", ""),
                    "NonRefundable": passenger_info.get("nonRefundable", ""),
                    "FareDescription": generated_fare_descriptions,
                    "BaggageDescription": generated_baggage_info_list,
                    "PassengerTotalFare": generated_passenger_total_fare
                }
            )
        # return structured passenger infos
        return passenger_infos

    def generate_fare_descriptions(self, passenger_obj=None):
        """
        generate_fare_descriptions(*passenger_obj=object) => Generates structured fare descriptions from passenger info
        return => fare_descriptions (list)
        """
        # define fare description placeholder
        fare_descriptions = []
        # Loop into fare components to get and set fare info in formatted way
        for fare in passenger_obj["passengerInfo"].get("fareComponents", []):
            # Define segments placeholder
            segments = []
            # Loop into segments to set formatted segment from fare
            for segment in fare.get("segments", {}):
                # check if segment node exists
                if segment.get("segment", None) is not None:
                    # Add segment to segments list to set segments for this fare
                    segments.append(
                        {
                            "CabinClass": self.get_cabin_class(cabin_class=segment["segment"].get("cabinCode", "")),
                            "SeatsAvailable": segment["segment"].get("seatsAvailable", ""),
                            "BookingCode": segment["segment"].get("bookingCode", ""),
                            "MealCode": segment["segment"].get("mealCode", "")
                        }
                    )
                else:
                    # insert original segment node
                    segments.append(segment)
            # Check if referenced fare is exists in fare component description list
            if fare.get("ref", "") in self.extracted_fareComponentDescs:
                # Store referenced component
                component = self.fareComponentDescs[self.extracted_fareComponentDescs[fare.get("ref", {})]]
                # Add component values, segments in fare description in a formatted way
                fare_descriptions.append(
                    {
                        "NotValidAfter": component.get("notValidAfter", ""),
                        "NotValidBefore": component.get("notValidBefore", ""),
                        "Segment": segments
                    }
                )
        # return fare descriptions
        return fare_descriptions

    def get_cabin_class(self, cabin_class=""):
        """
        get_cabin_class(*cabin_class=string) => Translates Sabre Cabin Code to Standard SkyTrip format
        return => Cabin Code (string)
        """
        # define result placeholder
        result = ""
        # map cabin classes
        cabin_class_map = {
            "P": "Premium First",
            "F": "First",
            "J": "Premium Business",
            "C": "Business",
            "S": "Premium Economy",
            "Y": "Economy"
        }
        # loop through cabin class map
        for cabin_code, formatted_class in cabin_class_map.items():
            # check if sabre cabin code matches with the mapped cabin code
            if cabin_class == cabin_code:
                # assign cabin code in standard format
                result = formatted_class
        # return the result
        return result
        

    def generate_baggage_infos(self, passenger_obj=None):
        """
        generate_baggage_infos(*passenger_obj=object) => Generates structured fare descriptions from passenger info
        return => baggage_info_list (list)
        """
        # Define baggage info placeholder
        baggage_info_list = []
        # Loop into passenger info -> baggage info to get and set baggage
        for baggage in passenger_obj["passengerInfo"].get("baggageInformation", []):
            # Check if referenced baggage is available in baggage allowance list
            if baggage["allowance"].get("ref", "") in self.extracted_baggageAllowanceDescs:
                # Assign referenced baggage allowance to allowance variable
                allowance = self.baggageAllowanceDescs[
                    self.extracted_baggageAllowanceDescs[baggage["allowance"].get("ref", "")]
                ]
                # Add formatted baggage info in baggage info list
                baggage_info_list.append(
                    {
                        "NumberOfPieces": allowance.get("pieceCount", ""),
                        "MaxWeight": allowance.get("weight", ""),
                        "Unit": allowance.get("unit", "")
                    }
                )
        # return baggage infos
        return baggage_info_list

    def generate_passenger_total_fare(self, passenger_obj=None):
        """
        generate_passenger_total_fare(*passenger_obj=object) => Generates passenger total fare
        return => passenger_total_fare (object)
        """
        # Passenger fare node for this passenger
        passenger_fare = passenger_obj["passengerInfo"].get("passengerTotalFare", {})
        # Format passenger fare for adding it to passenger info
        # passenger_total_fare = {
        #     "TotalFare": passenger_fare.get("totalFare", ""),
        #     "TotalTaxAmount": passenger_fare.get("totalTaxAmount", ""),
        #     "Currency": passenger_fare.get("currency", ""),
        #     "BaseFareAmount": passenger_fare.get("baseFareAmount", ""),
        #     "BaseFareCurrency": passenger_fare.get("baseFareCurrency", "")
        # }
        passenger_total_fare = passenger_fare
        # return passenger total fare object
        return passenger_total_fare
