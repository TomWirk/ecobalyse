import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np


dash.register_page(__name__, path='/relaship', name="Relationship 📈")


####################### DATASET #############################
data = pd.read_csv("ecobalyse_data_transformed.csv")
data['mass'] = pd.to_numeric(data['mass'], errors='coerce')
data = data.replace(np.nan, 0, regex=True)
data = data[data["mass"] !=0]
####################### SCATTER CHART #############################
def create_scatter_chart(x_axis="acd", y_axis="cch"):
    return px.scatter(data_frame=data, x=x_axis, y=y_axis, height=600)

####################### WIDGETS #############################
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

colnames= data.select_dtypes(include=numerics).columns


x_axis = dcc.Dropdown(id="x_axis", options=colnames, value="acd", clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=colnames, value="cch", clearable=False)

####################### Pacd LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    "X-Axis", x_axis, 
    "Y-Axis", y_axis,
    dcc.Graph(id="scatter")
])

####################### CALLBACKS ###############################
@callback(Output("scatter", "figure"), 
          [Input("x_axis", "value"),
           Input("y_axis", "value")])
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)