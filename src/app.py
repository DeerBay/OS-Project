# Imports of needed libraries
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Df All Athletes
athlete_events = pd.read_csv("../data/final_df.csv")

# Df Swedish Athletes
sweden_athletes = pd.DataFrame(athlete_events[athlete_events["NOC"] == "SWE"])

# Loading template for graphs
load_figure_template("quartz")

# This initializes a Dash web application, 
# applies the "QUARTZ" Bootstrap theme for styling, 
# and includes a viewport meta tag to ensure proper rendering on various devices.
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.QUARTZ],
               meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

# Needs to be included for deploying on render
server = app.server

# Layout for App
app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.H2("Olympic Games Achievements 1896-2016", className="text-center text-primary")),
        ],
        className="mb-3 mt-3", # Adding marginal bottom and top
    ),
    dbc.Row([
            dcc.Dropdown(id='year_dropdown', className='text-info',
                        multi=True, 
                        options=[year for year in sorted(athlete_events['Year'].unique())], 
                        placeholder='Select Year',
                        style={'width':'150px', 'margin-left': '10px', 'margin-right': '10px'},
            ),
            dcc.Dropdown(id='sport_dropdown', className='text-info',
                        multi=True, 
                        options=[sport for sport in sorted(athlete_events['Sport'].unique())], 
                        placeholder='Select Sport',
                        style={'width':'150px', 'margin-left': '10px', 'margin-right': '10px'},

            ),
            dcc.Dropdown(id='season_dropdown', className='text-info',
                        multi=True, 
                        options=[season for season in sorted(athlete_events['Season'].unique())], 
                        placeholder='Select Season',
                        style={'width':'150px', 'margin-left': '10px', 'margin-right': '10px'})

    ], justify='center', class_name="mb-2 ml-50 mr-50"), 

    dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H3("Workning Title Graph One Left", className="text-body-tertiary", id="header_graph_1_left")),
                    dbc.CardBody([
                        dcc.Dropdown(id='country_dropdown_left', 
                                 className='ml-3 mr-3 mb-1 text-info', 
                                 options=[sport for sport in sorted(athlete_events['Sport'].unique())], 
                                 placeholder='Select Sport'),
                                 dcc.Graph(id="graph_1_left", figure={}),
                    ]),
                ],
                className="mb-3",
            ), xs=12, sm=11, md=10, lg=5
        ),
        dbc.Col(  
            dbc.Card(
                [
                    dbc.CardHeader(html.H3("Workning Title Graph One Right", className="text-body-tertiary", id="header_graph_2_right")),
                    dbc.CardBody([
                        dcc.Dropdown(id='country_dropdown_right', 
                                 className='ml-3 mr-3 mb-1 text-info', 
                                 options=[year for year in sorted(athlete_events['Year'].unique())], 
                                 placeholder='Select Year'),
                        dcc.Graph(id="graph_1_right"),
                                  ]),
                ],
                className="mb-3",
            ), xs=12, sm=11, md=10, lg=5
        ),
    ], justify='evenly'),
    dbc.Row([
        dbc.Button("Reset", id='reset-button', className='float-left', n_clicks=0), # Callback to reset page
        dcc.Link("Contributors", href="https://github.com/DeerBay/OS-Project/graphs/contributors", target="_blank"), # "_blank": Opens the linked document in a new tab or window.
    ],style={"margin-top": "20px", "text-align": "center"})
])

@callback(
    Output("graph_1_left", "figure"),
    )

def figure_one(year, country):
    df = athlete_events.query("Year == @year & Country == @country")
    # Dataframe for participants and medals per year
    participants_medals= df.groupby(['Year', 'Season', 'Country', 'Continent','Country_latitude', 'Country_longitude','Continent_latitude', 'Continent_longitude', 'Sport'], as_index=False)[['Name', 'Medal']].agg(
    {'Name': 'nunique', 'Medal': 'count'})
    return ...
    ...

if __name__ == "__main__":
    app.run(debug=True)