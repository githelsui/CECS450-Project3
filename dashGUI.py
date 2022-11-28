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
with open('Sports_Reference_NBA_Data_2021_-_2022_Season.xlsx_-_sportsref_download.xls.csv') as csv_file:
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
        html.Div(id='td-output'),
        html.Div(children = 'All Teams Wins/Losses'),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = hist
        ),
        html.Div(children = ['Implied Probability\n\n', dcc.Input(
            id='ImpliedProb1',
            type = 'number',
            value = 100
            ), 
            html.Table([
                html.Tr([html.Td('Team #1 Win %: '), html.Td(id='imp1')]),
            ]),
            dcc.Input(
            id='ImpliedProb2',
            type = 'number',
            value = 100
            ),
            html.Table([
                html.Tr([html.Td('Team #2 Win %: '), html.Td(id='imp2')]),
            ]),
        ]),
        html.Div(children = [html.Div(children = 'TEAM 1 VS TEAM 2'),
            dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder','Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'Atlanta Hawks', id='drop1', style=dict(width='50%')), 
            dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder','Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'Atlanta Hawks', id='drop2', style=dict(width='50%')) 

        ]),
        html.Div(children = [html.Div(children = "Radial Chart of Normalized Data"), 
            dcc.Graph(id = 'rad1', figure = rad1, style={'display': 'inline-block'}), 
                      
            dcc.Graph(id = 'rad2', figure = rad2, style={'display': 'inline-block'})
        ])
    ])


#this callback allows users to choose the teams they want to see in the radial chart
#the Input elements are parameters to the function immediately below
#the Output elements are [rad1, rad2] list that the function returns
#automatically get connected to eachother
@app.callback(
    Output('rad1', 'figure'),
    Output('rad2', 'figure'),
    Input('drop1', 'value'),
    Input('drop2', 'value')
)
def update_graph(drop1, drop2):
    allTeams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder','Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
    rowNumber1 = allTeams.index(drop1) + 1
    rowNumber2 = allTeams.index(drop2) + 1

    #gets the data values from the rows list created when the csv file was imported
    dataValues1 = [float(rows[rowNumber1][24]), float(rows[rowNumber1][19]), float(rows[rowNumber1][20]), float(rows[rowNumber1][21])]
    dataValues2 = [float(rows[rowNumber2][24]), float(rows[rowNumber2][19]), float(rows[rowNumber2][20]), float(rows[rowNumber2][21])]

    #normalization would go here
    descriptionNames = ['Points Per Game', 'Assists Per Game', 'Steals Per Game', 'Blocks Per Game']

    df1 = pd.DataFrame.from_dict(dict(
        value = dataValues1,
        description = descriptionNames
        ))

    df2 = pd.DataFrame.from_dict(dict(
        value = dataValues2,
        description = descriptionNames
        ))


    rad1 = px.line_polar(df1, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 150])

    rad2 = px.line_polar(df2, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 150])

    return [rad1, rad2]

#implied probability callback
#allows users to enter a value and get the odds of them winning (as percentages) 
@app.callback(
    Output('imp1', 'children'),
    Output('imp2', 'children'),
    Input('ImpliedProb1', 'value'),
    Input('ImpliedProb2', 'value')
)

def updateAmericanOdds(imp1, imp2):
    percentage = 0
    listStr = []
    if imp1 != None:
        if (imp1 >= 0):
            percentage = (100 / (imp1 + 100)) * 100
        else: 
            percentage = ((-1*(imp1)) / (-1*(imp1) + 100)) * 100
        asStr = str(percentage)+ " %"
        listStr.append(asStr)
    if imp2 != None:
        if (imp2 >= 0):
            percentage = (100 / (imp2 + 100)) * 100
        else:
            percentage = ((-1 * (imp2)) / (-1 * (imp2) + 100)) * 100
        asStr = str(percentage) + " %"
        listStr.append(asStr)
        return listStr
    return ["", ""]


if __name__ == '__main__':
    app.run_server(debug=True)