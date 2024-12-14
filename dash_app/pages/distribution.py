import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np

dash.register_page(__name__, path='/distribution', name="Distribution 📊")

####################### LOAD DATASET #############################
data = pd.read_csv("ecobalyse_data_transformed.csv")
data['mass'] = pd.to_numeric(data['mass'], errors='coerce')
data = data.replace(np.nan, 0, regex=True)
## Select the numerical columns
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

####################### HISTOGRAM ###############################
def create_distribution(col_name="acd"):
    return px.histogram(data_frame=data, x=col_name, height=600)

####################### WIDGETS ################################
colnames = data.select_dtypes(include=numerics).columns
print(colnames)
dd = dcc.Dropdown(id="dist_column", options=colnames, value="acd", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])

####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column):
    return create_distribution(dist_column)