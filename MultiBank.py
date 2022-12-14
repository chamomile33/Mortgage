import json
import pandas as pd
from banks.sber import sber_request
from banks.vtb import vtb_request


class MultiBank:

    def request(self, userdata=None):
        """ \\
            Get json responses from all banks for a single property, or for a DataFrame describing properties. \\
            Expected parameters for each property: \\

            "LoanProgram" - number from 1 to 4. Encodes loan purpose.\\
            1 - Новостройка
            2 - Вторичное жилье
            3 - Ипотека для семьи с детьми
            4 - Ипотека для ИТ специалистов

            "RegionCode" - code numer of a region of property \\
            "PropertyCost" - number, property cost \\
            "InitialFee" - number, initial payment \\
            "LoanTerm" - number of years for paying the loan \\
            Missing parameters are filled with standard values.\\
            \\
            Standard response:\\
            "CreditSum": сумма кредита
            "CreditRate": процентная ставка
            "MonthlyPayment": месячный платеж
            "Term": длительность
            "OverPayment": переплата
            "TotalCost": Итоговая стоимость квартиры
        """

        if userdata is None:
            userdata = self._standard_request_description

        if isinstance(userdata, pd.DataFrame):
            return self._multi_request(userdata)

        return self._single_request(userdata)

    def _multi_request(self, user_data):
        for loan_description in user_data:
            yield self._single_request(loan_description)

    def _single_request(self, loan_description):
        request_description = self._standard_request_description
        for key in self._standard_request_description:
            if key in loan_description:
                request_description[key] = loan_description[key]
        return self._request(request_description)

    def _request(self, request_description):
        response = {"Sber": sber_request(request_description),
                    "VTB": vtb_request(request_description),
                    # "Tinkoff": tink_request(request_description),
                    # "Alpha": alpha_request(request_description)
                    }
        return response

    def __init__(self, params=None):
        self._standard_request_description = {
            "LoanProgram": 1,  # 1..4
            "RegionCode": 77,  # That's Moscow
            "PropertyCost": 3000000,  # Property cost -- the cost of a real estate you want to buy
            "InitialFee": 600000,  # The initial payment
            "LoanTerm": 30,  # Number of years of payment
        }
