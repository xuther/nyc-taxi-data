import numpy as np
import json
import csv
import os
import locale
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)

#InDirDepart = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/departures"
InDirDepart = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/departures/061-*"
#InDirArrive = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals"
InDirArrive = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/061-*"
OutFile = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/"

departures = sc.wholeTextFiles(InDirDepart)
arrivals = sc.wholeTextFiles(InDirArrive)

def timeToIndex(t):
    time = t.split(":")
    time[0] = locale.atoi(time[0])
    
    if time[1] == '0':
        time[1] == '00'
    
    time[1] = locale.atoi(time[1])
    y =  (time[1]/15) + (time[0] * 4)
    return y

def labelPointsWithTractAndArriveDepart(x, status):
    toReturn = []
    for y in x[1]:
        y = y.split(",")
        timeIndex = timeToIndex(y[1])
        point = timeIndex + (locale.atoi(y[0]) * 96) + (status * 672)
        toReturn.append((point, locale.atoi(y[2])))
    return toReturn

splitDepartures = departures.map(lambda x: (x[0].split("/")[-1].split(".")[0], x[1].split()[1:]))
pointedDepartures = splitDepartures.map(lambda x: (x[0], labelPointsWithTractAndArriveDepart(x, 0)))

splitArrivals = arrivals.map(lambda x: (x[0].split("/")[-1].split(".")[0], x[1].split()[1:]))
pointedArrivals = splitArrivals.map(lambda x: (x[0], labelPointsWithTractAndArriveDepart(x, 1)))

combined = sc.union([pointedDepartures, pointedArrivals])

combined = combined.reduceByKey(lambda x, y: x + y)

combined = combined.map(lambda x: (x[0], sorted(x[1], key = lambda y: y[0])))

collected = combined.collect()

with open(OutFile + "points.csv", 'w+') as f:
    with open(OutFile + "indicies.csv", 'w+') as indf:
        w = csv.writer(f)
        tractCount = 0
        for tract in collected:
            toWrite = []
            i = 0
            for j in range(1344):
                point = tract[1][i]
                if point[0] == j:
                    toWrite.append(point[1])
                    if i == len(tract[1])-1:
                        i = 0 
                    else:
                        i += 1
                else:
                    toWrite.append(0)
            w.writerow(toWrite)
            indf.write(str(tractCount) + "," + tract[0] + "\n")
            tractCount += 1
        
