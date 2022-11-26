import csv

# Key to search for (implemented for testing and making sure filtering will work down the line)
key = input("Enter key you'd like to search for: ")
# Create a 2D Array by reading csv data
data = list(csv.reader(open("NBA_Team_Stats.csv")))

# Look through 2D Array and return rows which match term being looked for (In our case, most likely dates)
for i in range(len(data)):
  for j in range(len(data[i])):
      if data[i][j] == key:
        print(data[i])




