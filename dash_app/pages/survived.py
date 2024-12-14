import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np 

dash.register_page(__name__, path='/Categorial', name="Pie Chart 📊")

####################### DATASET #############################
data = pd.read_csv("ecobalyse_data_transformed.csv")
data['mass'] = pd.to_numeric(data['mass'], errors='coerce')
data = data.replace(np.nan, 0, regex=True)

data = data[data["mass"] != 0]
####################### BAR CHART #############################
def create_pie_chart(colnames="business"):
    values = data[colnames].value_counts().values
    labels = data[colnames].value_counts().index

    fig = px.pie(data ,values = values, names = labels)
    ## return  fig
    return fig

####################### WIDGETS ################################
colnames = ["business", 
            "countryDyeing", 
           "countryFabric",
           "countryMaking", 
           "countrySpinning", 
           "fabricProcess", 
          "makingComplexity",
          "product",
          "traceability", 
         "upcycled"]
dd = dcc.Dropdown(id="dcc_id", options=colnames, value="business", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dd, 
    dcc.Graph(id="bar_chart")
])

####################### CALLBACKS ################################
@callback(Output("bar_chart", "figure"), 
          [Input("dcc_id", "value")])
def update_bar_chart(sel_col):
    return create_pie_chart(sel_col)