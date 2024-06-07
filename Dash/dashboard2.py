# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1(
            "Flight Delay Time Statistics",
            style={
                'font-size': 45,
                'color': '#070217',
                'text-align': 'center',
                'margin-bottom': '25px'
            }
        ),
        html.Div(
            [
                "Input Year",
                dcc.Input(
                    id = "year",
                    type = "number",
                    value = "2010",
                    style = {
                        'font-size': 25,
                        'height': 35,
                        'margin-left':'10px',
                        'margin-bottom':'20px'
                    }
                )
            ],
            style = {
                'text-align': 'center'
            }
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id = "carrier_fig"
                    ),
                    style = {
                        'width': '50%'
                    }
                ),
                html.Div(
                    dcc.Graph(
                        id = "weather_fig"
                    ),
                    style = {
                        'width': '50%'
                    }
                )
            ],
            style = {
                'display': 'flex',
                'justify-content': 'space-around',
                'margin-bottom': '20px'
            }
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(
                        id = "nas_fig"
                    ),
                    style = {
                        'width': '50%'
                    }
                ),
                html.Div(
                    dcc.Graph(
                        id = "sec_fig"
                    ),
                    style = {
                        'width': '50%'
                    }
                )
            ],
            style = {
                'display': 'flex',
                'justify-content': 'space-around',
                'margin-bottom': '20px'
            }
        ),
        html.Div(
            [
                dcc.Graph(
                    id = "late_fig"
                )
            ],
            style = {
                'width': '80%',
                'align': 'center',
                'margin': '0 auto'
            }
        )
    ],
    style={
        'font-family': 'Arial, sans-serif',
        'background-color': '#f9f9f9',
        'padding': '20px'
    }
)

@app.callback(
    [
        Output(
        component_id = "carrier_fig",
        component_property = "figure"),

        Output(
        component_id = "weather_fig",
        component_property = "figure"),

        Output(
        component_id = "nas_fig",
        component_property = "figure"),

        Output(
        component_id = "sec_fig",
        component_property = "figure"),

        Output(
        component_id = "late_fig",
        component_property = "figure"),
    ],
    Input(
        component_id = "year",
        component_property = "value"
        )
    )

def update_graph1(year):

    carrier, weather, NAS, security, late = compute_info(airline_data, year)

    carrier_fig = px.line(
        carrier,
        x = "Month",
        y = 'CarrierDelay',
        color = "Reporting_Airline",
        title = "Average carrier Delay time (mins) by Airline"
    )

    weather_fig = px.line(
        weather,
        x = "Month",
        y = "WeatherDelay",
        color = "Reporting_Airline",
        title = "Average Weather Delay time (mins) by Airline"
    )

    NAS_fig = px.line(
        NAS,
        x = "Month",
        y = "NASDelay",
        color = "Reporting_Airline",
        title = "Average NAS Delay time (mins) by Airline"
    )

    security_fig = px.line(
        security,
        x = "Month",
        y = "SecurityDelay",
        color = "Reporting_Airline",
        title = "Average Security Delay time (mins) by Airline"
    )

    late_fig = px.line(
        late,
        x = "Month",
        y = "LateAircraftDelay",
        color = "Reporting_Airline",
        title = "Average Late Aircraft Delay time (mins) by Airline"
    )

    return [carrier_fig, weather_fig, NAS_fig, security_fig, late_fig] 


def compute_info(airline_data, year):

    df = airline_data[airline_data['Year'] == int(year)]

    carrier = df.groupby(["Month", "Reporting_Airline"])['CarrierDelay'].mean().reset_index()
    weather = df.groupby(["Month", "Reporting_Airline"])['WeatherDelay'].mean().reset_index()
    NAS = df.groupby(["Month", "Reporting_Airline"])['NASDelay'].mean().reset_index()
    security = df.groupby(["Month", "Reporting_Airline"])['SecurityDelay'].mean().reset_index()
    late = df.groupby(["Month", "Reporting_Airline"])['LateAircraftDelay'].mean().reset_index()
    
    return carrier, weather, NAS, security, late


# Run the application

if __name__ == '__main__':
    app.run_server()