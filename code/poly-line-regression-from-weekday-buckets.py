import locale
import numpy as np
import matplotlib.pyplot as plt

InFile = "./061-010100.csv"

data = []

with open(InFile) as f:
    headers = f.readline()

    line = f.readline()
    while line != "":
        data.append(str.strip(line).split(","))
        line = f.readline()

# Need to translate the Y axis - scales go from 00:00 (midnight) to 23:45 in 15 minute increments.
# Thus there are 24*4 points - label them from 0 to 95
for i in range(len(data)):
    time = data[i][1].split(":")
    time[0] = locale.atoi(time[0])
    time[1] = locale.atoi(time[1])
    y =  (time[1]/15) + (time[0] * 4)
    data[i].append(y)
    data[i][0] = locale.atoi(data[i][0])
    data[i][2] = locale.atoi(data[i][2])

#arrays to accept our values
data_by_days = [[],[],[],[],[],[],[]]

#Build our x,y where x is our time (encoded) and y is the number of trips during that period for that day.
for i in range(len(data)):
    data_by_days[data[i][0]].append([data[i][3],data[i][2]])

polynomials = []
#sort the array
#for i in range(len(data_by_days)):
for i in range(1):
    data_by_days[i] = sorted(data_by_days[i], key=lambda x: x[0])
    x = []
    y = []
    for j in range(len(data_by_days[i])):
        x.append(data_by_days[i][j][0])
        y.append(data_by_days[i][j][1])

    x = np.array(x)
    y = np.array(y)
    z = np.polyfit(x,y,5)
    polynomials.append(z)

    p = np.poly1d(z)

    xp = np.linspace(0, 100, 600)
    out = plt.plot(x, y, '.', xp, p(xp), '-')

    plt.ylim(0, 500)

    plt.show()
    #graph with pyplot
