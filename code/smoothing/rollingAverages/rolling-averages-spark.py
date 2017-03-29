#!/usr/bin/python

import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
import locale
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)

indir = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals"
values = []
dataset = None
GeneratePlot = True


dataset = sc.wholeTextFiles(indir + "/*.csv")

def appendTractToEachPoint(x):
    toReturn = []
    for point in x[1]:
        splitPoint = point.split(",")
        toReturn.append((x[0] + " | " + splitPoint[0], [tuple(splitPoint[1:])]))
    return toReturn

#Run a rolling average
def runRolling(x):
    df = pd.DataFrame.from_records(x)
    s = pd.Series(df[1].values, index=df[0].values)
    #s = s/s.max() #Normalize
    r = s.rolling(window=3, center=True, win_type='boxcar').mean()
    return zip(r.index, r)

def timeToIndex(t):
    time = t.split(":")
    time[0] = locale.atoi(time[0])
    
    if time[1] == '0':
        time[1] == '00'
    
    time[1] = locale.atoi(time[1])
    y =  (time[1]/15) + (time[0] * 4)
    return y

def runTimeToIndex(x):
    toReturn = []
    for y in x:
        toReturn.append((timeToIndex(y[0]), locale.atoi(y[1])))
    return toReturn

def tupleListToStringList(x):
    toReturn = []
    for y in x:
       toReturn.append(str(y[0]) + "," + str(y[1]))
    return toReturn

def plotAndSave(x):
    if (GeneratePlot and "061-" in x[0]):
        for weekday in x[1]:
            temp = zip(*weekday[1][1:-1]) 
            plt.plot(temp[0], temp[1])
            fig = matplotlib.pyplot.gcf()
            fig.set_size_inches(18.5, 10.5, forward=True)
            fig.savefig(indir + "/rolling-averages/figures/" + row[0].split('.')[0].strip() + "-" + weekday[0].strip() + ".png")
            fig.clf()

dataset1 = dataset.map(lambda x: (x[0].split("/")[-1], x[1].split()[1:]))
dataset2 = dataset1.flatMap(lambda x: appendTractToEachPoint(x))
dataset3 = dataset2.reduceByKey(lambda x,y: x + y)
dataset4 = dataset3.map(lambda x: (x[0], runTimeToIndex(x[1])))
dataset4 = dataset4.map(lambda x: (x[0], sorted(x[1], key=lambda x: x[0])))

dataset5 = dataset4.map(lambda x: (x[0], runRolling(x[1])))
dataset6 = dataset5.map(lambda x: (x[0], sorted(x[1], key=lambda x: x[0])))
dataset7 = dataset6.map(lambda x: (x[0].split("|")[0], [(x[0].split("|")[1], x[1])]))
dataset8 = dataset7.reduceByKey(lambda x,y: x + y)

data = dataset8.collect()

for row in data:
    plotAndSave(row)
    for weekday in row[1]:
        with open(indir + "/rolling-averages/" + row[0].split('.')[0].strip() + "-" + weekday[0].strip() + ".csv", "w+") as f:
            writer = csv.writer(f)
            writer.writerows(weekday[1])
        
