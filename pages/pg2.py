from dash import Dash, html, dcc
from dash import Output, Input, callback, html
import dash
import plotly.express as px
import pandas as pd

from dash_bootstrap_templates import load_figure_template

load_figure_template("SUPERHERO")

dash.register_page(__name__, name='Analiza sudara u Njujorku')



collisions = pd.read_csv("assets/NYC_Collisions.csv")


layout = html.Div([
    html.H2("Analiza sudara u Njujorku", style={'text-align':'center'}),
    html.Br(),
    html.P("U kalendaru ispod možete odabrati datume, da biste videli broj sudara u Opštinama Njujorka",
           style={'color':'yellow'}),
    dcc.DatePickerRange(
        id="dates",
        min_date_allowed = collisions["ACCIDENT_DATE"].min(),
        max_date_allowed = collisions["ACCIDENT_DATE"].max(),
        start_date = collisions["ACCIDENT_DATE"].min(),
        end_date = collisions["ACCIDENT_DATE"].max(),
        display_format="D-MMM-YY",
        style={
            'border-radius': '12px',
            'border': '2px solid #ccc',
            'padding': '6px',
            'color':'white',
           # 'background-color':'mint',
            'font-family': 'Calibri',
            'fontWeight': 'bold'
        }
    ),
    dcc.Graph(id="graph"),

    html.P("Disclaimer: Svi korišćeni podaci su netačni", style={"color":"red"})
])

@callback(
    Output("graph","figure"),
    [Input("dates", "start_date"),Input("dates", "end_date"),]
)

def plot_collision_bar(start_date,end_date):
    fig = px.bar(
        (collisions
         .assign(Broj_Sudara = collisions["COLLISION_ID"],
                Opština = collisions["BOROUGH"])
         .loc[collisions["ACCIDENT_DATE"].between(start_date,end_date)]
         .groupby("Opština")
         .count()
         .reset_index()),
        x="Broj_Sudara",
        y="Opština",
        title = f"Broj sudara u Njujorku između {start_date[:10]} and {end_date[:10]}"
    )

    fig.update_layout(
        font=dict(
            family="Calibri",
            size=14,
            color="white"
    ))
    return fig