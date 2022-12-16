import json
import pandas as pd

from banks.alpha import alpha_request
from banks.sber import sber_request
from banks.tink import tink_request
from banks.vtb import vtb_request
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State


def _create_form(response, bank_name):
    r = response[bank_name]
    ru_names = {'Sber': "СБЕР", 'VTB': "ВТБ", "Tinkoff": "Tinkoff", "Alpha": "Альфа"}
    # print(response[bank_name])
    if "Failed" not in response[bank_name]:
        rows = [ru_names[bank_name], str(round(r["MonthlyPayment"], 2)), str(r["Term"]), str(r["CreditRate"]), str(round(r["TotalCost"], 2))]
    else:
        rows = [ru_names[bank_name]]+['Отказ']*4
    form = []
    for row in rows:
        form.append(dbc.Form(class_name=bank_name + '-form', children=[
            dbc.Row([
                dbc.Row([
                    dbc.Col([
                        dbc.Label(row, width='auto', style={'font-size': '17px'})
                    ], style={"text-align": "center"})
                ]),
            ])
        ]),)
    return form


def _request(request_description):
    request_description["InitialFee"] = max(request_description["InitialFee"],
                                            int(request_description["PropertyCost"] * 0.15))
    response = {"Sber": sber_request(request_description),
                "VTB": vtb_request(request_description),
                "Tinkoff": tink_request(request_description),
                "Alpha": alpha_request(request_description)
                }
    return response


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
            "InitialFee": Первоначальный взнос
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
        return _request(request_description)

    def __init__(self, params=None):
        self._standard_request_description = {
            "LoanProgram": 1,  # 1..4
            "RegionCode": 77,  # That's Moscow
            "PropertyCost": 3000000,  # Property cost -- the cost of a real estate you want to buy
            "InitialFee": 600000,  # The initial payment
            "LoanTerm": 30,  # Number of years of payment
        }

    def get_bank_div(self, mortgage_info):
        response = self.request(mortgage_info)
        if "Failed" in mortgage_info:
            return html.Div([
                dbc.Col(dbc.Label("Ответ банков по ипотеке: не было запроса.", width='auto',
                                  style={'font-size': '17px', 'font-weight': 'bold'}), style={'width': '25%', 'display': 'inline-block'}),
            ], style={'margin-left': '0px', 'margin-right': '0px'})
        cols = [_create_form(response, "Sber"), _create_form(response, "VTB"), _create_form(response, "Tinkoff"), _create_form(response, "Alpha")]
        rows = []
        row_names = ["Предложения по ипотеке", "Месячный платёж, руб.", "Продолжительность ипотеки, года", "Процентная ставка, %", "Итоговая стоимость квартиры"]
        for i in range(len(row_names)):
            rows.append(
                dbc.Row([
                    dbc.Col(dbc.Label(row_names[i], width='auto',
                                      style={'font-size': '17px', 'font-weight': 'bold'}),
                            style={'width': '25%', 'display': 'inline-block', 'text-align': 'center'}),
                ])
            )
            rows.append(
                dbc.Row([
                    dbc.Col(cols[0][i], style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Col(cols[1][i], style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Col(cols[2][i], style={'width': '25%', 'display': 'inline-block'}),
                    dbc.Col(cols[3][i], style={'width': '25%', 'display': 'inline-block'}),
                ])
            )
        div = html.Div(rows, style={'margin-left': '0px', 'margin-right': '0px'})
        return div
