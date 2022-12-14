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


response = parser.request(data)

print('-'*40)
for key in response:
    print(key)
    print(json.dumps(response[key], indent=4))
    print('-'*40)
