# import necessary libraries and packages
from skytrip.utils.helper import connect_db, get_exception_message
import inspect
from psycopg2.extras import DictCursor
from skytrip.db_read.helper import DBreadHelper


def get_coupon_value(RequestBody={}):
    """
    get_coupon_value() => Calculate and return coupon value.
    params => RequestBody (object)
    """

    def calculate_discount(coupon_setting=None, base_fair=None):
        """
        calculate_discount() => return calculated amount.
        params => coupon_setting (object), base_fair (float)
        """
        # print(" ================== Coupon Setting ================== : \b", coupon_setting)
        # print(" ================== Base Fair ================== : \b", base_fair)
        result = 0
        cut_off_value = coupon_setting["CutOffValue"]
        max_value = coupon_setting["MaxValue"]
        # For Coupon Type => Percentage
        if coupon_setting.get("CouponType", None) == 0:
            # print(" ================== Coupon Type 'Percentage' ==================")
            reduced_fair = (base_fair * cut_off_value) / 100

            if coupon_setting.get("MaxValue", None) is not None and max_value > 0:
                if (base_fair - reduced_fair) <= max_value:
                    result = reduced_fair
                else:
                    result = base_fair - max_value
            else:
                result = reduced_fair
        # For Coupon Type => Fixed Amount
        elif coupon_setting.get("CouponType", None) == 1:
            # print(" ================== Coupon Type 'Fixed Amount' ==================")
            result = base_fair - cut_off_value
        else:
            raise Exception(f"Invalid Coupon Type {coupon_setting.get('CouponType', None)}!")

        # return the result
        return {
            "DiscountedFair": result,
            "DiscountAmount": (base_fair - result)
        }


    def get_coupon_type(coupon_type=None):
        """
        get_coupon_type() => return coupon type.
        params => coupon_type (integer)
        """
        try:
            coupon_type_map = {
                0: "Percentage",
                1: "Fixed Amount"
            }
            if coupon_type in coupon_type_map:
                return coupon_type_map[coupon_type]
            else:
                raise Exception(f"Invalid Coupon Type {coupon_type}!")

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to get coupon type!"
                )
            )
    try:
        # define result placeholder
        result = None

        # create connection
        con = connect_db()
        # cursor
        cur = con.cursor(
            cursor_factory=DictCursor
        )

        # -------*******------- Fetch Records from "setup_couponsetting" Table -------*******-------
        try:
            # Get User Medias Query
            cur.execute(
                "SELECT id, origin_location_code, destination_location_code, all_route, code, cut_off_value, coupon_type, max_value, created_at, updated_at FROM setup_couponsetting WHERE code='{}'".format(
                    RequestBody.get("CouponCode", None)
                )
            )

            # fetch user medias
            coupon = cur.fetchone()

            # define target map
            target_map = {
                "ID": None,
                "OriginLocationCode": None,
                "DestinationLocationCode": None,
                "ForAllRoute": None,
                "CouponCode": None,
                "CutOffValue": None,
                "CouponType": None,
                "MaxValue": None,
                "CreatedAt": None,
                "UpdatedAt": None
            }

            # DB Read Helper Instance
            db_read_helper = DBreadHelper()

            # assign result from map response
            result = db_read_helper.map_detail_response(
                response=coupon, target_map=target_map
            )

            # print(" ================== Result ================== : \b", result)

            responseNode = result["body"]["responseData"]

            # Response Route
            if responseNode['OriginLocationCode'] is not None and responseNode['DestinationLocationCode'] is not None:
                responseRoute = f"{responseNode['OriginLocationCode'].upper()}-{responseNode['DestinationLocationCode'].upper()}"
            else:
                responseRoute = f"{responseNode['OriginLocationCode']}-{responseNode['DestinationLocationCode']}"
            # Request Route
            requestRoutes = []
            for route in RequestBody.get("LegDescription", []):
                requestRoutes.append(
                    f"{route['OriginLocation'].upper()}-{route['DestinationLocation'].upper()}"
                )
            
            # print(requestRoutes, "------- Request Routes -------")
            # print(responseRoute, "------- Response Route -------")

            # calculate discount
            if responseNode.get("ForAllRoute", None) == True:
                discounted_fair = calculate_discount(
                    coupon_setting=responseNode, base_fair=RequestBody.get("BaseFair", None)
                )
            elif responseRoute in requestRoutes:
                discounted_fair = calculate_discount(
                    coupon_setting=responseNode, base_fair=RequestBody.get("BaseFair", None)
                )
            else:
                raise Exception(f"Origin and Destination Location Code Doesn't match!")

            # Get Coupon Type String Representation
            result["body"]["responseData"]["CouponType"] = get_coupon_type(
                coupon_type=responseNode.get("CouponType", None)
            )

            # Assign DiscountedFair and DiscountAmount in result node
            result["body"]["responseData"]["DiscountedFair"] = discounted_fair["DiscountedFair"]
            result["body"]["responseData"]["DiscountAmount"] = discounted_fair["DiscountAmount"]

            # return the result
            return result

        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to SELECT Coupon Setting from 'setup_couponsetting' Table!"
                )
            )

    # ------- Handle Exceptions -------
    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg="Failed to get Coupon Setting!"
            )
        )
