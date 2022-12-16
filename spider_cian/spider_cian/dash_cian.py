import asyncio
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc,Input,Output,State
import datetime
import re
import numpy as np
import json
from urllib.request import urlopen
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from MultiBank import MultiBank
import subprocess
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
banks = MultiBank()
object_type = dcc.Dropdown(['Новостройка', 'Вторичка'],id='object_type')
rooms = dcc.Checklist(['1','2','3','4','5','6+','Студия','Свободная планировка'],inline = True,labelStyle={'margin-right':'15px'},inputStyle={'margin-right':'2px'},id = 'rooms')
minprice = dbc.InputGroup([dbc.Input(type = 'number',placeholder="от",min = 0,max = 900_000_000_000,id = 'minprice',step=1),dbc.InputGroupText("₽")])
maxprice = dbc.InputGroup([dbc.Input(type = 'number',placeholder="до",min = 0,max = 900_000_000_000,id = 'maxprice',step=1),dbc.InputGroupText("₽")])
price = dbc.Row([
    dbc.Col(minprice),
    dbc.Col(maxprice)
]
)
minarea = dbc.InputGroup([dbc.Input(type = 'number',placeholder="от",min = 0,max = 9000,id = 'minarea',step=1),dbc.InputGroupText("м²")])
maxarea = dbc.InputGroup([dbc.Input(type = 'number',placeholder="до",min = 0,max = 9000,id = 'maxarea',step=1),dbc.InputGroupText("м²")])
area = dbc.Row([
    dbc.Col(minarea),
    dbc.Col(maxarea)
]
)
min_living_area = dbc.InputGroup([dbc.Input(type = 'number',placeholder="от",min = 0,max = 9000,id = 'min_living_area',step=1),dbc.InputGroupText("м²")])
max_living_area = dbc.InputGroup([dbc.Input(type = 'number',placeholder="до",min = 0,max = 9000,id = 'max_living_area',step=1),dbc.InputGroupText("м²")])
living_area = dbc.Row([
    dbc.Col(min_living_area),
    dbc.Col(max_living_area)
]
)
min_kitchen_area = dbc.InputGroup([dbc.Input(type = 'number',placeholder="от",min = 0,max = 9000,id = 'min_kitchen_area',step=1),dbc.InputGroupText("м²")])
max_kitchen_area = dbc.InputGroup([dbc.Input(type = 'number',placeholder="до",min = 0,max = 9000,id = 'max_kitchen_area',step=1),dbc.InputGroupText("м²")])
kitchen_area = dbc.Row([
    dbc.Col(min_kitchen_area),
    dbc.Col(max_kitchen_area)
]
)
minfloor = dbc.Input(type = 'number',placeholder="от",min = 0,max = 200,id = 'minfloor',step=1)
maxfloor = dbc.Input(type = 'number',placeholder="до",min = 0,max = 200,id = 'maxfloor',step=1)
floor_type = dcc.Checklist(['Не первый','Не последний','Только последний'],inline = True,labelStyle={'margin-right':'25px'},inputStyle={'margin-right':'2px'},id = 'floor_type')
floor = dbc.Row([dbc.Row([dbc.Col(minfloor),dbc.Col(maxfloor)]),dbc.Row(floor_type)])

min_house_year = dbc.InputGroup([dbc.Input(type = 'number',placeholder="от",min = 1000,max = datetime.datetime.now().year,id = 'min_house_year',step=1),dbc.InputGroupText("г")])
max_house_year = dbc.InputGroup([dbc.Input(type = 'number',placeholder="до",min = 1000,max = datetime.datetime.now().year,id = 'max_house_year',step=1),dbc.InputGroupText("г")])
house_year = dbc.Row([
    dbc.Col(min_house_year),
    dbc.Col(max_house_year)
]
)
mortgage_type = dcc.Dropdown(['Стандартная ипотека', 'Ипотека для семьи с детьми','Ипотека для ИТ специалистов'],id='mortgage_type')
down_payment = dbc.InputGroup([dbc.Input(type = 'number',min = 0,id = 'down_payment',step=1),dbc.InputGroupText("₽")])
salary = dbc.InputGroup([dbc.Input(type = 'number',min = 0,id = 'salary',step=1),dbc.InputGroupText("₽")])
percent_on_mortgage = dbc.InputGroup([dbc.Input(type = 'number',min = 0,max = 100,id = 'percent_on_mortgage',step=1),dbc.InputGroupText("%")])

region = dbc.Input(type='text',id='region', pattern=r"^[а-яА-Я,\.-\w\s]{0,50}$")
html_form = html.Div(style = {'margin-left':'10px'},children=[
    dbc.Form(class_name = 'card p-1',children=[
    dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Тип квартиры",width = 'auto',style={'font-size':'17px'})])]),
            dbc.Col(object_type)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Количество комнат", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(rooms)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Цена", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(price)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Общая площадь", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(area)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Жилая площадь", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(living_area)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Площадь кухни", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(kitchen_area)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Этаж", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(floor)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(
        [
            dbc.Row([dbc.Col([dbc.Label("Год постройки", width="auto",style={'font-size':'17px'})])]),
            dbc.Col(house_year)
        ],
        style={'margin-bottom':'10px','margin-left':'2px','margin-right':'2px'}
    ),
     dbc.Row(
        [
            dbc.Row([dbc.Label("Район", width="auto",style={'font-size':'17px'})]),
            dbc.Col(region)
        ],
        style={'margin-bottom':'20px','margin-left':'2px','margin-right':'2px'}
    )

]),

dbc.Form(class_name = 'card p-1',style={'margin-top':'20px'},children =[
    dbc.Row(
        [
            dbc.Row([dbc.Label("Тип ипотеки", width="auto",style={'font-size':'17px'})]),
            dbc.Col(mortgage_type)
        ],
        style={'margin-bottom':'20px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(
        [
            dbc.Row([dbc.Label("Первоначальный взнос", width="auto",style={'font-size':'17px'})]),
            dbc.Col(down_payment)
        ],
        style={'margin-bottom':'20px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(
        [
            dbc.Row([dbc.Label("Зарплата", width="auto",style={'font-size':'17px'})]),
            dbc.Col(salary)
        ],
        style={'margin-bottom':'20px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(
        [
            dbc.Row([dbc.Label("Процент от зарплаты, отдаваемый на ипотеку", width="auto",style={'font-size':'17px'})]),
            dbc.Col(percent_on_mortgage)
        ],
        style={'margin-bottom':'20px','margin-left':'2px','margin-right':'2px'}
    ),
    dbc.Row(dbc.Button("Count", color="primary",style={'width':'20%'},id='count'),justify='center')
])])

app.layout = html.Div([
    dbc.Col(html_form,style={'width':'35%','display':'inline-block'}),
    dbc.Col(id = 'mortgage',style={'width':'60%','display':'inline-block','margin-left':'10px','margin-top':'20px', 'vertical-align':'top'},
    children=[html.Div([
            dbc.Row([dcc.Graph(id = 'map')]),
            html.Label(id='mean'),
            dbc.Row(id = 'banks')
        ])])
],style={'margin-left':'0px','margin-right':'0px'})


def get_region_id(reg_name):
    regions_df = pd.read_csv('spider_cian/items.csv').set_index('name')
    match = process.extractOne(reg_name,regions_df.index.to_list(),scorer=fuzz.token_sort_ratio)
    return regions_df.loc[[match[0]]]['id'].values[0]

def get_url(form_dict):
    basic_url = "https://cian.ru/cat.php?deal_type=sale"
    rooms = form_dict['rooms']
    if rooms != None:
        for room in rooms:
            if room=='6+':
                room = '6'
            elif room == 'Студия':
                room = '9'
            elif room == 'Свободная планировка':
                room = '7'
            basic_url += f'&room{room}=1'

    region = form_dict['region']
    if region != None:
        id = get_region_id(region)
        basic_url+=f'&region={id}'

    if form_dict['object_type'] == 'Новостройка':
        basic_url+= '&with_newobject=1'
    elif form_dict['object_type'] == 'Вторичка':
        basic_url+='&object_type%5B0%5D=1'
    
    if form_dict['minprice'] != None:
        basic_url+=f"&minprice={form_dict['minprice']}"
    if form_dict['maxprice'] != None:
        basic_url+=f"&maxprice={form_dict['maxprice']}"
    
    if form_dict['minarea'] != None:
        basic_url+=f"&mintarea={form_dict['minarea']}"
    if form_dict['maxarea'] != None:
        basic_url+=f"&maxtarea={form_dict['maxarea']}"
    
    if form_dict['min_living_area'] != None:
        basic_url+=f"&minlarea={form_dict['min_living_area']}"
    if form_dict['max_living_area'] != None:
        basic_url+=f"&maxlarea={form_dict['max_living_area']}"

    if form_dict['min_kitchen_area'] != None:
        basic_url+=f"&minkarea={form_dict['min_kitchen_area']}"
    if form_dict['max_kitchen_area'] != None:
        basic_url+=f"&maxkarea={form_dict['max_kitchen_area']}"
    
    if form_dict['minfloor'] != None:
        basic_url+=f"&minfloor={form_dict['minfloor']}"
    if form_dict['maxfloor'] != None:
        basic_url+=f"&maxfloor={form_dict['maxfloor']}"

    if form_dict['floor_type']!=None:
        if form_dict['floor_type'] == 'Не первый':
            basic_url+=f'&is_first_floor=1'
        elif form_dict['floor_type'] == 'Только последний':
            basic_url+=f'&floornl=0'
        elif form_dict['floor_type'] == 'Не последний':
            basic_url+=f'&floornl=1'

    if form_dict['min_house_year'] != None:
        basic_url+=f"&min_house_year={form_dict['min_house_year']}"
    if form_dict['max_house_year'] != None:
        basic_url+=f"&max_house_year={form_dict['max_house_year']}"
    return basic_url
def get_figure(df):
    fig = go.Figure()
    fig = px.scatter_mapbox(
        df,
        lon='lon',
        lat='lat',
        custom_data=['address','price','url']
     )
    fig.update_traces(
            hovertemplate='<br>' +
            'Адрес: %{customdata[0]}' + '<br>' +
            'Цена: %{customdata[1]}' + '<br>' +
            'Ссылка: %{customdata[2]}' + '<br>' +
            '<extra></extra>'
    )

    fig.update_layout(
        mapbox = dict(center = go.layout.mapbox.Center(lat=df['lat'].median(), lon=df['lon'].median()), zoom=7,style = 'carto-positron'),
        title = 'Title',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

form = ['rooms','region','object_type','minprice','maxprice','minarea','maxarea','min_living_area','max_living_area',
        'min_kitchen_area','max_kitchen_area','minfloor','maxfloor','floor_type','min_house_year','max_house_year']
@app.callback(Output('mortgage','children'),
              Input('count', 'n_clicks'),
              State('rooms', 'value'),
              State('region', 'value'),
              State('object_type','value'),
              State('minprice','value'),
              State('maxprice','value'),
              State('minarea','value'),
              State('maxarea','value'),
              State('min_living_area','value'),
              State('max_living_area','value'),
              State('min_kitchen_area','value'),
              State('max_kitchen_area','value'),
              State('minfloor','value'),
              State('maxfloor','value'),
              State('floor_type','value'),
              State('min_house_year','value'),
              State('max_house_year','value'),
              State('mortgage_type','value'),
              State('down_payment','value'),
              State('salary','value'),
              State('percent_on_mortgage','value')
              )
def get_map(clicks,rooms,region,object_type,minprice,maxprice,minarea,maxarea,min_living_area,max_living_area,
        min_kitchen_area,max_kitchen_area,minfloor,maxfloor,floor_type,min_house_year,max_house_year,mortgage_type,down_payment,salary,percent_of_mortgage):
    if clicks != None:
        form_dict = {item:None for item in form} 
        form_dict['rooms'] = rooms
        form_dict['region'] = region
        form_dict['object_type'] = object_type
        form_dict['minprice'] = minprice
        form_dict['maxprice'] = maxprice
        form_dict['minarea'] = minarea
        form_dict['maxarea'] = maxarea
        form_dict['min_living_area'] = min_living_area
        form_dict['max_living_area'] = max_living_area
        form_dict['min_kitchen_area'] = min_kitchen_area
        form_dict['max_kitchen_area'] = max_kitchen_area
        form_dict['minfloor'] = minfloor
        form_dict['maxfloor'] = maxfloor
        form_dict['floor_type'] = floor_type
        form_dict['min_house_year'] = min_house_year
        form_dict['max_house_year'] = max_house_year
        url = get_url(form_dict)
        #print(url)
        p = subprocess.Popen(f'cd spider_cian && python temp.py "{url}"', stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        out = out.decode('cp1251')
        #print(out)

        ans = list(map(lambda x: x + '}' , out.split('}\r\n')))[:-1]
        flats = []
        for d in ans:
            temp = eval(d)
            temp['lon'] = temp['coordinates']['lng']
            temp['lat'] = temp['coordinates']['lat']
            del temp['coordinates']
            flats.append(temp)
        df = pd.DataFrame.from_records(flats)
        if df.empty:
            return  html.Label('Подходящие квартиры не найдены')
        df['price'] = df['price'].astype('int')
        #print(df.info())
        fig = get_figure(df)

        mortgage_info = dict()
        loan_program = 0
        if mortgage_type == 'Ипотека для семьи с детьми':
            loan_program = 3
        elif mortgage_type == 'Ипотека для ИТ специалистов':
            loan_program = 4
        elif mortgage_type == 'Стандартная ипотека':
            if object_type == None or object_type == 'Новостройка':
                loan_program = 1
            else:
                loan_program = 2
        if loan_program != 0:
            mortgage_info['LoanProgram'] = loan_program
        mortgage_info['PropertyCost'] = df['price'].mean()
        if down_payment != None:
            mortgage_info['InitialFee'] = down_payment
        #print(mortgage_info)
        
        #print(banks.request(mortgage_info))
        dcc.Graph(figure = fig)
        return html.Div([
            dbc.Row([dcc.Graph(figure = fig,id = 'map')]),
            html.Label(f'Средняя стоимость квартиры = {round(df.price.mean())}',id = 'mean'),
            dbc.Row(html.Div(),id = 'banks')
        ])
    else:
        return  html.Label()

@app.callback([Output('banks','children'),
               Output('mean','children')],
              [
              Input('map', 'selectedData'),
              State('mortgage_type','value'),
              State('down_payment','value'),
              State('salary','value'),
              State('percent_on_mortgage','value'),
              State('mean','children')]
              )
def change_banks_info(selectedData,mortgage_type,down_payment,salary,percent_on_mortgage,mean):
    if selectedData is not None:
        if len(selectedData['points'])>0:
            point_data = selectedData['points']
            mortgage_info = dict()
            loan_program = 0
            if mortgage_type == 'Ипотека для семьи с детьми':
                loan_program = 3
            elif mortgage_type == 'Ипотека для ИТ специалистов':
                loan_program = 4
            elif mortgage_type == 'Стандартная ипотека':
                if object_type == None or object_type == 'Новостройка':
                    loan_program = 1
                else:
                    loan_program = 2
            if loan_program != 0:
                mortgage_info['LoanProgram'] = loan_program
            mean_price = round(np.mean(list(map(lambda x: x['customdata'][1],point_data))))
            mortgage_info['PropertyCost'] = mean_price
            if down_payment != None:
                mortgage_info['InitialFee'] = down_payment
            print(mortgage_info)
            print(banks.request(mortgage_info))
            return html.Div(),f'Средняя стоимость квартиры = {mean_price}'
    return html.Div(),mean
app.run_server(debug=True) 