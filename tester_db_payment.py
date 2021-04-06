from skytrip.db_payment.db_payment_handler import DBpaymentHandler
import json

true = True
false = False

# # -------------------------------------------------------------------
# #                           Prepare Data
# # -------------------------------------------------------------------

data = {
    "user_email": "user@user.com",
    "tran_id": "8e931621-ecda-4296-a7ce-82eef53098d4",
    "transaction_log": "###1711231900331kHP17lnrr9T8Gt",
    "total_amt": 445095,
    "amount": 445095,
    "card_type": "VISA-Dutch Bangla",
    "store_amount": 445095,
    "card_no": "425272XXXXXX345",
    "bank_tran_id": "1711231900331S0R8atkhAZksmM",
    "status": "VALID",
    "tran_date": "2017-11-23 18:59:55",
    "currency": "BDT",
    "card_issuer": "Standard Chartered Bank",
    "card_brand": "VISA",
    "card_issuer_country": "Bangladesh",
    "card_issuer_country_code": "BD",
    "store_id": "testbox",
    "verify_sign": "8070c0cefed9e629b01100d8a92afda2",
    "verify_key": "amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_type,currency,currency_amount,currency_rate,currency_type,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d",
    "cus_fax": "01711111111",
    "currency_type": "BDT",
    "currency_amount": 100.00,
    "currency_rate": 1.0000,
    "base_fair": 0.00
}

event_body = data
response = None


def moduleRunner(testWithWhile=False, runAmount=7):
    """
    moduleRunner() => Skytrip Module Runner Function.
    params: testWithWhile (Boolean, default=False), runAmount (integer, default=7)
    """
    if testWithWhile == True:
        i = 0
        while i <= runAmount:
            moduleHandler = DBpaymentHandler(EventBodyData=event_body)
            response = moduleHandler.insert_data_in_payment()
            print(
                f"\n {'*' * 50} DB Payment Response Data {'*' * 50} : \n\n PaymentID: ", response, "\n\n")
            i += 1
    else:
        moduleHandler = DBpaymentHandler(EventBodyData=event_body)
        response = moduleHandler.insert_data_in_payment()
        print(f"\n {'*' * 50} DB Payment Response Data {'*' * 50} : \n\n PaymentID: ",
              response, "\n\n")
    # return the response
    return response


# get actual response
response = moduleRunner(testWithWhile=False, runAmount=5)
