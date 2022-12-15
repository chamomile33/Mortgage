import json

import requests
import logging


def vtb_request(request_description):
    url = "https://siteapi.vtb.ru/api/calcmortgage/api/Sitecore/Mortgage/NewBuildingAjax"
    data = _vtb_refactor(request_description)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
               "Accept": "application/json, text/plain, */*",
               "Accept-Language": "en-US,en;q=0.5",
               "Accept-Encoding": "gzip, deflate, br",
               "Content-Type": "application/json",
               "Origin": "https://www.vtb.ru",
               "Connection": "keep-alive",
               "Referer": "https://www.vtb.ru/",
               "Sec-Fetch-Dest": "empty",
               "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Site": "same-site",
               "TE": "trailers",
               }
    response = requests.post(url=url, json=data, headers=headers)
    if response.ok:
        return _vtb_refactor_response(response.json())
    logging.exception("VTB request refused.")
    logging.exception(response.text)
    return {"Failed": 1}


def _vtb_refactor(request_destription):
    request_data = '{"location":null,"ProgramName":"NewBuildingProgram","PropertyPrice":7000000,' \
                   '"DataSourceId":"E27EE059-6B85-4B51-9688-BDB7FD91D3A7","Programs":["7"],"Clients":[],' \
                   '"IsProgramChecked":true,"IsFirstLoad":false,"CreditSumByIncome":0,"CreditTermByCost":30,' \
                   '"CreditTermByIncome":0,"DownPayment":1400000,"MaternialCapital":0,"MonthlyIncome":200000,' \
                   '"MonthlyPaymentByCost":0,"MonthlyPaymentByCostSign":0,"MonthlyPaymentByIncome":0,' \
                   '"MonthlyPaymentByIncomeSign":0} '

    request_data = json.loads(request_data)
    if request_destription["LoanProgram"] == 1:
        request_data = json.loads('{"location":null,"ProgramName":"NewBuildingProgram","PropertyPrice":9360000,'
                                  '"DataSourceId":"E27EE059-6B85-4B51-9688-BDB7FD91D3A7","Programs":["7"],"Clients":['
                                  '],"IsProgramChecked":true,"IsFirstLoad":false,"CreditSumByIncome":0,'
                                  '"CreditTermByCost":30,"CreditTermByIncome":0,"DownPayment":1791000,'
                                  '"MaternialCapital":0,"MonthlyIncome":200000,"MonthlyPaymentByCost":0,'
                                  '"MonthlyPaymentByCostSign":0,"MonthlyPaymentByIncome":0,'
                                  '"MonthlyPaymentByIncomeSign":0}')
    if request_destription["LoanProgram"] == 2:
        request_data = json.loads('{"location":null,"ProgramName":"ResaleProgram","PropertyPrice":11200000,'
                                  '"DataSourceId":"AEE792C1-3565-4835-B7E5-9FA9A9F4009F","Programs":["7"],"Clients":['
                                  '],"IsProgramChecked":true,"IsFirstLoad":false,"CreditSumByIncome":0,'
                                  '"CreditTermByCost":30,"CreditTermByIncome":0,"DownPayment":1400000,'
                                  '"MaternialCapital":0,"MonthlyIncome":200000,"MonthlyPaymentByCost":0,'
                                  '"MonthlyPaymentByCostSign":0,"MonthlyPaymentByIncome":0,'
                                  '"MonthlyPaymentByIncomeSign":0}')
    if request_destription["LoanProgram"] == 3:
        request_data = json.loads('{"location":null,"ProgramName":"Gospoddezhka","PropertyPrice":9140000,'
                                  '"DataSourceId":"A56A9289-FC66-4F7B-8F3B-FA4F5E9BD113","Programs":["7"],"Clients":['
                                  '],"IsProgramChecked":true,"IsFirstLoad":false,"CreditSumByIncome":0,'
                                  '"CreditTermByCost":30,"CreditTermByIncome":0,"DownPayment":1371000,'
                                  '"MaternialCapital":0,"MonthlyIncome":1000000,"MonthlyPaymentByCost":0,'
                                  '"MonthlyPaymentByCostSign":0,"MonthlyPaymentByIncome":0,'
                                  '"MonthlyPaymentByIncomeSign":0}')
    if request_destription["LoanProgram"] == 4:
        return {"Failed": 1}
    request_data["PropertyPrice"] = request_destription["PropertyCost"]
    request_data["DownPayment"] = request_destription["InitialFee"]
    request_data["baseDeposit"] = request_destription["InitialFee"]
    request_data["CreditTermByCost"] = request_destription["LoanTerm"]
    return request_data


def _vtb_refactor_response(response):
    data = {
        "CreditSum": response['CreditSizeByCost'],
        "CreditRate": response['MorgageRateByCost'],
        "MonthlyPayment": response['MonthlyPaymentByCost'],
        "Term": response['CreditTermByCost'],
        "OverPayment": response['MonthlyPaymentByCost']*12*response['CreditTermByCost'] - response['CreditSizeByCost'],
        "TotalCost": response['MonthlyPaymentByCost']*12*response['CreditTermByCost'] + response["DownPayment"],
        "InitialFee": response["DownPayment"],
    }
    return data
