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
#Read the data file processed by dataProcessing.py
gdf = pd.read_excel('./data/fileToLoad/allData.xlsx')
# App layout
fig = px.choropleth_mapbox(mapbox_style="open-street-map",center = {"lat": 49.611621, "lon": 6.1319346})
#
app = dash.Dash(__name__)
server = app.server
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
                value = "greaterRegion" 
            ),
            dcc.Dropdown(
                id='Polluant',
                options=[
                     {"label": "NO2", "value": 'no2'},
                     {"label": "SO2", "value": 'so2'},
                     {"label": "O3", "value": 'o3'},
                     {"label": "CO", "value": 'co'}],
                value = "no2"
            ),
            dcc.Dropdown(
                id='Nuts',
                options=[
                     {"label": "Nation", "value": 'nuts1'},
                     {"label": "Region", "value": 'nuts2'},
                     {"label": "Departement", "value": 'nuts3'}],
                value='nuts3',
            ),
            dcc.Dropdown(
                id='Year',
                options=[
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                value=2019,
            ),
            dcc.Dropdown(
                id='stats',
                options=[
                     {"label": "mean value", "value": 'mean'},
                     {"label": "minimum value", "value": 'min'},
                     {"label": "maximum value", "value": 'max'},
                     {"label": "standard deviation value", "value": 'std'}],
                value='mean',       
             style={'width': '30%', 'display': 'inline-block'}),

    #    html.Div([
    #        html.H4("Health :", style={'text-align': 'center'}),
    #        dcc.RadioItems(
    #            id='crossfilter-yaxis-type',
    #            options=[{'label': i, 'value': i} for i in ['COVID-19 deaths', 'COVID-19 cases', 'COVID-19 hotspots']],
    #            value='COVID-19 deaths',
    #            labelStyle={'display': 'inline-block'}
    #        )], style={'width': '22%', 'float': 'right', 'display': 'inline-block'}),
       
    #    html.Div([
    #        html.H4("Environment :", style={'text-align': 'center'}),
    #        dcc.RadioItems(
    #            id='Environment',
    #            options=[{'label': i, 'value': i} for i in ['Air pollution', 'wheather', 'land use']],
    #            value='Air pollution',
    #            labelStyle={'display': 'inline-block'})
    #        ], style={'width': '22%', 'float': 'right', 'display': 'inline-block'}),
        
    #    html.Div([
    #        html.H4("Population :", style={'text-align': 'center'}),
    #        dcc.RadioItems(
    #            id='Population',
    #            options=[{'label': i, 'value': i} for i in ['Demography', 'Socio economic', 'Density']],
    #            value='Demography',
    #            labelStyle={'display': 'inline-block'})
    #        ], style={'width': '22%', 'float': 'right', 'display': 'inline-block'})
        
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
        
        html.Div([
        dcc.Graph(id='pollution_map', style={"height": 600, "width" : '100%', 'margin':'0 auto', 'background-color': 'rgba(0,0,0,0)'},
        figure=fig,
        hoverData={'points':[{'location': 'Breux'}]})
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
            12: 'December'}), style={'width': '90%', 'margin': '0 auto', 'padding': '0px 20px 20px 20px', 'background-color': 'rgba(0,0,0,0)'}),

        html.Div([
            dcc.Graph(id='poll-time-series'),
            ], style={'display': 'inline-block', 'width': '49%', 'margin': '0 auto'}),

        html.Div([
            dcc.Graph(id='COVID-time-series'),
            ], style={'display': 'inline-block', 'width': '49%', 'margin': '0 auto'}),])])

    
def create_time_series(dff, title, poll, stat):
    fig = px.scatter(dff, x='date', y='{}'.format(stat), height= 400)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, plot_bgcolor='rgba(0,0,0,0)')
    return [fig]

def create_COVID_time_series(dff, title):
    fig = px.scatter(dff, x='date', y='COVID Cases', height= 400)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10}, plot_bgcolor='rgba(0,0,0,0)')
    return [fig]


@app.callback(
    [Output('poll-time-series', 'figure')],
    [Input('pollution_map', 'hoverData'),
     Input('Polluant', 'value'),
     Input('stats','value')])
def update_poll_timeseries(hoverData, poll, stat):
    country_name = hoverData['points'][0]['location']
    dff = gdf[gdf['id'] == country_name]
    dff = dff[dff['polluant'] == poll]
    title = '<b>{} {} pollution data</b>'.format(country_name, poll)
    return create_time_series(dff, title, poll, stat)

@app.callback(
    [Output('COVID-time-series', 'figure')],
    [Input('pollution_map', 'hoverData')])
def update_covid_timeseries(hoverData):
    country_name = hoverData['points'][0]['location']
    dff = gdf[gdf['id'] == country_name]
    title = '<b>{} COVID Cases data</b>'.format(country_name)
    return create_COVID_time_series(dff, title)


if __name__ == '__main__':
    server.run(debug=True)
    #app.run_server(debug=True)
    #server.run(host = "0.0.0.0", port= 5000)