from skytrip.db_read.get_coupon_value import get_coupon_value
import json


data = {
    "LegDescription": [
        {
            "OriginLocation": "BAH",
            "DestinationLocation": "DAC"
        },
        {
            "OriginLocation": "DAC",
            "DestinationLocation": "CGP"
        }
    ],
    "CouponCode": "DDD12345",
    "BaseFair": 100000
}

response = get_coupon_value(RequestBody=data)


print(f"\n {'*' * 50} Get Coupon Value {'*' * 50} : \n\n Response: ", response, "\n\n")
