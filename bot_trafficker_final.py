# Getting all the libraries 

import os

# -- Libraries to use for data manipulation, cleaning and visualization ...
from random import sample, choice
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -- Dash Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output

# MAP
# -- You'll need a API Token to display the map, visit MAPBOX to create an account ...
# --  Inputting mapbox's api token

# DATA INGESTION
data = pd.read_excel('c:\\Users\\Eduardo\\Documents\\Ironhack\\Assignments\\Capstone Project\\data_homologada.xlsx')
data["TIME_DEL"] = pd.to_datetime(data["TIME_DEL"])
data["TIME_SHIPPED"] = pd.to_datetime(data["TIME_SHIPPED"])
data["TRACK"] = [f"T{i}" for i in range(len(data["TRACK"]))] #data["TRACK"].astype(str)
data["METRIC"] = abs(data["TIME_DEL"] - data["TIME_SHIPPED"])
data["METRIC"] = data["METRIC"].dt.days

# CREATING DASHBOARD
mapbx_api = "pk.eyJ1Ijoiam9zZS1neiIsImEiOiJja2l2M3B4ZGswZ21iMnNwZ283Y2lvdjlwIn0.Bp8yEEwlAR9ZDLzpwzOtxw" #password(text = 'MAPBOX API TOKEN', title = 'MAPBOX API TOKEN', mask = '*') # 

def update_graphs(token):

    plot = data.copy()

    mapBot = px.scatter_mapbox(plot, lat="LAT_DEL", lon="LONG_DEL", color="STATUS", size = "METRIC", zoom=2, mapbox_style="open-street-map")
    mapBot.update_layout(mapbox_accesstoken = token, height=700)
    metricBar = px.bar(plot, x="TRACK", y="METRIC", color="PROVIDER")

    return mapBot, metricBar

mapBot, metricBar = update_graphs(mapbx_api)

style1 = {'font-family': 'Roboto', 'font-size': '125%'}
style0 = {'text-align':'center','font-family': 'Arial', 'font-size': '100%', 'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}

app = dash.Dash(__name__, title='Track&Trace', update_title='Cargando...', external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)


server = app.server


app.layout = html.Div(html.Center(html.Div([
    html.Div(html.P()),
    html.Div([
        html.Div([],
            style = {'width': '20%', 'display': 'inline-block', 'align-items': 'left','vertical-align': 'middle'}
            ),
        html.Div(dcc.Markdown('## **BotTrafficker**'),
            style = style0
            )
        ],
        style = {'vertical-align': 'middle'}
        ),
    html.Div(html.P(dcc.Markdown(" "))),
    dcc.Tabs([
        dcc.Tab(label='Data',
            style = style1,
            selected_style = style1,
            children=[
                html.Div([
                    dt.DataTable(
                        id = 'table_raw',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data = data.to_dict('records')
                        )]#, style = {'width': '50%', 'display': 'inline-block'}
                    )
                    ]
            ),
        dcc.Tab(label='Dashboard',
            style = style1,
            selected_style = style1,
            children=[
                html.Div([
                    dcc.Graph(
                        id = 'map_bot',
                        figure = mapBot
                        )]
                    ),
                    dcc.Graph(
                        id = 'metric_bar',
                        figure = metricBar
                    )
                    ]
        )])])))

"""def update_graphs():

    plot = data.copy()

    mapBot = px.scatter_mapbox(plot, lat="LAT_DEL", lon="LONG_DEL",  color="STATUS", size = "METRIC", zoom=10, mapbox_style="open-street-map")
    metricBar = px.bar(plot, x="TRACK", y="METRIC", color="PROVIDER")

    return mapBot, metricBar
"""
# Run the App

if __name__ == '__main__':
    app.run_server(debug=True)
    
