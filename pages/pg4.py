import dash
from dash import dcc, html,callback,Output, Input
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
load_figure_template("SUPERHERO")

dash.register_page(__name__, name='GEO Data i rezultati')

education = pd.read_csv("assets/states_all.csv").iloc[:, 1:].rename({
         "AVG_MATH_4_SCORE": "matematika_prosek_4ti_razred",
         "AVG_MATH_8_SCORE": "matematika_prosek_8mi_razred",
         "AVG_READING_4_SCORE": "engleski_prosek_4ti_razred",
         "AVG_READING_8_SCORE": "engleski_prosek_8mi_razred"
}, axis=1)

summary_dataframe = (
    education

    .groupby(["STATE","YEAR"])
    .agg({
        "TOTAL_REVENUE": "sum",
        "TOTAL_EXPENDITURE": "sum",
        "GRADES_ALL_G": "sum",
        "matematika_prosek_8mi_razred": "mean",
        "engleski_prosek_8mi_razred": "mean"
    })
    .assign(per_student_spend = lambda x: x["TOTAL_EXPENDITURE"] / x["GRADES_ALL_G"])
    .reset_index()
)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New_Hampshire": "NH",
    "New_Jersey": "NJ",
    "New_Mexico": "NM",
    "New_York": "NY",
    "North_Carolina": "NC",
    "North_Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode_Island": "RI",
    "South_Carolina": "SC",
    "South_Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West_Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District_Of_Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

summary_dataframe["STATE_CODE"] = summary_dataframe["STATE"].str.title().map(us_state_to_abbrev)

education_2013 = summary_dataframe.query('YEAR == 2013')

layout = html.Div(
    [html.P("Ispod se nalaze 2 zasebna Tab-a koja možete istražiti",
            style={"textAlign":"center","font-size":"23px",'color':'yellow'}),
        html.P("Disclaimer: Svi korišćeni podaci su netačni" ,
               style={"color": "red", "textAlign":"left"}),
       # html.Br(),
        dcc.Tabs(
            id="tabs",
            className="dbc",
            value="tab-1",
            style={"fontSize": 32},
            children=[
                dcc.Tab(
                    label="Nacionalni pregled",
                    value="tab-1",
                    children=[
                        dcc.RadioItems(
                            options=["matematika_prosek_8mi_razred", "engleski_prosek_8mi_razred"],
                            value="matematika_prosek_8mi_razred",
                            id="Metric-Radio",
                            labelStyle={'display': 'inline-block', 'margin': '10px'},
                            inputStyle={'height': '25px', 'width': '25px', 'margin': '0 10px 0 0'},
                            style={'display': 'flex', 'flex-direction': 'row',"color":"white",'fontSize':'40px'},
                            className="dbc"
                        ),
                        html.Br(),
                        dcc.Graph(id="test_score_map")]
                ),
                dcc.Tab(
                    label="Fokus na nivou države",
                    value="tab-2",
                    children=[
                        html.Br(),
                        html.P("Izaberite državu ispod da biste videli kako se rangira:",
                               style={"color": "yellow",
                                      "textAlign":"center",
                                      "font-size":"18px",
                                      'font-style': 'italic'}),
                        html.Br(),
                        dbc.Row(
                            [
                                dcc.Dropdown(
                                    options=[
                                        {"label": state.title(), "value": state}
                                        for state in education["STATE"].unique()
                                    ],
                                    value="ALABAMA",
                                    style={#"background":"white",
                                           "fontColor": "black",
                                           "color": "black",
                                           "font-size":20,
                                           'textAlign': 'center',
                                           'font-weight': 'bold',
                                           },
                                    className="dbc",
                                    id="State Dropdown",
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(id="KPI 1"), style={"textAlign": "center", "fontSize": 24}
                                ),
                                dbc.Col(
                                    dbc.Card(id="KPI 2"), style={"textAlign": "center", "fontSize": 24}
                                ),
                                dbc.Col(
                                    dbc.Card(id="KPI 3"), style={"textAlign": "center", "fontSize": 24}
                                ),
                                dbc.Col(
                                    dbc.Card(id="KPI 4"), style={"textAlign": "center", "fontSize": 24}
                                ),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(dcc.Graph(id="Performance Over Time",style={'width': '90%'})),width=6
                                ),
                                dbc.Col(dbc.Card(dcc.Graph(id="Funding Over Time",style={'width': '90%'})),width=6),
                            ]
                        ),
                    ],
                ),
            ],
        )
    ]
)


@callback(
    Output("test_score_map", "figure"),
    Input("Metric-Radio", "value")
)
def bar_chart(column):
    width = 500
    fig = px.choropleth(
        summary_dataframe,
        locations="STATE_CODE",
        color=column,
        locationmode="USA-states",
        scope="usa",
        title="Pregled rezultata na nacionalnom nivou",
    ).update_layout(
        title_font={"size": 28},
        title={"x": .5},
        margin={"r": 50, "t": 50, "l": 20, "b": 20},
        coloraxis_colorbar={"x": .8}

    )

    return fig


@callback(
    Output("KPI 1", "children"),
    Output("KPI 2", "children"),
    Output("Performance Over Time", "figure"),
    Output("Funding Over Time", "figure"),
    Input("State Dropdown", "value"),
)
def other_func(state):
    if not state:
        raise PreventUpdate
    markdown_title = f"{state.title()}"
    kpi_1 = f"""Matematika 8mi razred 
            Poena:{int(education_2013.query('STATE == @state').matematika_prosek_8mi_razred.values)}"""
    kpi_2 = f"""Engleski 8mi razred 
            Poena:{int(education_2013.query('STATE == @state').engleski_prosek_8mi_razred.values)}"""

    line_df = education.query(f"STATE == '{state}'").sort_values("YEAR")

    line = px.line(
        line_df,
        x="YEAR",
        y="GRADES_ALL_G",
        title="Izlaznost",
    ).update_layout(
        title_font={"size": 20},
        title={"x": .5},
        font=dict(
            color="white"),
        xaxis_title="Godina",
        yaxis_title="Broj đaka",
    )

    bar_df = education.query("YEAR in [1992, 2019] and STATE == @state")
    bar = px.bar(
        bar_df,
        x="YEAR",
        y=["matematika_prosek_4ti_razred", "matematika_prosek_8mi_razred"],
        barmode="group",
        title="Rezultati ispita 1992 vs 2019",
    ).update_layout(
        title_font={"size": 20},
        title={"x": .5},
        xaxis_title="Godina",
        yaxis_title="Broj poena",
        # legend_title="Legend Title",
        font=dict(
            color="white"),
        legend={
            "title": None,
            "x": 0,
            "y": 1.1,
           #            "orientation": "h",
            "xanchor": "right",
        }
    )

    return kpi_1, kpi_2, line, bar