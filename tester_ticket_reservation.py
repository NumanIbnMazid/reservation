from skytrip.ticket_reservation.reservation_handler import ReservationHandler
import json
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import random
import string
from tester_helper import get_token, manage_book_info_json
from skytrip.ticket_reservation.reservation_config import ReservationConfig


true = True
false = False

# load req body util data
req_body_util_JSON = "UTILS/JSON_STORE/req-body-util.json"
req_body_util_data = None
with open(req_body_util_JSON) as f:
    req_body_util_data = json.load(f)

# json_dir = "Req_Res_Samples/responses/sabre/search_structured_response_sabre.json"
json_dir = "Req_Res_Samples/responses/sabre/revalidate_structured_response_sabre.json"
final_json_file = "UTILS/JSON_STORE/reservation-tester-requestBody.json"

response_data = None

with open(json_dir) as f:
  response_data = json.load(f)


def calculate_age(dob=None):
    """
    calculate_age() => Calculates age from date of birth
    params => dob (date of birth)
    """
    today = datetime.date.today()
    age = relativedelta(today, parse(dob))

    return {
        "year": age.years,
        "month": age.months,
        "day": age.days,
        "all_month": (age.years * 12) + age.months
    }


def generate_random_string(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_random_number(size=4, chars='1234567890'):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_date(startYear=2021, endYear=2023):
    start_date = datetime.date(startYear, 1, 1)
    end_date = datetime.date(endYear, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    random_date = start_date + datetime.timedelta(days=random_number_of_days)

    return random_date


def generate_random_name(gender="M", shortname=False):
    first_male = ("JAMES", "JOHN", "ROBERT", "MICHAEL", "WILLIAM", "DAVID", "RICHARD", "CHARLES", "JOSEPH", "THOMAS",
                  "CHRISTOPHER", "DANIEL", "PAUL", "MARK", "DONALD", "GEORGE", "KENNETH", "STEVEN", "EDWARD", "BRIAN", "ANTHONY")
    first_female = ("MARY", "PATRICIA", "LINDA", "BARBARA", "ELIZABETH", "JENNIFER", "MARIA", "SUSAN", "MARGARET", "DOROTHY",
                    "LISA", "NANCY", "BETTY", "HELEN", "SANDRA", "DONNA", "CAROL", "RUTH", "SHARON", "MICHELLE", "LAURA")

    last = ("SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER", "WILSON", "MOORE", "TAYLOR",
                   "ANDERSON", "THOMAS", "JACKSON", "WHITE", "HARRIS", "MARTIN", "THOMPSON", "GARCIA", "MARTINEZ")

    if gender == "M":
        first_name = random.choice(first_male)
    else:
        first_name = random.choice(first_female)

    last_name = random.choice(last)
    
    if shortname == True:
        return last_name
    else:
        full_name = (first_name + " " + last_name)
        return full_name


def generate_birth_date(passenger_type=None):
    try:
        date_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                        14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        age = 0
        if passenger_type == "ADT":
            age = 30
        if passenger_type == "CNN":
            age = 10
        if passenger_type == "INF":
            age = 1

        cur_date, dateOnly, replacedDate, parsedBirthdate, birthdate = None, None, None, None, None

        cur_date = datetime.datetime.now()
        dateOnly = str(cur_date)[0:10]
        randomDate = str(random.choice(date_choices))
        yearMonth = dateOnly[:8]
        time = str(cur_date)[10:]

        replacedDate = yearMonth + randomDate + time

        parsedBirthdate = parse(replacedDate)

        birthdate = parsedBirthdate - datetime.timedelta(days=age*365)
        return birthdate
        
    except Exception as E:
        raise Exception(
            f"***Error*** (tester_ticket_reservation.py) => generate_birth_date() : failed to generate birth date! \n[cur_date: {cur_date}, dateOnly: {dateOnly}, randomDate: {randomDate}, yearMonth: {yearMonth}, time: {time}, replacedDate: {replacedDate}, parsedBirthdate: {parsedBirthdate}, birthdate: {birthdate}].\n Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
        )


passenger_types_to_skip_count = ["INF"]

response_root = response_data["body"].get("responseData", "")

itineraries = response_root.get("Itineraries", [])

target_itinerary = {}

skip_airlines = ["FZ"]
specific_airline_code = "BG"

# Specify itinerary
# target_itinerary_id = 1
target_itinerary_id = itineraries[0].get("ID", None)
disallow_connected = False
specific_airline = False
only_definedID_airline = True
requireSpecialService = False

for itinerary in itineraries:
    if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") not in skip_airlines:
        if disallow_connected == True:
            if len(itinerary.get("ScheduleDescription", [])) == 1:
                if specific_airline == True:
                    if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") == specific_airline_code:
                        target_itinerary_id = itinerary.get("ID", "")
                        target_itinerary = itinerary
                elif only_definedID_airline == True:
                    if itinerary.get("ID", 0) == target_itinerary_id:
                        target_itinerary_id = itinerary.get("ID", "")
                        target_itinerary = itinerary
                else:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
        else:
            if specific_airline == True:
                if itinerary["ScheduleDescription"][0]["Carrier"].get("MarketingCarrierCode", "") == specific_airline_code:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
            elif only_definedID_airline == True:
                if itinerary.get("ID", 0) == target_itinerary_id:
                    target_itinerary_id = itinerary.get("ID", "")
                    target_itinerary = itinerary
            else:
                target_itinerary_id = itinerary.get("ID", "")
                target_itinerary = itinerary

# ---------------------- main node generation ----------------------

try:

    # Configure Passenger Info
    passenger_infos = target_itinerary.get("PassengerInfo", [])
    contact_number_insert_node = []
    email_insert_node = []
    person_name_insert_node = []
    advance_passenger_insert_node = []
    service_insert_node = []

    # define initial passenger name number index
    num_index = -1

    for idx, info in enumerate(passenger_infos):
        # loop according to passenger number
        for passenger_index in range(0, int(info.get("PassengerNumber", 1))):

            num_index += 1

            # generate name number
            name_number = str(num_index + 1) + ".1"


            # generate short name and full name
            full_name = generate_random_name(gender="M" if num_index % 2 == 0 else "F")
            short_name = generate_random_name(gender="M" if num_index % 2 == 0 else "F", shortname=True)
            date_of_birth = str(generate_birth_date(passenger_type=info.get("PassengerType", "")).strftime("%Y-%m-%d"))
            gender = "M" if num_index % 2 == 0 else "F"

            if info.get("PassengerType", "") not in passenger_types_to_skip_count:
                # contact number
                single_contact_number = {
                    "NameNumber": name_number,
                    "Phone": str(generate_random_number(size=13)),
                    "PhoneUseType": "H"
                }
                contact_number_insert_node.append(single_contact_number)
                # email
                single_email = {
                    "NameNumber": name_number,
                    "Address": f"{short_name.lower()}@gmail.com"
                }
                email_insert_node.append(single_email)

            # person name
            single_person_name = {
                "NameNumber": name_number,
                "NameReference": "ABC123",
                "PassengerType": info.get("PassengerType", ""),
                # "GivenName": f"{info.get("PassengerType", "")} Passenger" + str(idx + 1),
                "GivenName": full_name,
                "Surname": short_name,
                "DateOfBirth": date_of_birth,
                "Gender": gender
            }
            person_name_insert_node.append(single_person_name)
            # advance_passenger
            single_advance_passenger = {
                # "Document": {
                #     "Number": "1234567890",
                #     "Visa": {
                #         "ApplicableCountry": "UAE",
                #         "PlaceOfBirth": "Dhaka",
                #         "PlaceOfIssue": "Dhaka",
                #         "IssueDate": "2018-09-18"
                #     },
                #     "Type": "V"
                # },
                "Document": {
                    "Number": generate_random_string(size=3).upper() + generate_random_number(5),
                    "IssueCountry": "BGD",
                    "NationalityCountry": "BGD",
                    "ExpirationDate": str(generate_random_date(startYear=2021, endYear=2023)),
                    "Type": "P"
                },
                # "Document": {
                #     "Number": generate_random_number(9),
                #     "IssueCountry": "BGD",
                #     "NationalityCountry": "BGD",
                #     "ExpirationDate": "2022-09-17",
                #     "Type": "I"
                # },
                "PersonName": {
                    "NameNumber": name_number,
                    "GivenName": full_name,
                    "MiddleName": "",
                    "Surname": short_name,
                    "DateOfBirth": date_of_birth,
                    "Gender": gender,
                },
                "SegmentNumber": "A"
            }
            advance_passenger_insert_node.append(single_advance_passenger)

            # generate service
            if requireSpecialService == True:
                if num_index == 0:
                    single_service = {
                        "PersonName": {
                            "NameNumber": name_number
                        },
                        "SegmentNumber": "A",
                        "SSR_Code": "WCHC",
                        "Text": "UNABLE TO WALK",
                        "VendorPrefs": {
                            "Airline": {
                                "Hosted": false
                            }
                        }
                    }
                    service_insert_node.append(single_service)


except Exception as E:
    raise Exception(
        f"***Error*** (tester_ticket_reservation.py) : An Exception Occured! Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
    )


data = {
    "ExistedToken": get_token(),
    "UserID": 1,
    "TransactionID": "8e931621-ecda-4296-a7ce-82eef53098d4",
    "DataSource": "B2C",
    "Utils": {
        "ExampleData": "Example Utils Data"
    },
    "RequestLOG": false,
    "RequestBody": {
        "ContactNumber": contact_number_insert_node,
        "Email": email_insert_node,
        "PersonName": person_name_insert_node,
        "AdvancePassenger": advance_passenger_insert_node,
        "Service": service_insert_node,
        "OriginDestinationInformation": req_body_util_data["ticket_search"].get("OriginDestinationInformation", []),
        "LegDescription": req_body_util_data["ticket_search"].get("LegDescription", []),
        "TargetItinerary": target_itinerary
    }
}


# Generate JSON
with open(final_json_file, "w") as outfile:
    target_req_body_data = {
        "RequestBody": data,
        "TargetItineraryID": target_itinerary_id,
        "LegDescription": req_body_util_data["ticket_search"].get("LegDescription", []),
        "TargetItinerary": target_itinerary
    }
    json.dump(target_req_body_data, outfile, indent=4)


event_body = data


def moduleRunner(testWithWhile=False, runAmount=7):
    """
    moduleRunner() => Skytrip Module Runner Function.
    params: testWithWhile (Boolean, default=False), runAmount (integer, default=7)
    """
    if testWithWhile == True:
        i = 0
        while i <= runAmount:
            modulehandler = ReservationHandler(EventBodyData=event_body)
            response = modulehandler.sabre_reservation_handler(
                generateJSON=True)
            print(f"\n {'*' * 50} Reservation Response Data {'*' * 50} : \n\n",
                  response, "\n\n")
            i += 1
    else:
        modulehandler = ReservationHandler(EventBodyData=event_body)
        response = modulehandler.sabre_reservation_handler(generateJSON=True)
        print(f"\n {'*' * 50} Reservation Response Data {'*' * 50} : \n\n",
              response, "\n\n")
    # return the response
    return response


# get actual response
response = moduleRunner(testWithWhile=False, runAmount=5)


try:
    # Update Book Info JSON File
    if response["body"]["responseData"]["CreatePassengerNameRecordRS"]["ApplicationResults"].get("status", None) == "Complete":
        # manage Book Info JSON
        manage_book_info_json(
            pnr_ID=response["body"]["responseData"]["CreatePassengerNameRecordRS"]["ItineraryRef"].get("ID", None),
            response=response,
            info_node_name="PASSENGER NAME RECORD INFO",
            detail_node_name="PASSENGER NAME RECORD DETAIL",
        )
except Exception as E:
    raise Exception(
        f"***Error*** (tester_ticket_reservation.py) : Failed to manage book info json file! Exception Type: {str(E.__class__.__name__)}. Arguments: [{str(E)}]"
    )
