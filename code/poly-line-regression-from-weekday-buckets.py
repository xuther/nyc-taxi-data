#!/usr/bin/python

import csv
import locale
import numpy as np
import matplotlib
import os
import warnings
from sklearn import preprocessing

warnings.simplefilter('ignore', np.RankWarning)

Tract = "061-010100"
InDir = "./"
InFile = "./061-016700.csv"

#Open the out-CSV file for writing.
outCSV = open('./csv-out/lines-of-fit.csv', 'w+')
csvWriter = csv.writer(outCSV)

for file in os.listdir(InDir):
#for i in range(1):
#Debug
    #file = InFile

    if not file.endswith(".csv"):
        continue
    if file.find('061') == -1:
        continue

    print file
    Tract = file.split(".")[0]
    #Tract = file.split(".")[1]

    data = []

    with open(file) as f:
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

        if time[1] == '0':
            time[1] == '00'

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

    import matplotlib.pyplot as plt



    for i in range(len(data_by_days)):
    #for i in range(1):
        data_by_days[i] = sorted(data_by_days[i], key=lambda x: x[0])
        if len(data_by_days[i]) < 1:
            continue

        x = []
        y = []
        for j in range(len(data_by_days[i])):
            x.append(data_by_days[i][j][0])
            y.append(data_by_days[i][j][1])

        x = np.array(x)
        y = np.array(y)

        #Normalizing on a 1d array is depriciated. Transfer to 2d for normalization
        y = y.reshape(-1, 1)
        min_max_scaler = preprocessing.MinMaxScaler()
        y = min_max_scaler.fit_transform(y)

        #Bring it back to a 1d array.
        y = y.flatten()

        polyCount = 1
        bestResid = 1000000
        bestPoly = []
        decreasing = True

        # try at least the first five polynomial cuves - then continue until we get a decrease in SSE
        while polyCount <= 5 or decreasing:
            #print "calculatingFit"
            z, residual, _, _, _ = np.polyfit(x,y,polyCount, full=True)

            if residual < bestResid:
                bestResid = residual
                bestPoly = z
                decreasing = True
                #print "Better residual found."
            else:
                decreasing = False

            polyCount += 1

        print "Using " + str(len(bestPoly)) + " residuals.\nTried " + str(polyCount) + "."

        print Tract
        #Output the coefficients into the csv file.
        #csvWriter.writerow([Tract, i, bestPoly, bestResid])

        p = np.poly1d(bestPoly)
        print bestPoly

        alpha = 1

        if i < 4:
            alpha = .2

        xp = np.linspace(0, 100, 600)
        _ = plt.plot(x, y, '.', xp, p(xp), '-', label=labels[i], alpha=alpha)

    plt.ylim(-.25, 1.5)
    plt.legend(loc='upper left')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5, forward=True)
    fig.savefig('./out-figures/' + Tract +'-combined.png')
    fig.clf()
    #graph with pyplot

#close the out-csv file.
outCSV.close()
