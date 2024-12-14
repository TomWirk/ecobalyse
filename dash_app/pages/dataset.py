import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go

import numpy as np 
dash.register_page(__name__, path='/dataset', name="Dataset 📋")

####################### LOAD DATASET #############################
data = pd.read_csv("ecobalyse_data_transformed.csv")

data['mass'] = pd.to_numeric(data['mass'], errors='coerce')
data = data.replace(np.nan, 0, regex=True)
####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(data=data.to_dict('records'),
                         page_size=20,
                         style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
                         style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                        ),
])