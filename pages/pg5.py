import dash
from dash import dcc, html, dash_table
from dash_bootstrap_templates import load_figure_template

import pandas as pd
load_figure_template("SUPERHERO")

dash.register_page(__name__, name='Tabularni prikaz')

df = pd.read_excel("assets/vehiclesforapp.xlsx")

style = {
    'backgroundColor': 'rgb(69, 72, 77)',
    'color': 'white',
    'font-family': "TimesNewRoman",
    'textAlign': 'left',
}

layout = html.Div(style={"textAlign": "center"},
        children=[
            dcc.Markdown('''
                    # Tabularni prikaz za samostalno filtriranje i sortiranje
                       ''' ),
            dcc.Markdown('''
                    #### Tabelu ispod možete: 

                    ''',
                         style={'text-align':'left','font-size':'15px'}
                         ),
            dcc.Markdown('''
                     ***Filtrirati,***
                     ***Sortirati,***  i zatim
                     ***Export-ovati*** (*.xlsx*)

                    ''',
                         style={'text-align':'left','font-size':'15px', 'color':'yellow'}
                         ),
            dcc.Markdown('''
                     *Napomena: Tabela je "Case-Sensitive"*

                    ''',
                         style={'text-align':'left','font-size':'9px', 'color':'white'}
                         ),
            html.P("Disclaimer: Svi korišćeni podaci su netačni", style={"color": "red","textAlign":"left"}),
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                export_format="xlsx",
                style_header={'backgroundColor': 'rgb(30, 30, 30)',
                              'fontWeight': 'bold',
                              'fontSize': '15px',
                              'color': 'white',
                              'text-align':'center'},
                style_data=style,
                export_headers='display',
                export_columns='all',
                style_cell={
                     'padding': '2px'
                            },
                css=[
                    {
                     'selector': '.export',
                     'rule': 'font-size: 18px; height: 40px; width: 100px; font-weight: bold; '
                            'color: white; background-color: green; border-radius: 12px'},
                ],


    )

])