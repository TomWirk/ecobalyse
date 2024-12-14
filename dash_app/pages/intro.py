import dash
from dash import html

dash.register_page(__name__, path='/', name="Introduction 😃")

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Div(children=[
        html.H2("Ecobalyse database"),
        "Faire de la description des données",
        html.Br(),html.Br(),
        "Faire la description des données",
        html.Br(), html.Br(),
        
    ]),
    html.Div(children=[
        html.Br(),
        html.H2("Variables du dataset")
    ])
], className="bg-light p-4 m-2")