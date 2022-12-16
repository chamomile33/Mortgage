import re

from urllib.request import urlopen
from banks.def_calculator import calc
from lxml import etree

_alpha = [5.9, 7.9, 5.7, 10, 4]


def alpha_init():
    url = "https://alfabank.ru/get-money/mortgage/"
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    ob = tree.xpath('//p[contains(text(),"Ставка")]/text()')
    _alpha[0] = float(re.findall(' (.*)%', ob[0])[0].replace(',', '.'))
    _alpha[1] = float(re.findall(' (.*)%', ob[1])[0].replace(',', '.'))
    _alpha[2] = float(re.findall(' (.*)%', ob[2])[0].replace(',', '.'))
    _alpha[4] = float(re.findall('\s(.*)%', ob[3])[0].replace(',', '.'))
    url = "https://alfabank.ru/get-money/mortgage/lgotnaya-ipoteka-dlya-it-specialistov/"
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    ob = tree.xpath('//span[@class="a2jE8"]/text()')
    _alpha[3] = float(re.findall('(.*)%', ob[0])[0].replace(',', '.'))


def alpha_request(request_description):
    if _request_failed(request_description):
        return {"Failed": 1}
    rate = _alpha[request_description["LoanProgram"]-1]
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
    if request_description["LoanProgram"] == 1 and request_description["PropertyCost"] > 12000000:
        request_description["LoanProgram"] = 5
    return False
