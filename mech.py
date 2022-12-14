import requests
import json
from MultiBank import MultiBank
from banks.tink import tink_request
from banks.def_calculator import calc
parser = MultiBank()
parser.request()
data = {
    "LoanProgram": 1,
    "RegionCode": 77,
    "PropertyCost": 7000000,
    "InitialFee": 600000,
    "LoanTerm": 25,
}

print(calc(rate=10.9, term=2, deposit=200000, cost=1200000))

# tink_init()
# tink_request("aboba")


# response = parser.request(data)

# print(json.dumps(response['Sber'], indent=4))
# print('-'*40)
# print(json.dumps(response['VTB'], indent=4))
