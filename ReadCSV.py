import csv


# def teamDataForYears(years):
#     # Key to search for (implemented for testing and making sure filtering will work down the line)
#     key = input("Enter key you'd like to search for: ")
#     # Create a 2D Array by reading csv data
#     data = list(csv.reader(open("Sports Reference NBA Data (2021 - 2022) Season.xlsx - sportsref_download.xls.csv")))
#
#     # Look through 2D Array and return rows which match term being looked for (In our case, most likely dates)
#     for i in range(len(data)):
#         for j in range(len(data[i])):
#             if data[i][j] == key:
#                 print(data[i])


def teamWinsDataFrame():
    data = list(csv.reader(open("Sports Reference NBA Data (2021 - 2022) Season.xlsx - sportsref_download.xls.csv")))
    res = []
    teamNames = []
    wins = []
    for i in range(len(data)):
        if data[i][1] != "Team" and data[i][1] != "League Averages":
            teamNames.append(data[i][1])
            wins.append(data[i][25])
    res = [teamNames, wins]
    return res