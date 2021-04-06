from skytrip.skytrip_handler.create_pnr import create_pnr
import json


data = {
    "ExistedToken": {
        "access_token": "T1RLAQL3RPZA9yvHzMtK1/m7MMWUIXoMMBDcT5x2dHK2m13VxRQOIPHqAADAS2SeJp2cIA/b2NmPnnVSDxGrTbaXq0FE4G7nKhnQLijlWwDxA/CtdiVnfUq37Fu3bpYv9u7iWmzv82WbIMvUWr6hn7tFU/jZ32iBy8SRSwduP7U2b7Rbbw9X2wS0fIC2McZqEKNc57NNTPTlVnf9BUluhChI7sNqrqzFcxhHTAaisywu3BMdT8jqrPRlaaeMCqfxJ6opCeOUB+P+f7vVDMiDadrXGvPd9EXRaNTYLeSf2+/m10OcBQyaYLKaitV3",
        "token_type": "bearer",
        "expires_in": 604800,
        "expires": 1616997963.0937102
    },
    "UserID": 1,
    "TransactionID": "8e931621-ecda-4296-a7ce-82eef53098d4",
    "DataSource": "B2C",
    "Utils": {
        "ExampleData": "Example Utils Data"
    },
    "RequestLOG": False,
    "RequestBody": {
        "ContactNumber": [
            {
                "NameNumber": "1.1",
                "Phone": "4574675236431",
                "PhoneUseType": "H"
            }
        ],
        "Email": [
            {
                "NameNumber": "1.1",
                "Address": "wilson@gmail.com"
            }
        ],
        "PersonName": [
            {
                "NameNumber": "1.1",
                "NameReference": "ABC123",
                "PassengerType": "ADT",
                "GivenName": "EDWARD JACKSON",
                "Surname": "WILSON",
                "DateOfBirth": "1991-04-04",
                "Gender": "M"
            }
        ],
        "AdvancePassenger": [
            {
                "Document": {
                    "Number": "1XF74875",
                    "IssueCountry": "BGD",
                    "NationalityCountry": "BGD",
                    "ExpirationDate": "2022-06-14",
                    "Type": "P"
                },
                "PersonName": {
                    "NameNumber": "1.1",
                    "GivenName": "EDWARD JACKSON",
                    "MiddleName": "",
                    "Surname": "WILSON",
                    "DateOfBirth": "1991-04-04",
                    "Gender": "M"
                },
                "SegmentNumber": "A"
            }
        ],
        "Service": [],
        "OriginDestinationInformation": [
            {
                "DepartureDateTime": "2021-04-17T23:00:00",
                "OriginLocation": {
                    "LocationCode": "DAC"
                },
                "DestinationLocation": {
                    "LocationCode": "DXB"
                },
                "RPH": "0"
            }
        ],
        "LegDescription": [
            {
                "DepartureDate": "2021-04-17",
                "DepartureLocation": "DAC",
                "ArrivalLocation": "DXB"
            }
        ],
        "TargetItinerary": {
            "ID": 1,
            "GDS": "Sabre",
            "ScheduleDescription": [
                {
                    "NoOfStoppage": 0,
                    "ETicketable": True,
                    "TotalDistanceInMiles": 2640,
                    "Departure": {
                        "Airport": "DAC",
                        "City": "DAC",
                        "Country": "BD",
                        "Time": "01:45:00+06:00",
                        "Terminal": "",
                        "DateAdjustment": 0
                    },
                    "Arrival": {
                        "Airport": "KWI",
                        "City": "KWI",
                        "Country": "KW",
                        "Time": "05:05:00+03:00",
                        "Terminal": "4",
                        "DateAdjustment": 0
                    },
                    "Carrier": {
                        "OperatingCarrierCode": "KU",
                        "OperatingFlightNumber": 420,
                        "MarketingCarrierCode": "KU",
                        "MarketingFlightNumber": 420
                    }
                },
                {
                    "NoOfStoppage": 0,
                    "ETicketable": True,
                    "TotalDistanceInMiles": 530,
                    "Departure": {
                        "Airport": "KWI",
                        "City": "KWI",
                        "Country": "KW",
                        "Time": "09:35:00+03:00",
                        "Terminal": "4",
                        "DateAdjustment": 0
                    },
                    "Arrival": {
                        "Airport": "DXB",
                        "City": "DXB",
                        "Country": "AE",
                        "Time": "12:35:00+04:00",
                        "Terminal": "3",
                        "DateAdjustment": 0
                    },
                    "Carrier": {
                        "OperatingCarrierCode": "KU",
                        "OperatingFlightNumber": 671,
                        "MarketingCarrierCode": "KU",
                        "MarketingFlightNumber": 671
                    }
                }
            ],
            "PassengerInfo": [
                {
                    "PassengerType": "ADT",
                    "PassengerNumber": 1,
                    "NonRefundable": False,
                    "FareDescription": [
                        {
                            "NotValidAfter": "2021-04-17",
                            "NotValidBefore": "2021-04-17",
                            "Segment": [
                                {
                                    "CabinClass": "Economy",
                                    "SeatsAvailable": 7,
                                    "BookingCode": "V",
                                    "MealCode": "BM"
                                },
                                {
                                    "CabinClass": "Economy",
                                    "SeatsAvailable": 7,
                                    "BookingCode": "V",
                                    "MealCode": "BM"
                                }
                            ]
                        }
                    ],
                    "BaggageDescription": [
                        {
                            "NumberOfPieces": 2,
                            "MaxWeight": "",
                            "Unit": ""
                        }
                    ],
                    "PassengerTotalFare": {
                        "totalFare": 30568,
                        "totalTaxAmount": 8255,
                        "currency": "BDT",
                        "baseFareAmount": 265.0,
                        "baseFareCurrency": "USD",
                        "equivalentAmount": 22313,
                        "equivalentCurrency": "BDT",
                        "constructionAmount": 265.0,
                        "constructionCurrency": "NUC",
                        "commissionPercentage": 0,
                        "commissionAmount": 0,
                        "exchangeRateOne": 1.0
                    }
                }
            ],
            "TotalFare": {
                "totalPrice": 30568,
                "totalTaxAmount": 8255,
                "currency": "BDT",
                "baseFareAmount": 265.0,
                "baseFareCurrency": "USD",
                "constructionAmount": 265.0,
                "constructionCurrency": "NUC",
                "equivalentAmount": 22313,
                "equivalentCurrency": "BDT"
            }
        }
    }
}

response = create_pnr(RequestBody=data)


print(f"\n {'*' * 50} Create PNR {'*' * 50} : \n\n Response: ", response, "\n\n")
