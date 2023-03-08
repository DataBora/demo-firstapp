import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import numpy as np
import pandas as pd

dash.register_page(__name__, name='Info po regijama')

load_figure_template("SUPERHERO")

# page 1 data
df = px.data.gapminder()

layout = html.Div(
    children=[html.H2(f"Prosečan životni vek prema Geo-Lokaciji", style={"textAlign":"center"}),
        html.Br(),
        html.P("Koristite Radio-Dugme ispod da biste izabrali regiju:",
              style={"textAlign":"left",'font-style': 'italic','color':'yellow'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.RadioItems(options=df.continent.unique(),
                                       id='cont-choice',
                                       labelStyle={'display': 'block', 'margin': '10px'},
                                       inputStyle={'height': '25px', 'width': '25px', 'margin': '0 10px 0 0'},
                                       style={'display': 'flex', 'flex-direction': 'row',"color":"white",'fontSize':'40px'}
                                       )
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                                  figure=px.histogram(df, x='continent',
                                                      y='lifeExp',
                                                      histfunc='avg'),
                                  style={'height': '420px', 'width': '1000px'}),
                        html.P("Disclaimer: Svi korišćeni podaci su netačni", style={"color":"red"}),
                    ], width=12
                )
            ]
        )
    ]
)


@callback(
    Output('line-fig', 'figure'),
    Input('cont-choice', 'value')
)
def update_graph(value):
    if value is None:
        fig = px.histogram(df, x='continent', y='lifeExp', histfunc='avg')
    else:
        dff = df[df.continent==value]
        fig = px.histogram(dff, x='country', y='lifeExp', histfunc='avg')
    fig.update_layout(
        #title="Plot Title",
        xaxis_title="Geo Lokacija",
        yaxis_title="Prosečan broj godina",
        #legend_title="Legend Title",
        font=dict(
            family="Calibri",
            size=18,
            color="white"
    ))
    return fig