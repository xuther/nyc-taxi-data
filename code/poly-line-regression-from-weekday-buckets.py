import locale
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

Tract = "061-010100"
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

labels = {0: "Monday",
1: "Tuesday",
2: "Wednesday",
3: "Thursday",
4: "Friday",
5: "Saturday",
6: "Sunday"}


for i in range(len(data_by_days)):
#for i in range(1):
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
    _ = plt.plot(xp, p(xp), '-', label=labels[i])

    plt.ylim(0, 1000)

plt.legend(loc='upper left')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5, forward=True)
fig.savefig('../' + Tract +'-combined.png')
    #graph with pyplot
