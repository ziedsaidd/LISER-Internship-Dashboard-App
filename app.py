#importing the requiered modules
import os 
import geopandas as gpd
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
import rasterstats
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
import dash  
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import time


# App layout
app = dash.Dash(__name__)
app.layout = html.Div(
        [
        # header
        html.Div([

            html.Span("Air pollution web app - COVID 19 Project", className='app-title'),
            
            html.Div(
                html.Img(src='https://wwwfr.uni.lu/var/storage/images/universite/actualites/a_la_une/collaboration_scellee_avec_liser/1014145-1-fre-FR/collaboration_scellee_avec_liser_medium.jpg',height="100%")
                ,style={"float":"right","height":"100%"})
            ],
            className="row header"
            ),
        
        
        html.Div([

        html.Div([
            dcc.Dropdown(
                id='Country',
                options=[
                     {"label": "Greater Region", "value": 'greaterRegion'},
                     {"label": "Luxembourg", "value": 'luxembourg'},
                     {"label": "France", "value": 'france'},
                     {"label": "Europe", "value": 'europe'},
                     {"label": "USA", "value": 'usa'}],
                #value='Greater Region',
                #placeholder="Select a country or a region"
                value = "greaterRegion" 
            ),
            dcc.Dropdown(
                id='Polluant',
                options=[
                     {"label": "NO2", "value": 'no2'},
                     {"label": "SO2", "value": 'so2'},
                     {"label": "O3", "value": 'o3'},
                     {"label": "CO", "value": 'co'}],
                #value='NO2',
                #placeholder="Select a polluant"
                value = "no2"
            ),
            dcc.Dropdown(
                id='Nuts',
                options=[
                     {"label": "Nation", "value": 'nuts1'},
                     {"label": "Region", "value": 'nuts2'},
                     {"label": "Departement", "value": 'nuts3'}],
                value='nuts3',
                #placeholder="Select the Nuts level"
            ),
            dcc.Dropdown(
                id='Year',
                options=[
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                value=2019,
                #placeholder="Select the year"
            ),
            dcc.Dropdown(
                id='stats',
                options=[
                     {"label": "mean value", "value": 'mean'},
                     {"label": "minimum value", "value": 'min'},
                     {"label": "maximum value", "value": 'max'},
                     {"label": "standard deviation value", "value": 'std'}],
                value='mean',
                #placeholder="Select the stats")],
        
             style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.H4("Health :", style={'text-align': 'center'}),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['COVID-19 deaths', 'COVID-19 cases', 'COVID-19 hotspots']],
                value='COVID-19 deaths',
                labelStyle={'display': 'inline-block'}
            )], style={'width': '22%', 'float': 'right', 'display': 'inline-block'}),
       
        html.Div([
            html.H4("Environment :", style={'text-align': 'center'}),
            dcc.RadioItems(
                id='Environment',
                options=[{'label': i, 'value': i} for i in ['Air pollution', 'wheather', 'land use']],
                value='Air pollution',
                labelStyle={'display': 'inline-block'})
            ], style={'width': '22%', 'float': 'right', 'display': 'inline-block'}),
        
        html.Div([
            html.H4("Population :", style={'text-align': 'center'}),
            dcc.RadioItems(
                id='Population',
                options=[{'label': i, 'value': i} for i in ['Demography', 'Socio economic', 'Density']],
                value='Demography',
                labelStyle={'display': 'inline-block'})
            ], style={'width': '22%', 'float': 'right', 'display': 'inline-block'})
        
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([
        dcc.Graph(id='pollution_map', style={"height": 700}, figure={})
        ]),
        
        html.Div(dcc.Slider(
            id='month_selector',
            min=1,
            max=12,
            value=1,
            marks={
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'}), style={'width': '100%', 'padding': '0px 20px 20px 20px'}),

        html.Div([
            dcc.Graph(id='x-time-series'),
            ], style={'display': 'inline-block', 'width': '49%'}),

        html.Div([
            dcc.Graph(id='y-time-series'),
            ], style={'display': 'inline-block', 'width': '49%'}),])])


gdf = pd.read_excel('./data/fileToLoad/allData.xlsx')

@app.callback(
[Output(component_id='pollution_map', component_property='figure')],
[Input(component_id='Country', component_property='value'),
Input(component_id='Polluant', component_property='value'),
Input(component_id='Nuts', component_property='value'),
Input(component_id='Year', component_property='value'),
Input(component_id='month_selector', component_property='value'),
Input(component_id='stats', component_property='value')]
)
def update_graph(reg, poll, nut, y, m, s):
    #gdf = pd.read_excel(('./data/processedData/{}_{}_{}_{}_{}.xlsx').format(reg, poll, nut, y, m))
    start1 = time.time()

    with open("./data/geojsonFiles/geojson_{}_{}".format(reg, nut)) as geofile:
        geojson_layer = json.load(geofile)
    for feature in geojson_layer['features']:
        feature['id'] = feature['properties']['GEN']
    df = gdf.copy()
    df = df[df["zone"] == reg]
    df = df[df["year"] == y]
    df = df[df["nuts"] == nut]
    df = df[df["month"] == m]
    df = df[df["polluant"] == poll]
    done1 = time.time()

    fig = px.choropleth_mapbox(df, geojson=geojson_layer, locations='id', color = s,
                           mapbox_style="open-street-map",
                           zoom=6, center = {"lat": 49.611621, "lon": 6.1319346},
                           opacity=0.5,
                           range_color = [0, 0.000150],
                           labels={s:('{} {} value (mol/m²)').format(poll, s)}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    done2 = time.time()
    print (done2-done1, done1-start1)
    return [fig]
    

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)