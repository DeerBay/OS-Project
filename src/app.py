# Imports of needed libraries
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash_bootstrap_templates import load_figure_template

############### Preparation of dataframes for the app ###############

# Read the required datafiles for the app
athlete_events = pd.read_csv("../data/final_df.csv", low_memory=False)
gender_ratios = pd.read_csv("../data/gender_ratios.csv")

# Changing the NaN values in the Medal column to "No Medal"
athlete_events['Medal'] = athlete_events['Medal'].fillna('No Medal')
# Creating column Number of Medals and mapping the Medal column to values of 1 for medal and 0 for NaN value
athlete_events['Number of Medals'] = athlete_events['Medal'].map({'Gold': 1, 'Silver': 1, 'Bronze': 1, 'No Medal': 0})

# Grouping to get the final dataframe for the app - sum of participants and number of medals count for the desired columns
grouped_final_athlete_events = athlete_events.groupby(['Year','Season', 'Medal', 'Country', 'Sport', 'Country_latitude', 'Country_longitude']).agg({
    'Participants': 'nunique',
    'Number of Medals': 'sum'}).reset_index()



############### Creating the app ###############

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
app.layout = dbc.Container([

    ################# Header ##################
    dbc.Row(
        [html.H1("Olympic Games Achievements 1896-2016", className="text-center text-primary")],
        className="mb-3 mt-3", # Adding marginal bottom and top
    ),
    ################# Dropdown row ##############
    dbc.Row(
    [
        dbc.Col(
            dcc.Dropdown(
                id='year_dropdown',
                className='text-info mt-1',
                multi=True, 
                options=[{'label': year, 'value': year} for year in sorted(athlete_events['Year'].unique())], 
                placeholder='Select Year',
                style={'width': '100%'},
            ),
            xs=12, sm=6, md=4, lg=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id='sport_dropdown',
                className='text-info mt-1',
                multi=True, 
                options=[{'label': sport, 'value': sport} for sport in sorted(athlete_events['Sport'].unique())], 
                placeholder='Select Sport',
                style={'width': '100%'},
            ),
            xs=12, sm=6, md=4, lg=3
        ),
        dbc.Col(
            dcc.Dropdown(
                id='season_dropdown',
                className='text-info mt-1',
                multi=True, 
                options=['Summer', 'Winter'], 
                placeholder='Select Season',
                style={'width': '100%'},
            ),
            xs=12, sm=6, md=4, lg=3
        ),
    ],
    justify='center',
    style={'margin-left': '10px', 'margin-right': '10px'},
    className="sticky-top mb-2" #Sticky-top to fix it to the top of the window
),

    ############# Graphs ################

    dbc.Row([
        dbc.Col(
            dbc.Card([ # To make a "card" or a frame to the object inside
                    dbc.CardHeader(html.H3("Medals All Countries", className="text-body-tertiary", id="header_graph_all_countries")),
                    dbc.CardBody([
                    dcc.Dropdown(id='country_dropdown_right', 
                    className='mb-1 mt-1 text-info', 
                    options=[
                    {'label': 'Sort by Sports', 'value': 'Sport'},
                    {'label': 'Sort by Countries', 'value': 'Country'}],
                    placeholder='Sort by Country or Sport',
                    style={'width': '100%'},
            ), 
                        dcc.Graph(id="graph_all_countries_sunburst", figure={}),
                        ])
            ], className="mb-3"
            ),xs=12, sm=11, md=10, lg=5
        ),
        dbc.Col(
            dbc.Card([
                    dbc.CardHeader(html.H3("Medals Sweden", className="text-body-tertiary", id="header_graph_sweden")),
                    dbc.CardBody([
                        dcc.Dropdown(
                        id='sport_or_medal_dropdown', 
                        className='text-info mt-1 mb-1', 
                        options=[
                            {'label': 'Sort by Sports', 'value': 'Sports'},
                            {'label': 'Sort by Medals', 'value': 'Medals'}
                        ], 
                        placeholder='Sort by Sports or Medals',
                        style={'width': '100%'}),
                        dcc.Graph(id="graph_sweden_sunburst", figure={}),
                        ]), 
            ], className="mb-3"
            ),xs=12, sm=11, md=10, lg=5
        ),
    ], justify='evenly', className="container-fluid"),  # Added container-fluid class for better responsiveness

    dbc.Row([
        dbc.Col(
            dbc.Card([
                    dbc.CardHeader(html.H3("Sweden top 10 all Medals", className="text-body-tertiary", id="header_graph_sweden_top10")),
                    dbc.CardBody([
                                 dcc.Graph(id="graph_sweden_top10", figure={}),
                    ]),
                ],
                className="mb-3",
            ), xs=12, sm=11, md=10, lg=5
        ),
        dbc.Col(
            dbc.Card([
                    dbc.CardHeader(html.H3("Sweden top 10 Gold Medals", className="text-body-tertiary", id="header_graph_sweden_gold")),
                    dbc.CardBody([
                                 dcc.Graph(id="graph_sweden_gold", figure={}),
                    ]),
                ],
                className="mb-3",
            ), xs=12, sm=11, md=10, lg=5
        ),
    ], justify='evenly', className="container-fluid mb-3"),  # Added container-fluid class for better responsiveness

 ############## Mapbox Graphs ###############
    dbc.Row([
            html.H4("Number of Participants and Medals by Country"),
            dcc.Graph(
                id="graph_mapbox_2",    
                figure={}, 
            ),
        ], className="mx-2 mb-3"),

     dbc.Row([
            html.H4("Number of Participants and Gender Distribution by Country"),
            dcc.Dropdown(
                id='country_dropdown_left', 
                className='mb-1 text-info', 
                options=["Medals", "Gender ratio"], 
                placeholder='Sort by medals or gender ratio',
                style={'width': '260px'},
            ),
            dcc.Graph(
                id="graph_gender_or_medals_mapbox", 
                figure={}
            ),
        ],className="mx-2 mb-3"),
  
  ########## Reset button and link to GitHub ##############
    dbc.Row([
            dbc.Button("Reset", 
                    id='reset-button', 
                    #href="https://iths-olympics.onrender.com",   
                    title='Resets all graphs',
                    style={'width': '150px'}), # Hover text

            dcc.Link("Contributors", 
                    href="https://github.com/DeerBay/OS-Project/graphs/contributors", 
                    target="_blank", # "_blank": Opens the linked document in a new tab or window.
                    title='Link to repository on GitHub',
                    className='text-center'), 
        ],className='mb-3', justify='center'),

], 
fluid=True
) # End of container

############ Callback Decoraters to define functions ############ 



# Figure one; Sunburst graph sorted by number of medals per country per sport/year
@callback(
    Output("graph_all_countries_sunburst", "figure"),
    Input("year_dropdown", "value"),
    Input("sport_dropdown", "value"),
    Input("country_dropdown_right", "value"),

)
def figure_one(years, sports, sort):
    if sort == "Sport" or sort in [None, "", []]:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.sunburst(grouped_final_athlete_events.sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80), values='Number of Medals', path=['Sport', 'Country'], title= "Medals and sports for all countries")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.query("Year==@years").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            fig = px.sunburst(df, values='Number of Medals', path=['Sport', 'Country'], title= "Medals and sports for all countries")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Sport==@sports").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            fig = px.sunburst(df, values='Number of Medals', path=['Sport', 'Country'], title= "Medals and sports for all countries")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Year==@years").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            df = df.query("Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Sport', 'Country'], title= "Medals and sports for all countries")
    else:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.sunburst(grouped_final_athlete_events.sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80), values='Number of Medals', path=['Country', 'Sport'], title= "Medals and sports for all countries")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.query("Year==@years").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            fig = px.sunburst(df, values='Number of Medals', path=['Country', 'Sport'], title= "Medals and sports for all countries")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Sport==@sports").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            fig = px.sunburst(df, values='Number of Medals', path=['Country', 'Sport'], title= "Medals and sports for all countries")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Year==@years").sort_values(by="Number of Medals", ascending=False, ignore_index=True).head(80)
            df = df.query("Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Country', 'Sport'], title= "Medals and sports for all countries")
    return fig


# Figure two; Sunburst graph sorted by number of medals per sport/year for SWEDEN
@callback(
    Output("graph_sweden_sunburst", "figure"),
    Input("year_dropdown", "value"),
    Input("sport_dropdown", "value"),
    Input("sport_or_medal_dropdown", "value"),
)
def figure_two(years, sports, sort):
    title_fig = "Medals and sports for team SWEDEN"
    if sort == "Sports" or sort in [None, "", []]:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.sunburst(grouped_final_athlete_events.query("Country == 'Sweden'"), values='Number of Medals', 
                color_discrete_sequence=px.colors.qualitative.Pastel1, path=['Sport', 'Medal'], title = title_fig)
        elif years not in [None, "", []] and sports in [None, "", []]:
            # Query for country Sweden and year 2016
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Year==@years")
            fig = px.sunburst(df, values='Number of Medals', path=['Sport', 'Medal'],
                color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Sport', 'Medal'],
                color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Year==@years")
            df = df.query("Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Medal', 'Sport'],
            color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
            return fig
    elif sort =="Medals":   
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.sunburst(grouped_final_athlete_events.query("Country == 'Sweden'"), values='Number of Medals', color_discrete_sequence=px.colors.qualitative.Pastel1, path=['Sport', 'Medal'], title = title_fig)
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Year==@years")
            fig = px.sunburst(df, values='Number of Medals', path=['Medal', 'Sport'],color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Medal', 'Sport'],color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.query("Country == 'Sweden' and Year==@years")
            df = df.query("Sport==@sports")
            fig = px.sunburst(df, values='Number of Medals', path=['Medal', 'Sport'],color_discrete_sequence=px.colors.qualitative.Pastel1, title = title_fig)
            return fig
    




# Figure three: Bar graph showing top 10 sports with the most medals in Sweden
@callback(
    Output("graph_sweden_top10", "figure"),
    [
        Input('year_dropdown', 'value'),
        Input('sport_dropdown', 'value'),
        Input('season_dropdown', 'value'),
    ]
)
def figure_three(year, sport, season):
    # Filter the data based on the selected values
    filtered_data = grouped_final_athlete_events.query("Country == 'Sweden'")

    if year:
        filtered_data = filtered_data[filtered_data['Year'].isin(year)]
    if sport:
        filtered_data = filtered_data[filtered_data['Sport'].isin(sport)]
    if season:
        filtered_data = filtered_data[filtered_data['Season'].isin(season)]

    # Grouping by sport and counting medals
    medals_per_sport = filtered_data[filtered_data['Number of Medals'] > 0].groupby("Sport", as_index=False)["Number of Medals"].count()
    
    # Sort values on number of medals in descending order, resetting index and displaying the result in a plot.
    fig = px.bar(
        data_frame=medals_per_sport.sort_values(by='Number of Medals', ascending=False, ignore_index=True).head(10),
        x='Sport',
        y='Number of Medals',
        labels={'Number of Medals': 'Number of Medals'},
        template='plotly_white',
        title="Top 10 Sports with the Most Medals",
        barmode='overlay',
    )
    fig.update_xaxes(tickangle=45)

    return fig


#Figure four: Bar graph showing top 10 sports with the most gold medals in Sweden
@callback(
    Output("graph_sweden_gold", "figure"),
    [
        Input('year_dropdown', 'value'),
        Input('sport_dropdown', 'value'),
        Input('season_dropdown', 'value'),

    ]
)
def figure_four(year, sport, season):
    # Filter the data based on the selected values
    filtered_data = grouped_final_athlete_events.query("Country == 'Sweden'")
    if year:
        filtered_data = filtered_data[filtered_data['Year'].isin(year)]
    if sport:
        filtered_data = filtered_data[filtered_data['Sport'].isin(sport)]
    if season:
        filtered_data = filtered_data[filtered_data['Season'].isin(season)]

    # Grouping by sport and counting medals
    medals_per_sport = filtered_data[filtered_data['Number of Medals'] > 0].groupby(["Sport", "Medal"], as_index=False)["Number of Medals"].count()
    
    # Filter to include only Gold medals
    medals_per_sport = medals_per_sport[medals_per_sport['Medal'].isin(['Gold'])]

    # Sort values on the number of medals in descending order, resetting index and displaying the result in a plot.
    fig = px.bar(
        data_frame=medals_per_sport.sort_values(by='Number of Medals', ascending=False, ignore_index=True).head(10),
        x='Sport',
        y='Number of Medals',
        labels={'Number of Medals': 'Number of Medals'},
        title="Top 10 Sports Gold Medals",
        barmode='group',
    )
    fig.update_xaxes(tickangle=45)

    return fig   



# Figure five: Mapbox graph showing participants and medals per country/year and season by choice
@callback(
Output("graph_mapbox_2", "figure"),
Input("year_dropdown", "value"),
Input("sport_dropdown", "value"),
Input("season_dropdown", "value")
)
def figure_five(years, sports, sort):
    if sort in [None, "", []]:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.scatter_mapbox(
                grouped_final_athlete_events.drop(columns=["Year","Sport","Season", "Medal"]).groupby(
                    ["Country", "Country_latitude", "Country_longitude"], as_index= False).agg(
                    {"Participants": "sum", "Number of Medals": "sum"}
                    ), 
                    lat="Country_latitude", lon="Country_longitude", size="Participants", color="Number of Medals", 
                    hover_name="Country",  mapbox_style="open-street-map", 
                    center=dict(lat=0, lon=0), zoom=1.2, opacity=0.5,
                    title="Size according to count of participants")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Sport","Season","Medal"]).query("Year==@years")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1,
            title="Size according to count of participants")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Year","Season","Medal"]).query("Sport==@sports")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns= ["Season","Medal"]).query("Year==@years")
            df = df.query("Sport==@sports")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants")
    elif sort =="Summer":
        if (years in [None, "", []]) and (sports in [None, "", []]):
            df = grouped_final_athlete_events.drop(columns=["Year","Sport","Medal"])
            df = df.query('Season == "Summer"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
             hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1.2, opacity=0.5,
            title="Size according to count of participants and Season")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Sport","Medal"]).query("Year==@years")
            df = df.query('Season == "Summer"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1,
            title="Size according to count of participants and Season")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Year","Medal"]).query("Sport==@sports")
            df  = df.query('Season == "Summer"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants and Season")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Medal"]).query("Year==@years")
            df = df.query("Sport==@sports")
            df  = df.query('Season == "Summer"')    
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants and Season")
    else:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            df = grouped_final_athlete_events.drop(columns=["Year","Sport","Medal"])
            df = df.query('Season == "Winter"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
             hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1.2, opacity=0.5,
            title="Size according to count of participants and Season")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Sport","Medal"]).query("Year==@years")
            df = df.query('Season == "Winter"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1,
            title="Size according to count of participants and Season")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Year","Medal"]).query("Sport==@sports")
            df  = df.query('Season == "Winter"')
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants and Season")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Medal"]).query("Year==@years")
            df = df.query("Sport==@sports")
            df  = df.query('Season == "Winter"')    
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants and Season")
        
    fig.update_mapboxes(bounds_east=180, bounds_west=-180, bounds_north=90, bounds_south=-90)
    fig.update_layout(                       
    mapbox_style="white-bg",
    mapbox_layers=[
    {
    "below": 'traces',
    "sourcetype": "raster",
    "sourceattribution": "United States Geological Survey",
    "source": [
    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    ]
    }
    ])
    return fig


# Figure six: Mapbox graph with participants and medals per country/year/sport, and dropdown alternative to see gender ratios per country/year/sport
@callback(
    Output("graph_gender_or_medals_mapbox", "figure"),
    Input("year_dropdown", "value"),
    Input("sport_dropdown", "value"),
    Input("country_dropdown_left", "value")
)
def figure_six(years, sports, sort):
    if sort == "Medals" or sort in [None, "", []]:
        if (years in [None, "", []]) and (sports in [None, "", []]):
            fig = px.scatter_mapbox(grouped_final_athlete_events.drop(columns=["Year","Sport","Season","Medal"]).groupby(
                    ["Country", "Country_latitude", "Country_longitude"], as_index= False).agg(
                    {"Participants": "sum", "Number of Medals": "sum"}
                    ), 
                    lat="Country_latitude", lon="Country_longitude", size="Participants", color="Number of Medals", 
                    hover_name="Country",  mapbox_style="open-street-map", 
                    center=dict(lat=0, lon=0), zoom=1.2, opacity=0.5,
                    title="Size according to count of participants")
        elif years not in [None, "", []] and sports in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Sport","Season","Medal"]).query("Year==@years")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map", 
            center=dict(lat=0, lon=0), zoom=1,
            title="Size according to count of participants")
        elif years in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns=["Year","Season","Medal"]).query("Sport==@sports")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants")
        elif years not in [None, "", []] and sports not in [None, "", []]:
            df = grouped_final_athlete_events.drop(columns= ["Season","Medal"]).query("Year==@years")
            df = df.query("Sport==@sports")
            fig = px.scatter_mapbox(df, lat="Country_latitude", 
            lon="Country_longitude", size="Participants", color="Number of Medals", 
            hover_name="Country",  mapbox_style="open-street-map",
            center=dict(lat=0, lon=0), zoom=1, 
            title="Size according to count of participants")
    elif sort =="Gender ratio":
        df = gender_ratios
        fig = px.scatter_mapbox(df, animation_frame = "Year", lat="Country_latitude",
                lon="Country_longitude", size="Count", color="Ratio", 
                hover_name="Country",  mapbox_style="open-street-map", 
                center=dict(lat=0, lon=0), zoom=1, title="Gender ratios over the years")

    fig.update_mapboxes(bounds_east=180, bounds_west=-180, bounds_north=90, bounds_south=-90)
    return fig


if __name__ == "__main__":
    app.run(debug=True, jupyter_mode = 'external')
    