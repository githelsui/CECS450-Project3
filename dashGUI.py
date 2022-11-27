from dash import Dash, html, dcc, Input, Output
import plotly.express as px 
import pandas as pd
import csv

#n
#runs on http://127.0.0.1:8050/

app = Dash(__name__)
#Grab data from CSV file.
with open('Odds - Sheet1.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

#This is hacky, but i dont know why the radial chart breaks if I do it the easier, more direct way.
dataValues1 = [float(rows[1][5]), float(rows[1][6]), float(rows[1][7]), float(rows[1][9])]
dataValues2 = [float(rows[2][5]), float(rows[2][6]), float(rows[2][7]), float(rows[2][9])]
descriptionNames = ['Percent 2-Point Field Goals Attempted', 'Percent 3-Point Field Goals Attempted',
                              'Percent 2-Point Field Goals Scored', 'Percent 3-Point Field Goals Scored']
#print(dataValues)

#Selected columns are F, G, H, and J
#Defaulting to first row until we decide how to change what team is being viewed
df1 = pd.DataFrame.from_dict(dict(
        value = dataValues1,
        description = descriptionNames
        ))
df2 = pd.DataFrame.from_dict(dict(
        value = dataValues2,
        description = descriptionNames
        ))
#print(df1)
rad1 = px.line_polar(df1, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 100])

rad2 = px.line_polar(df2, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 100])
#rad1.show()

df2 = px.data.stocks()
hist = px.histogram(df2, x = "date", nbins = 23) #23 weeks in nba season


app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting'),
        dcc.Dropdown(['OPT 1', 'OPT 2'], 'OPT 1', id='Test-Dropdown'),
        html.Div(id='td-output'),
        html.Div(children = 'All Teams Wins/Losses'),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = hist
        ),
        html.Div(children = 'Radial Chart of Normalized Data'),
        dcc.Graph(
            id ='Radial Visualization',
            figure= rad1
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
