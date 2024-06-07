import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read in the data
airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
    encoding="ISO-8859-1",
    dtype={'Div1Airport': str, 'Div1TailNum': str, 'Div2Airport': str, 'Div2TailNum': str}
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1(
            'Airline Performance Dashboard',
            style={
                'font-size': 40,
                'textAlign': 'center',
                'color': '#431a3f',
            }
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id='input-year',
                    value='2010',
                    type='number',
                    style={
                        'height': '35px',
                        'font-size': 25
                    }
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id='line-plot')
            ]
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id='year',
                    value='2010',
                    type="number",
                    style={
                        'height': '35px',
                        'font-size': 25
                    }
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id='bar-plot')
            ]
        ),
    ]
)

# Define the callback for the line plot
@app.callback(
    Output('line-plot', 'figure'),
    Input('input-year', 'value')
)
def update_line_plot(year):
    df = airline_data[airline_data['Year'] == int(year)]
    line_data = df.groupby("Month")['ArrDelay'].mean().reset_index()
    fig = go.Figure(
        data=go.Scatter(
            x=line_data['Month'],
            y=line_data['ArrDelay'],
            mode='lines',
            marker=dict(color="#e232a1")
        )
    )
    fig.update_layout(
        title='Month vs Average Flight Delay Time',
        xaxis_title='Month',
        yaxis_title='Average Arrival Delay (minutes)'
    )
    return fig

# Define the callback for the bar plot
@app.callback(
    Output('bar-plot', 'figure'),
    Input('year', 'value')
)
def update_bar_plot(year):

    data = airline_data[airline_data['Year'] == int(year)]
    
    bar_data = data[['DestState', 'Flights']].groupby("DestState").sum().reset_index()
    
    fig = px.bar(
    bar_data,
    x = 'DestState',
    y = 'Flights',
    title = f"Total number of flights to the destination state split by reporting air($year)"
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
