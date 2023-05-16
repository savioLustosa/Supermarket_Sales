import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
#from app import *
 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

load_figure_template("MINTY")

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY]
)

server = app.server

df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])


List_city = df_data["City"].value_counts().index

# =========  Layout  =========== #
app.layout =html.Div([

    dbc.Row([
        

        dbc.Col([
            dbc.Card([
                html.H2("Sales", style={"font-family":"Voltaire","font-size":"40px"}),
                html.Hr(),

                html.H5("Cidades: ", style={"margin-top":"20px"}),
                dcc.Checklist(List_city, List_city, id="ckeck_city",#inline=True,
                inputStyle={"margin-right":"5px","margin-left":"10px"}),
                
                html.H5("Variável de análise: ", style={"margin-top":"20px"}),
                dcc.RadioItems(["gross income","Rating"], "gross income", id="main_variable",#),inline=True),
                inputStyle={"margin-right":"5px","margin-left":"10px"}),

                   ],style={"height":"80vh","margin":"5px","padding":"20px"}),

                dbc.Row([html.H3("Desenvolvido Por:", style={"margin-left": "5px","font-size":"19px"})]),

                dbc.Row([html.H2("Savio Lustosa",
                style={"font-size":"15px","margin-left":"8px"})]),

                ],md=2, sm=2),

            

        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id="city_fig")], sm=4),
                dbc.Col([dcc.Graph(id="gender_fig")],  sm=4),
                dbc.Col([dcc.Graph(id="pay_fig")],  sm=4),
            ]),
            dbc.Row([dcc.Graph(id="income_per_date_fig")]),

            dbc.Row([dcc.Graph(id="income_per_product_fig")]),

   
        ],md=10, sm=10)
    ])           
])
# =========  Callbacks  =========== #                    
@app.callback(
    [
        Output('city_fig', 'figure'),
        Output('gender_fig', 'figure'),
        Output('pay_fig', 'figure'),
        Output('income_per_date_fig', 'figure'),
        Output('income_per_product_fig', 'figure'),
    ],

    [
        Input('ckeck_city', 'value'),
        Input('main_variable', 'value')
    ])

def render_graphs(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(["Gender", "City"])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby("Date")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line","City"])[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x = 'City', y = main_variable)
    fig_gender = px.bar(df_gender, y = main_variable, x='Gender', color= "City", barmode="group")
    fig_payment = px.bar(df_payment, y = 'Payment', x = main_variable, orientation="h")
    fig_product_line = px.bar(df_product_income, x = main_variable, y = "Product line", color="City", orientation= "h")
    fig_income_date = px.bar(df_income_time, y = main_variable, x = "Date")

    for fig in [fig_city, fig_payment, fig_gender, fig_income_date]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='MINTY'),

    
    fig_product_line.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=400)

    return fig_city, fig_gender,fig_payment, fig_income_date, fig_product_line

# =========  Servidor  =========== #
if __name__ == "__main__":
    app.run_server(port=8050, debug=True)

#if __name__ == '__main__':
 #   app.run_server(debug=False,port=8080,host='0.0.0.0')