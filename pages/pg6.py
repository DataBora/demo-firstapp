from datetime import datetime, date

import pandas as pd
import plotly.express as px
import dash
from dash import Input, Output, callback, html, dcc
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import finnhub

load_figure_template("SUPERHERO")

dash.register_page(__name__, name='Multi-select i korelacija')

education = (pd
             .read_csv("assets/states_all.csv")
             .iloc[:, 1:]
             .rename({
    "AVG_MATH_4_SCORE": "matematika 4ti razred",
    "AVG_MATH_8_SCORE": "matematika 8mi razred",
    "AVG_READING_4_SCORE": "Srpski 4ti razred",
    "AVG_READING_8_SCORE": "Srpski 8mi razred"
}, axis=1)
             .assign(expenditure_per_student=lambda x: x["TOTAL_EXPENDITURE"] / x["GRADES_ALL_G"])
             )

layout = html.Div([
    dbc.Row(html.H1("Obrazovni učinak i rashodi u SAD", style={"text-align": "center"})),
    html.P(children=["Prelaskom kursora preko Dijagrama rasejanja(levo),",html.Br(),
           "možete videti korelaciju troškova na Linijskom grafikonu(desno)"],
           style={"color": "yellow", "textAlign":"center", "font-size":"18",'font-style': 'italic'}),
    html.P("Izaberite X i Y kolonu ispod:",
           style={"color": "yellow", "textAlign":"left", "font-size":"18",'font-style': 'italic'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Markdown("X kolona",style={'color':'yellow', 'text-align':'center'}),
                dcc.RadioItems(
                    id="score-radio",
                    options=["matematika 4ti razred", "matematika 8mi razred", "Srpski 4ti razred", "Srpski 8mi razred"],
                    value="matematika 8mi razred"
                ),
                html.Hr(),
                dcc.Markdown("Y kolona", style={'color':'yellow', 'text-align':'center'}),
                dcc.RadioItems(
                    id="score-radio2",
                    options=["matematika 4ti razred", "matematika 8mi razred", "Srpski 4ti razred", "Srpski 8mi razred"],
                    value="Srpski 8mi razred"
                )], style={'border-radius': '12px'})
        ], width=2),
        dbc.Col(
            dcc.Graph(id="cross-filter-scatter", hoverData={'points': [{'customdata': ['CALIFORNIA']}]}),width=5,
        ),
        dbc.Col(dcc.Graph(id="x-line"),width=5,)
    ])
])


@callback(
    Output("cross-filter-scatter", "figure"),
    Input("score-radio", "value"),
    Input("score-radio2", "value"))
def score_scatter(x, y):
    fig = px.scatter(
        education.query("YEAR == 2013"),
        x=x,
        y=y,
        hover_name="STATE",
        custom_data=["STATE"]
    ).update_layout(
        # title="Plot Title",
        xaxis_title=f"Bodovi iz: {x}",
        yaxis_title=f"Bodovi iz: {y}",
        # legend_title="Legend Title",
        font=dict(
            family="Calibri",
            size=14,
            color="white"
        ))

    return fig


@callback(
    Output("x-line", "figure"),
    Input("cross-filter-scatter", "hoverData"))
def update_line(hoverData):
    state_name = hoverData["points"][0]["customdata"][0]
    df = education.query("STATE == @state_name")

    fig = px.line(
        df,
        x="YEAR",
        y="expenditure_per_student",
        title=f"Troškovi po studentu u {state_name.title()}"
    ).update_xaxes(showgrid=False,).update_layout(
        title={'y': 0.9,
               'x': 0.5,
               'xanchor': 'center',
               },
        xaxis_title="Godina",
        yaxis_title="Troškovi po studentu u hiljadama",
        # legend_title="Legend Title",
        font=dict(
            family="Calibri",
            size=14,
            color="white"
        ))



    return fig