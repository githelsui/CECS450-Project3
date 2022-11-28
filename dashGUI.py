from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import csv

import ReadCSV as readcsv

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
rad1 = px.line_polar(df1, r='value',
                     theta='description',
                     line_close=True,
                     range_r=[0, 100])

rad2 = px.line_polar(df2, r='value',
                     theta='description',
                     line_close=True,
                     range_r=[0, 100])
#rad1.show()

df2 = px.data.stocks()
teamWins = readcsv.teamWinsDataFrame()
#print(teamWins)
hist = px.histogram(x=teamWins[0], y=teamWins[1], labels=dict(x='Teams', y='Wins'))
#hist = px.histogram(df2, x = "date", nbins = 23) #23 weeks in nba season

# Lists w/ Normalized Data for Radial Chart Ranges
normalizationDataPoints = readcsv.normalizeStatsPoints()
print(normalizationDataPoints)

normalizationDataAssists = readcsv.normalizeStatsAssits()
print(normalizationDataAssists)

normalizationDataBlocks = readcsv.normalizeStatsBlocks()
print(normalizationDataBlocks)

normalizationDataSteals = readcsv.normalizeStatsSteals()
print(normalizationDataSteals)


app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting'),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = hist
        ),
        dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder',
                      'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'OPT 1', id='Test-Dropdown1'),
        html.Div(id='td-output'),
        dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder',
                      'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'OPT 1', id='Test-Dropdown2'),
        html.Div(children = 'All Teams Wins/Losses'),
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





