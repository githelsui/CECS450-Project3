# import csv
#
# with open('NBA_Team_Stats.csv') as csvfile:
#     csvreader = csv.reader(csvfile, delimiter = ',')
# #     for row in csvreader:
# #         print(', '.join(row))
#
# import pandas as pd
# import csv
# import numpy as np
#
# key = input("Enter key you'd like to search for: ")
# data = list(csv.reader(open("NBA_Team_Stats.csv")))
#
# for i in range(len(data)):
#   for j in range(len(data[i])):
#       if data[i][j] == key:
#         print(data[i])

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import csv

#n
#runs on http://127.0.0.1:8050/

app = Dash(__name__)
#Grab data from CSV file.
with open('Sports Reference NBA Data (2021 - 2022) Season.xlsx - sportsref_download.xls.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

# This is hacky, but i dont know why the radial chart breaks if I do it the easier, more direct way.
dataValues1 = [float(rows[1][24]), float(rows[1][19]), float(rows[1][20]), float(rows[1][21])]
dataValues2 = [float(rows[2][24]), float(rows[2][19]), float(rows[2][20]), float(rows[2][21])]
descriptionNames = ['Points Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game']
# print(dataValues)

# Selected columns are Points (Column Y), Assists (Column T), Steals (Column U), Blocks (Column V)
# Defaulting to first row until we decide how to change what team is being viewed
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
                     range_r = [0, 150])

rad2 = px.line_polar(df2, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 150])
#rad1.show()

df2 = px.data.stocks()
hist = px.histogram(df2, x = "date", nbins = 23) #23 weeks in nba season


app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting'),
        dcc.Dropdown(['OPT 1'], 'OPT 1', id='Test-Dropdown'),
        html.Div(id='td-output'),
        html.Div(children = 'All Teams Wins/Losses'),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = hist
        ),
        html.Div(children = 'Radial Chart of Normalized Data'),
        dcc.Graph(
            id = 'Radial Visualization',
            figure = rad1
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