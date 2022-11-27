from dash import Dash, html, dcc, Input, Output
import plotly.express as px 
import pandas as pd 
from ReadCSV import teamWinsDataFrame

#n
#runs on http://127.0.0.1:8050/

app = Dash(__name__)

# Data for Histogram of Wins per Team
teamWins = teamWinsDataFrame()
print(teamWins)
# print(teamWins_df)
# hist = px.histogram(clean_data, labels=dict(x='Teams', y='Wins')) 
hist = px.histogram(x=teamWins[0], y=teamWins[1], labels=dict(x='Teams', y='Wins')) 
# hist = px.bar(teamWins_df)

df = pd.DataFrame(dict(
        r = [3,3, 3, 4, 5], 
        theta = ['DataPoint1', 'DataPoint2', 'DataPoint3', 'DataPoint4', 'DataPoint5']
        ))
rad = px.line_polar(df, r= 'r', theta = 'theta', line_close = True)

app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting'),
        dcc.Dropdown(['OPT 1', 'OPT 2'], 'OPT 1', id='Test-Dropdown'),
        html.Div(id='td-output'),
        html.Div(children = 'All Teams Wins'),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = hist
        ),
        html.Div(children = 'Radial Chart of Normalized Data'), 
        dcc.Graph(
            id ='Radial Visualization', 
            figure= rad
        )
])

@app.callback(
    Output('td-output', 'children'),
    Input('Test-Dropdown', 'value')
)
def update_output(value):
    return f'Displaying {value}'

if __name__ == '__main__': 
    app.run_server(debug=True)
