import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SUPERHERO],
                suppress_callback_exceptions=True)
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="dbc",
                                 style={'border': '2px solid #FFF',
                                        'padding': '10px',
                                        'border-radius': '10px',
                                        'text-align':'center'}),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="dbc",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
                [
                    html.Img(src='assets/Logobela.png',
                             style={'width': '100%',
                                    'margin': 'auto',
                                    'display': 'block'
                                    },),
                    html.P("www.BizAnaliza.com",
                           style={ "color": "lightgrey",
                                  "font-size":"12px",
                                  "display":"inline",
                                  "text-align": "center",
                                  'font-family':'Calibri',
                                  }),
                    html.P(" Borivoj_Grujičić_MBE",
                           style={"color": "lightgrey",
                                  "font-size":"12px",
                                  "display":"inline",
                                  "text-align": "center",
                                  'font-family':'Calibri',
                                  }),
                ], width=1,
            ),

        dbc.Col(html.Div("DEMO Aplikacija",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=False)