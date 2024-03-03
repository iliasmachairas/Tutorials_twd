# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import sys
import plotly.graph_objects as go

print(sys.executable)

# Read the airline spacex_df into pandas dataframe
FRA = pd.read_csv('FRA_df.csv', encoding='utf-8')
FRA['Date'] = pd.to_datetime(FRA['Date'])
FRA['year'] = (FRA.Date.dt.year).astype(int)


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H4("Fatal Road Accidents (FRA) in Athens (2011-2015)", style={'color': 'black'}),

    html.Div([
        html.Div([
            "Select vehicle: ",
            dcc.RadioItems(id='vehicle-radio',
                           options=[
                               {'label': 'car', 'value': 'car'},
                               {'label': 'motorcycle', 'value': 'motorcycle'},
                               {'label': 'Other', 'value': 'Other'},
                               {'label': 'All', 'value': 'All'}
                           ],
                           value='All',
                           labelStyle={'display': 'block'}
                           )
        ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            "Select year: ",
            dcc.Dropdown(id='year-dropdown',
                         options=[
                             {'label': '2011', 'value': 2011},
                             {'label': '2012', 'value': 2012},
                             {'label': '2013', 'value': 2013},
                             {'label': '2014', 'value': 2014},
                             {'label': 'All', 'value': 'All'}
                         ],
                         value='All',
                         )
        ], style={'width': '20%', 'display': 'inline-block'})
    ], style={'color': 'black'}),

    html.Div([
        html.Div(dcc.Graph(id='Bar-charts-Age_group'), style={'width': '30%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='pie-chart-Time'), style={'width': '30%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='Map-FRA'), style={'width': '30%', 'display': 'inline-block'})
    ])
])

@app.callback(
    Output(component_id='Bar-charts-Age_group', component_property='figure'),
    [Input(component_id='vehicle-radio', component_property='value'),
    Input(component_id="year-dropdown", component_property="value")])

def update_output_barplot(value_vehicle, value_year):
    df_clip_1 = FRA.copy() if value_year=='All' else FRA[FRA.year == value_year].copy()
    df_clip_2 = df_clip_1.copy() if value_vehicle=='All' else df_clip_1[df_clip_1.Vehicle == value_vehicle].copy()
    time_series_Age = df_clip_2.Age.value_counts()
    time_series_Age = time_series_Age.to_frame()
    fig = px.bar(time_series_Age, x='Age', y=time_series_Age.index, title="Age groups",orientation='h')
    fig.update_layout(
        title="Age Groups",
        xaxis_title="Count",
        yaxis_title="Age Group")
    return fig

@app.callback(
    Output(component_id='pie-chart-Time', component_property='figure'),
    [Input(component_id='vehicle-radio', component_property='value'),
    Input(component_id="year-dropdown", component_property="value")])

def update_output_pieplot(value_vehicle, value_year):
    df_clip_1 = FRA.copy() if value_year=='All' else FRA[FRA.year == value_year].copy()
    df_clip_2 = df_clip_1.copy() if value_vehicle=='All' else df_clip_1[df_clip_1.Vehicle == value_vehicle].copy()
    time_series = df_clip_2.Time.value_counts()
    time_series = time_series.to_frame()
    #print(time_series.head())
    fig2 = go.Figure(data=[go.Pie(labels=time_series.index, values=time_series.Time, hole=.3)])
    fig2.update_layout(title_text='Time')
    return fig2

@app.callback(
    Output(component_id='Map-FRA', component_property='figure'),
    [Input(component_id='vehicle-radio', component_property='value'),
    Input(component_id="year-dropdown", component_property="value")])

# Add the map
def update_output_map(value_vehicle, value_year):
    df_clip_1 = FRA.copy() if value_year=='All' else FRA[FRA.year == value_year].copy()
    df_clip_2 = df_clip_1.copy() if value_vehicle=='All' else df_clip_1[df_clip_1.Vehicle == value_vehicle].copy()
    fig = px.scatter_mapbox(df_clip_2, lon='x', lat='y',
                        color_discrete_sequence=["fuchsia"], hover_data=["Date", "Time"], zoom=9, height=500)
    fig.update_layout(title="Map", mapbox_style="open-street-map")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)