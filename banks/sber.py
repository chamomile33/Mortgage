import json

import requests
import logging


def sber_request(request_description):
    url = "https://api.domclick.ru/calc/api/v8/calculate"
    data = _sber_refactor_request(request_description)
    response = requests.post(url=url, json=data)
    if response.ok:
        return _sber_refactor_response(response.json())
    logging.exception("Sber request refused.")
    return {"Failed": 1}


def _sber_refactor_request(request_destription):
    request_data = '{"calculationParams":{"productId":3,"discountsActivity":{"1":true,"2":true,"7":true},' \
                   '"categoryCode":"salaryClient","loanConditions":{"realtyCost":4152914,"deposit":600000,' \
                   '"baseDeposit":600000,"maternalFund":0,"creditTerm":30},"regionNumber":77,"subproductCode":null,' \
                   '"subproductId":1,"additionalServicesParams":null,"developerDiscountsActivity":[],' \
                   '"ownRateDiscountsActivity":[]}} '
    request_data = json.loads(request_data)
    if request_destription["LoanProgram"] == 1:
        request_data = json.loads('{"calculationParams":{"productId":16,"discountsActivity":{"2":true,"7":true},'
                                  '"categoryCode":"salaryClient","loanConditions":{"realtyCost":5398418,'
                                  '"deposit":809763,"baseDeposit":809763,"maternalFund":0,"creditTerm":20},'
                                  '"regionNumber":77,"subproductCode":null,"subproductId":12,'
                                  '"additionalServicesParams":null,"developerDiscountsActivity":[],'
                                  '"ownRateDiscountsActivity":[]}}')
    if request_destription["LoanProgram"] == 2:
        request_data = json.loads('{"calculationParams":{"productId":3,"discountsActivity":{"1":true,"2":true,'
                                  '"7":true},"categoryCode":"salaryClient","loanConditions":{"realtyCost":10253428,'
                                  '"deposit":7372759,"baseDeposit":7372759,"maternalFund":0,"creditTerm":20},'
                                  '"regionNumber":77,"subproductCode":null,"subproductId":1,'
                                  '"additionalServicesParams":null,"developerDiscountsActivity":[],'
                                  '"ownRateDiscountsActivity":[]}}')
    if request_destription["LoanProgram"] == 3:
        request_data = json.loads('{"calculationParams":{"productId":10,"discountsActivity":{"7":true},'
                                  '"categoryCode":"salaryClient","loanConditions":{"realtyCost":10253428,'
                                  '"deposit":7372759,"baseDeposit":7372759,"maternalFund":0,"creditTerm":20},'
                                  '"regionNumber":77,"subproductCode":null,"subproductId":8,'
                                  '"additionalServicesParams":null,"developerDiscountsActivity":[],'
                                  '"ownRateDiscountsActivity":[]}}')
    if request_destription["LoanProgram"] == 4:
        request_data = json.loads('{"calculationParams":{"productId":4,"discountsActivity":{"7":true},'
                                  '"categoryCode":"salaryClient","loanConditions":{"realtyCost":21375574,'
                                  '"deposit":7372759,"baseDeposit":7372759,"maternalFund":0,"creditTerm":20},'
                                  '"regionNumber":0,"subproductCode":15400,"subproductId":33,'
                                  '"additionalServicesParams":null,"developerDiscountsActivity":[],'
                                  '"ownRateDiscountsActivity":[]}}')
    request_data["calculationParams"]["regionNumber"] = request_destription["RegionCode"]
    request_data["calculationParams"]["loanConditions"] = {
        "realtyCost": request_destription["PropertyCost"],
        "deposit": request_destription["InitialFee"],
        "baseDeposit": request_destription["InitialFee"],
        "maternalFund": 0,
        "creditTerm": request_destription["LoanTerm"],
    }
    return request_data


def _sber_refactor_response(response):
    data = {
        "CreditSum": response['data']['calculationResult']['creditSum'],
        "CreditRate": response['data']['calculationResult']['creditRate'],
        "MonthlyPayment": response['data']['calculationResult']['monthlyPayment'],
        "Term": response['data']['calculationResult']['term'],
        "OverPayment": response['data']['calculationResult']['overpayment'],
        "TotalCost": response['data']['calculationResult']['overpayment'] +
                     response['data']['calculationResult']['realtyCost'],
    }
    return data
