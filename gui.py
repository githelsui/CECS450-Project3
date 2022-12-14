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
import math
import ReadCSV as readcsv

#n
#runs on http://127.0.0.1:8050/

app = Dash(__name__)
#Grab data from CSV file.
with open('Sports_Reference_NBA_Data_2021_-_2022_Season.xlsx_-_sportsref_download.xls.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)


# Lists w/ Normalized Data for Radial Chart Ranges
normalizationDataPoints = readcsv.normalizeStatsPoints()
print(normalizationDataPoints)

normalizationDataAssists = readcsv.normalizeStatsAssits()
print(normalizationDataAssists)

normalizationDataBlocks = readcsv.normalizeStatsBlocks()
print(normalizationDataBlocks)

normalizationDataSteals = readcsv.normalizeStatsSteals()
print(normalizationDataSteals)

print("Points:" + str(len(normalizationDataPoints)))
print("Assists:" + str(len(normalizationDataAssists)))
print("Blocks:" + str(len(normalizationDataBlocks)))
print("Steals:" + str(len(normalizationDataSteals)))
#dictionary stuff

teamName = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder',
                      'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
print('names:' + str(len(teamName)))
normalizedDict = {"Team Name:":teamName, "Points":normalizationDataPoints,"Assists":normalizationDataAssists,"Steals":normalizationDataSteals,"Blocks":normalizationDataBlocks}
print(normalizedDict)
df3 = pd.DataFrame(normalizedDict)
print(df3)

print("IAT TEST: " + str(df3.iat[0,1]))


# This is hacky, but i dont know why the radial chart breaks if I do it the easier, more direct way.
dataValues1 = [float(df3.iat[0,1]), float(df3.iat[0,2]), float(df3.iat[0,3]), float(df3.iat[0,4])]
dataValues2 = [float(df3.iat[1,1]), float(df3.iat[1,2]), float(df3.iat[1,3]), float(df3.iat[1,4])]
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
                     range_r = [0, 100])

rad2 = px.line_polar(df2, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 100])
#rad1.show()

teamWins = readcsv.teamWinsDataFrame()
teamLosses = readcsv.teamLossesDataFrame()
#print(teamWins)
histWins = px.histogram(x=teamWins[0], y=teamWins[1], title='Number of Games Won per Team', labels=dict(x='Teams', y='Wins'))
histLosses = px.histogram(x=teamLosses[0], y=teamLosses[1], title='Number of Games Lost per Team', labels=dict(x='Teams', y='Losses'))

#hist = px.histogram(df2, x = "date", nbins = 23) #23 weeks in nba season


app.layout = html.Div(
    children=[
        html.H1(children='Sports Betting', style = {'border-bottom':'#000000 solid'}),
        html.Div(id='td-output'),
        html.Div(children = [html.Div(children = 'All Teams Wins / Losses '),
            dcc.Dropdown(['Wins', 'Losses'], 'Wins', id='dropHistogram', style={'display': 'inline block', 'width': '40%'}), 
        ]),
        dcc.Graph(
            id = 'Wins/Loss Histogram',
            figure = histWins
        ),
        html.Div(children = ('Implied Probability\n\n'), style = {'font-size': '20px', 'padding-bottom': '2%', 'border-top':'#000000 solid'}),
        html.Div(children = ['Team #1 Odds: ', 
            dcc.Input(
            id='ImpliedProb1',
            type = 'number',
            value = 100, 
            style = {'display': 'inline-block'}
            ), 
            html.Table([
                html.Tr([html.Td('Win %: '), html.Td(id='imp1')]),
            ], style={'padding-bottom': '1%'}),

            dcc.Store(id = 'im1'), 
            dcc.Store(id = 'im2'),
            html.Div(children = ['Team #2 Odds: ', 
                    dcc.Input(
                    id='ImpliedProb2',
                    type = 'number',
                    value = 100
                ),
                
                html.Table([
                    html.Tr([html.Td('Win %: '), html.Td(id='imp2')]),
                ], style={'padding-bottom': '1%'}), 
                ]),
            
            html.Table([
                html.Tr([html.Td('SportsBook Edge: '), html.Td(id='sportsEdge')],  style={'padding-top': '2%'}),
            ])
        ], style={'padding-bottom': '2%'}),
        html.Div(children = [html.Div(children = "Radial Chart of Normalized Data", style={'font-size': '20px','border-top':'#000000 solid'}), 
        html.Div(children = [html.Div(children = 'TEAM 1', style={'padding-top': '2%'}),
            dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder','Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'Atlanta Hawks', id='drop1', style={'display': 'inline block', 'width': '40%'}), 

        ]),
        html.Div(children = [html.Div(children = 'TEAM 2'),
            dcc.Dropdown(['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder','Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'], 'Atlanta Hawks', id='drop2', style={'display': 'inline block', 'width': '40%'}) 

        ]),

            dcc.Graph(id = 'rad1', figure = rad1, style={'display': 'inline-block', 'padding-left': '5%'}), 
                      
            dcc.Graph(id = 'rad2', figure = rad2, style={'display': 'inline-block', 'padding-right': '5%%'})
        ])
    ])

#this callback is for Histogram option between wins and losses per each team
@app.callback(
    Output('Wins/Loss Histogram', 'figure'),
    Input('dropHistogram', 'value'),
)

def update_histogram(drop):
    if drop != None:
        if drop == 'Wins':
            return histWins
        else:
            return histLosses

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
    rowNumber1 = allTeams.index(drop1)
    rowNumber2 = allTeams.index(drop2)

    #gets the data values from the rows list created when the csv file was imported
    # dataValues1 = [float(rows[rowNumber1][24]), float(rows[rowNumber1][19]), float(rows[rowNumber1][20]), float(rows[rowNumber1][21])]
    # dataValues2 = [float(rows[rowNumber2][24]), float(rows[rowNumber2][19]), float(rows[rowNumber2][20]), float(rows[rowNumber2][21])]

    # Updated to Normalized Values on Radial Chart
    dataValues1 = [float(df3.iat[rowNumber1, 1]), float(df3.iat[rowNumber1, 2]), float(df3.iat[rowNumber1, 3]), float(df3.iat[rowNumber1, 4])]
    dataValues2 = [float(df3.iat[rowNumber2, 1]), float(df3.iat[rowNumber2, 2]), float(df3.iat[rowNumber2, 3]), float(df3.iat[rowNumber2, 4])]

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
                     range_r = [0, 100])

    rad2 = px.line_polar(df2, r= 'value',
                     theta = 'description',
                     line_close = True,
                     range_r = [0, 100])

    return [rad1, rad2]

#implied probability callback
#allows users to enter a value and get the odds of them winning (as percentages) 
@app.callback(
    Output('imp1', 'children'),
    Output('imp2', 'children'),
    Output('im1', 'data'), 
    Output('im2', 'data'),
    Input('ImpliedProb1', 'value'),
    Input('ImpliedProb2', 'value')
)

def updateAmericanOdds(imp1, imp2):
    percentage1 = 0
    percentage2 = 0
    listStr = []
    if imp1 != None and imp2 != None: 
        if (imp1 >= 0):
            percentage1 = (100 / (imp1 + 100)) * 100
        else: 
            percentage1 = ((-1*(imp1)) / (-1*(imp1) + 100)) * 100

        if (imp2 >= 0):
            percentage2 = (100 / (imp2 + 100)) * 100
        else:
            percentage2 = ((-1 * (imp2)) / (-1 * (imp2) + 100)) * 100

        asStr1 = str(percentage1)+ " %"
        asStr2 = str(percentage2)+ " %"
        listStr = [asStr1, asStr2, percentage1, percentage2]
        return listStr
    return ["", "", "", ""]


@app.callback(
    Output('sportsEdge', 'children'),
    Input('im1', 'data'), 
    Input('im2', 'data')
)
def sportsbookEdge(i1, i2): 
    percentage1 = 0
    percentage2 = 0

    if i1== "" or i2 == "" or i1 == None or i2 == None: 
        return [""]
    else: 
        if (i1 >= 0):
            percentage1 = ((100 / (i1 + 100)))
        else: 
            percentage1 = (((-1*(i1)) / (-1*(i1) + 100)))

        if (i2 >= 0):
            percentage2 = ((100 / (i2 + 100)))
        else:
            percentage2 = (((-1 * (i2)) / (-1 * (i2) + 100)))
        sportsEdge = ((percentage1 + percentage2) - 1) * 10
        return [(str(sportsEdge) + " %")]



if __name__ == '__main__':
    app.run_server(debug=True)