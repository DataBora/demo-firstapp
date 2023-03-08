#API dashboard

import dash
from dash import Input, Output, callback, dcc, html
import plotly.express as px
import pandas as pd
from sodapy import Socrata
from dash_bootstrap_templates import load_figure_template

load_figure_template("SUPERHERO")

dash.register_page(__name__, path='/', name='UŽIVO analiza podataka')# '/' is home page

# Connect to Socrata API
socrata_domain = 'www.dallasopendata.com'
socrata_dataset_identifier = 'qgg6-h4bd'
client = Socrata(socrata_domain, app_token="xY8Qbydu8WohLxtzLjO4gyEbg")

# # pull the data from Socrata API
# results = client.get(socrata_dataset_identifier)
# # Convert data into a pandas dataframe
# df = pd.DataFrame(results)
#
# df["intake_time"] = pd.to_datetime(df["intake_time"])
# df["intake_time"] = df["intake_time"].dt.hour
# df["animal_stay_days"] = df["animal_stay_days"].astype(int)
# print(df.head())
# exit()


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
#                 suppress_callback_exceptions=True)

layout = html.Div([
    html.H1("UŽIVO: podaci iz azila za životinje u Dalasu(USA)", style={"textAlign":"center"}),
    html.P("Ovaj izveštaj se obnavlja jednom dnevno, sa online Baze podataka u Dalasu",
           style={"textAlign":"center", "color":"white","font-size":"18px",'font-style': 'italic'}),
    html.P("Isto ovako, možemo se povezati na Vašu bazu podataka(SQl, Cloud...), i uživo analizirati podatke.",
           style={"textAlign":"center", "color":"yellow", "font-size":"20px"}),
    html.P("Podaci se mogu obnavljati na 5,10,15,20...minuta ili na duži vremenski period.",
           style={"textAlign":"center", "color":"yellow", "font-size":"20px"}),
    html.Hr(),
    html.P("Izaberite životinju:",style={"textAlign":"left", "font-size":"18px"}),
    html.Div(html.Div(id="drpdn-div", children=[], className="two columns"),className="row"),

    dcc.Interval(id="timer", interval=93600 * 1000, n_intervals=0),
    dcc.Store(id="stored", data={}),

    html.Div(id="output-div", children=[]),
])


@callback(Output("stored", "data"),
          Output("drpdn-div", "children"),
          Input("timer","n_intervals")
)
def get_drpdn_and_df(n):
    results = client.get(socrata_dataset_identifier)
    # Convert data into a pandas dataframe
    df = pd.DataFrame(results)
    df["intake_time"] = pd.to_datetime(df["intake_time"])
    df["intake_time"] = df["intake_time"].dt.hour
    df["animal_stay_days"] = df["animal_stay_days"].astype(int)
    # print(df.iloc[:, :4].head())

    return df.to_dict('records'), dcc.Dropdown(id='animal-type',
                                               clearable=False,
                                               value="CAT",
                                               options=[{'label': x, 'value': x} for x in
                                                        df["animal_type"].unique()],
                                               style={"background": "white",
                                                      "fontColor": "black",
                                                      "color": "black",
                                                      'font-weight': 'bold',
                                                      'width': '150px',
                                                      "font-size": 20,
                                                      'textAlign': 'center',
                                                      'border-radius': '12px'},
                                               )


@callback(Output("output-div", "children"),
              Input("animal-type", "value"),
              Input("stored", "data"),
)
def make_bars(animal_chosen, data):
    df = pd.DataFrame(data)

    # HISTOGRAM
    df_hist = df[df["animal_type"]==animal_chosen]
    fig_hist = px.histogram(df_hist, x="animal_breed")
    fig_hist.update_xaxes(categoryorder="total descending")

    # STRIP CHART
    fig_strip = px.strip(df_hist, x="animal_stay_days", y="intake_type")

    # SUNBURST
    df_sburst = df.dropna(subset=['chip_status'])
    df_sburst = df_sburst[df_sburst["intake_type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
    fig_sunburst = px.sunburst(df_sburst, path=["animal_type", "intake_type", "chip_status"])

    # Empirical Cumulative Distribution
    df_ecdf = df[df["animal_type"].isin(["DOG","CAT"])]
    fig_ecdf = px.ecdf(df_ecdf, x="animal_stay_days", color="animal_type")

    # LINE CHART
    df_line = df.sort_values(by=["intake_time"], ascending=True)
    df_line = df_line.groupby(
        ["intake_time", "animal_type"]).size().reset_index(name="count")
    fig_line = px.line(df_line, x="intake_time", y="count",
                       color="animal_type", markers=True)

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns", style={'width': '50%'}),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns", style={'width': '50%'}),
        ], className="row"),
        html.Br(),
        html.H2("SVE ŽIVOTINJE", style={"textAlign":"center"}),
        html.P("Kliknite na 'Pie' grafikon za detaljnije informacije", style={"textAlign": "left", 'color':'yellow'}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns", style={'width': '50%'}),
            html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns", style={'width': '50%'}),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
        ], className="row"),
    ]
