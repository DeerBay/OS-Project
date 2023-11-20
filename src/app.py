from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

# Df All Athletes
athlete_events = pd.read_csv("../data/athlete_events.csv")

# Df Swedish Athletes
sweden_athletes = pd.DataFrame(athlete_events[athlete_events["NOC"] == "SWE"])

load_figure_template("quartz")

# This initializes a Dash web application, 
# applies the "QUARTZ" Bootstrap theme for styling, 
# and includes a viewport meta tag to ensure proper rendering on various devices.
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.QUARTZ],
               meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

server = app.server

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.H2("Olympic Games Achievements 1896-2016", className="text-center text-primary")),
        ],
        className="mb-3 mt-3", # Adding marginal bottom and top
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H3("Workning Title Graph One", className="text-body-tertiary", id="header_graph_1")),
                    dbc.CardBody(dcc.Graph()),
                ],
                className="mb-3",
            ), xs=12, sm=11, md=10, lg=5
        ),
        dbc.Col(  
            dbc.Card(
                [
                    dbc.CardHeader(html.H3("Workning Title Graph Two", className="text-body-tertiary", id="header_graph_2")),
                    dbc.CardBody(dcc.Graph()),
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

app.run(debug=True)