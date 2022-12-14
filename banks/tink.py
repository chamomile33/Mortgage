import logging
import re

from urllib.request import urlopen
from banks.def_calculator import calc
from lxml import etree

_tink = [5.9, 7.9, 5.7]


def tink_init():
    url = "https://www.tinkoff.ru/mortgage/"
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    ob = tree.xpath('//li[contains(text(),"Ставка")]/text()')
    ob2 = tree.xpath('//li[contains(text(),"ставка")]/text()')
    _tink[0] = float(re.findall('\\xa0(.*)%', ob[0])[0].replace(',', '.'))
    _tink[2] = float(re.findall('ставка (.+)%', ob2[0])[0].replace(',', '.'))
    _tink[1] = float(re.findall('\\xa0(.*)%', ob[1])[0].replace(',', '.'))


def tink_request(request_description):
    if _request_failed(request_description):
        logging.exception("Tink refused. Unable to give program.")
        return {"Failed: 1"}
    rate = _tink[request_description["LoanProgram"]-1]
    term = request_description["LoanTerm"]
    deposit = request_description["InitialFee"]
    cost = request_description["PropertyCost"]
    monthly_payment = calc(rate, term, deposit, cost)
    data = {
        "CreditSum": cost-deposit,
        "CreditRate": rate,
        "MonthlyPayment": monthly_payment,
        "Term": term,
        "OverPayment": monthly_payment*12*term - cost + deposit,
        "TotalCost": monthly_payment*12*term + deposit,
        "InitialFee": request_description["InitialFee"],
    }
    return data


def _request_failed(request_description):
    if request_description["LoanProgram"] == 4:
        return True
    if request_description["LoanProgram"] == 1 and request_description["PropertyCost"] > 12000000:
        return True
    return False
