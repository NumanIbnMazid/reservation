# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_skytrip_apis(RequestBody={}):
    """
    get_skytrip_apis() => Retrieves Skytrip APIs from Database.
    params => RequestBody (object)
    """

    def get_api(is_production, api_module_name):
        """
        get_api() => Returns Skytrip API based on production status.
        params => is_production (skytrip production status - Boolean), api_module_name (skytrip api module name - string)
        """
        production_api_map = {
            "GenerateToken": {
                "APIendpoint": "https://s161fi11w4.execute-api.ap-southeast-1.amazonaws.com/default/py_generate_token_prod",
                "APIkey": "ZaSfGSkMvV2TWJPbngZcL13iJisf1Tyo8JJPsS12"
            },
            "TicketSearch": {
                "APIendpoint": "https://5lnzbtmioa.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_search_prod",
                "APIkey": "foZdcVJApp3DBpEHyZ5D4NLF5TB0k358031NGmV7"
            },
            "RevalidateItinerary": {
                "APIendpoint": "https://onylv5m7l2.execute-api.ap-southeast-1.amazonaws.com/default/py_revalidate_itinerary_prod",
                "APIkey": "AfcVJUQytR4DxTfs0p0iY3CRiKCSVebWaaFUxtLa"
            },
            "TicketReservation": {
                "APIendpoint": "https://iqt17us0d9.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_reservation_prod",
                "APIkey": "273jcHrTZs2FHhSEBdEe55ByL9J0tjKC9hI13fDk"
            },
            "TicketIssue": {
                "APIendpoint": "https://rosjdx40c0.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_issue_prod",
                "APIkey": "2zp7wpTsnx1sSp3WbTEKtadeh9zaYgKz8WqJd57L"
            },
            "PaymentDB": {
                "APIendpoint": "https://jg0h9hnixe.execute-api.ap-southeast-1.amazonaws.com/default/py_payment_db",
                "APIkey": "FC4MpbQ6et4LNAEmRxwSm6sA66903prc4SyZDbGL"
            },
            "UserMediaUpload": {
                "APIendpoint": "https://77o9pc56dj.execute-api.ap-southeast-1.amazonaws.com/default/py_user_media",
                "APIkey": "LH7APqGq1t1ZMByBwLzeI85THQaODqa76kDUaM8x"
            },
            "GetUserMedias": {
                "APIendpoint": "https://taik5rzzmk.execute-api.ap-southeast-1.amazonaws.com/default/py_get_user_medias",
                "APIkey": "fbUql8vhiH7cn2c8a2AIZ6HShwzszzu63GyKe8sm"
            },
            "GetMediaDetail": {
                "APIendpoint": "https://0cp84gb2ai.execute-api.ap-southeast-1.amazonaws.com/default/py_get_media_detail",
                "APIkey": "Zsz0NTzAYO5RUk8qRkhIw116uCDxv3ku8A6CwFxc"
            },
            "GetUserPNRs": {
                "APIendpoint": "https://u14i0wjsf6.execute-api.ap-southeast-1.amazonaws.com/default/py_get_user_pnrs",
                "APIkey": "LX7cHCnH6s7dmi1b7IIuH306tSuKsrUt6aaeQQGN"
            },
            "GetPNRdetail": {
                "APIendpoint": "https://c7f2jmgv81.execute-api.ap-southeast-1.amazonaws.com/default/py_get_pnr_detail",
                "APIkey": "k5LXAS4Sdn6sW4JTxGfs35mjm7A2zTP65H0jj4ht"
            },
            "GetVisaInformationList": {
                "APIendpoint": "https://7o8z33m2xe.execute-api.ap-southeast-1.amazonaws.com/default/py_get_visa_information_list",
                "APIkey": "UJmFT7LmLL6E29bIJGwhtaI6gdlzXqzx9bwgip7e"
            },
            "GetVisaInformationDetail": {
                "APIendpoint": "https://h73tsj9ngl.execute-api.ap-southeast-1.amazonaws.com/default/py_get_visa_information_detail",
                "APIkey": "mE5odA1rkv3RGyc2lTp2s5DgXTYVF0xf6AkNR4ub"
            },
            "GetSSLcommerzConfiguration": {
                "APIendpoint": "https://9q97iqfdbc.execute-api.ap-southeast-1.amazonaws.com/default/py_get_ssl_commerz_conf",
                "APIkey": "kSYEJhf7c98ZPjUHFZexG7fXk7AsGpoJ6FuAKNNV"
            },
            "GetApplicationSettings": {
                "APIendpoint": "https://tawyqzh7g8.execute-api.ap-southeast-1.amazonaws.com/default/py_get_application_settings",
                "APIkey": "5fNVuAxZt2ZaZPC0hle950kbZf4NhbD6xXLxI1ii"
            },
            "GetPackageInformationList": {
                "APIendpoint": "https://knmnxx6e0j.execute-api.ap-southeast-1.amazonaws.com/default/py_get_package_information_list",
                "APIkey": "OEApZyi1C45ZgUg5tVAxs408VnzwH6k42KpwIaSC"
            },
            "GetPackageInformationDetail": {
                "APIendpoint": "https://6g1vy7dce7.execute-api.ap-southeast-1.amazonaws.com/default/py_get_package_information_detail",
                "APIkey": "Q9cgT5ONHT2JaW8Vp4Y3e8KEgJD4UEsT89pUgLSS"
            },
            "GetCouponValue": {
                "APIendpoint": "https://4d8vwpwaz7.execute-api.ap-southeast-1.amazonaws.com/default/py_get_coupon_value",
                "APIkey": "3UYR8oDAXh2LDdkeK9Xd9t9L6VZ2CnF4W8o8POLj"
            }
        }
        certification_api_map = {
            "GenerateToken": {
                "APIendpoint": "https://fz37e41g6l.execute-api.ap-southeast-1.amazonaws.com/default/py_generate_token_dev",
                "APIkey": "0aGguD5Yp057NJHyzxq6V8VQTDGQpCCQ8Y2XJEux"
            },
            "TicketSearch": {
                "APIendpoint": "https://ea5wmuwkq3.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_search_dev",
                "APIkey": "ygFntAG0r73uhAywXc8l73d4W2UasrVp8hjKUSyt"
            },
            "RevalidateItinerary": {
                "APIendpoint": "https://qgadi56gq8.execute-api.ap-southeast-1.amazonaws.com/default/py_revalidate_itinerary_dev",
                "APIkey": "VXZ7GbfZ2j1jvJOEwj8M82AYfUFsVXl352iSdF1J"
            },
            "TicketReservation": {
                "APIendpoint": "https://imh8d7avzd.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_reservation_dev",
                "APIkey": "0Wr75iqHgC4VGtC02LR7t8ECr4ZW7WYN8MVGTOSV"
            },
            "TicketIssue": {
                "APIendpoint": "https://65kf8pc7ug.execute-api.ap-southeast-1.amazonaws.com/default/py_ticket_issue_dev",
                "APIkey": "yJ7HX57vGpagis5QSM0vC7jM0O78KT2b6zbHbRSS"
            },
            "PaymentDB": {
                "APIendpoint": "https://jg0h9hnixe.execute-api.ap-southeast-1.amazonaws.com/default/py_payment_db",
                "APIkey": "FC4MpbQ6et4LNAEmRxwSm6sA66903prc4SyZDbGL"
            },
            "UserMediaUpload": {
                "APIendpoint": "https://77o9pc56dj.execute-api.ap-southeast-1.amazonaws.com/default/py_user_media",
                "APIkey": "LH7APqGq1t1ZMByBwLzeI85THQaODqa76kDUaM8x"
            },
            "GetUserMedias": {
                "APIendpoint": "https://taik5rzzmk.execute-api.ap-southeast-1.amazonaws.com/default/py_get_user_medias",
                "APIkey": "fbUql8vhiH7cn2c8a2AIZ6HShwzszzu63GyKe8sm"
            },
            "GetMediaDetail": {
                "APIendpoint": "https://0cp84gb2ai.execute-api.ap-southeast-1.amazonaws.com/default/py_get_media_detail",
                "APIkey": "Zsz0NTzAYO5RUk8qRkhIw116uCDxv3ku8A6CwFxc"
            },
            "GetUserPNRs": {
                "APIendpoint": "https://u14i0wjsf6.execute-api.ap-southeast-1.amazonaws.com/default/py_get_user_pnrs",
                "APIkey": "LX7cHCnH6s7dmi1b7IIuH306tSuKsrUt6aaeQQGN"
            },
            "GetPNRdetail": {
                "APIendpoint": "https://c7f2jmgv81.execute-api.ap-southeast-1.amazonaws.com/default/py_get_pnr_detail",
                "APIkey": "k5LXAS4Sdn6sW4JTxGfs35mjm7A2zTP65H0jj4ht"
            },
            "GetVisaInformationList": {
                "APIendpoint": "https://7o8z33m2xe.execute-api.ap-southeast-1.amazonaws.com/default/py_get_visa_information_list",
                "APIkey": "UJmFT7LmLL6E29bIJGwhtaI6gdlzXqzx9bwgip7e"
            },
            "GetVisaInformationDetail": {
                "APIendpoint": "https://h73tsj9ngl.execute-api.ap-southeast-1.amazonaws.com/default/py_get_visa_information_detail",
                "APIkey": "mE5odA1rkv3RGyc2lTp2s5DgXTYVF0xf6AkNR4ub"
            },
            "GetSSLcommerzConfiguration": {
                "APIendpoint": "https://9q97iqfdbc.execute-api.ap-southeast-1.amazonaws.com/default/py_get_ssl_commerz_conf",
                "APIkey": "kSYEJhf7c98ZPjUHFZexG7fXk7AsGpoJ6FuAKNNV"
            },
            "GetApplicationSettings": {
                "APIendpoint": "https://tawyqzh7g8.execute-api.ap-southeast-1.amazonaws.com/default/py_get_application_settings",
                "APIkey": "5fNVuAxZt2ZaZPC0hle950kbZf4NhbD6xXLxI1ii"
            },
            "GetPackageInformationList": {
                "APIendpoint": "https://knmnxx6e0j.execute-api.ap-southeast-1.amazonaws.com/default/py_get_package_information_list",
                "APIkey": "OEApZyi1C45ZgUg5tVAxs408VnzwH6k42KpwIaSC"
            },
            "GetPackageInformationDetail": {
                "APIendpoint": "https://6g1vy7dce7.execute-api.ap-southeast-1.amazonaws.com/default/py_get_package_information_detail",
                "APIkey": "Q9cgT5ONHT2JaW8Vp4Y3e8KEgJD4UEsT89pUgLSS"
            },
            "GetCouponValue": {
                "APIendpoint": "https://4d8vwpwaz7.execute-api.ap-southeast-1.amazonaws.com/default/py_get_coupon_value",
                "APIkey": "3UYR8oDAXh2LDdkeK9Xd9t9L6VZ2CnF4W8o8POLj"
            }
        }

        if is_production == True:
            if api_module_name in production_api_map.keys():
                return production_api_map.get(api_module_name, None)
            else:
                raise Exception(
                    get_exception_message(
                        Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=f"Invalid API Module Name! Available API Module Names are : [{production_api_map.keys()}]"
                    )
                )
        else:
            if api_module_name in certification_api_map.keys():
                return certification_api_map.get(api_module_name, None)
            else:
                raise Exception(
                    get_exception_message(
                        Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                        msg=f"Invalid API Module Name! Available API Module Names are : [{certification_api_map.keys()}]"
                    )
                )
    try:
        # -------*******------- Fetch Application Settings from "setup_applicationsetting" Table -------*******-------
        try:
            # define result placeholder
            result = None

            # create connection
            con = connect_db()
            # cursor
            cur = con.cursor(
                cursor_factory=DictCursor
            )
            # Get Application Settings Query
            cur.execute(
                "SELECT id, application_name, is_production, application_domain_url, created_at, updated_at FROM setup_applicationsetting LIMIT 1"
            )

            # fetch Application Settings
            skytrip_settings = cur.fetchone()

            # define target map
            target_map = {
                "ID": None,
                "ApplicationName": None,
                "IsProduction": None,
                "ApplicationDomainURL": None,
                "CreatedAt": None,
                "UpdatedAt": None
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_detail_response(
                response=skytrip_settings, target_map=target_map
            )

            # return the result
            # return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                        0][2],
                    msg="Failed to SELECT Application Settings from 'setup_applicationsetting' Table!"
                )
            )

        # Return the API based on production status
        try:
            response = get_api(is_production=result["body"]["responseData"].get("IsProduction", None), api_module_name=RequestBody.get("APImoduleName", None))
            response["IsProduction"] = result["body"]["responseData"].get("IsProduction", None)
            return response
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to return skytrip API!"
                )
            )
    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to get Skytrip APIs!"
            )
        )
