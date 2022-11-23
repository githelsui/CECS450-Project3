from dash import Dash, html, dcc
import plotly.express as px 
import pandas as pd 

#n
#runs on http://127.0.0.1:8050/

app = Dash(__name__)




df = pd.DataFrame(dict(
        r = [3,3, 3, 4, 5], 
        theta = ['DataPoint1', 'DataPoint2', 'DataPoint3', 'DataPoint4', 'DataPoint5']
        ))
rad = px.line_polar(df, r= 'r', theta = 'theta', line_close = True)


df = px.data.stocks()
hist = px.histogram(df, x = "date", nbins = 23) #23 weeks in nba season


app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting'),
        html.Div(children = 'All Teams Wins/Losses'),
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

if __name__ == '__main__': 
    app.run_server(debug=True)