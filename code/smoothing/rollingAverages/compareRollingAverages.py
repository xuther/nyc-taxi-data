#!/usr/bin/python

import csv
import numpy as np
import locale
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "16g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)

indir = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/rolling-averages"
outfile = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/rolling-averages/differences.csv"

def compareSets(a, b):
    #Ensure that a and b are both sorted
    a = sorted(a, key=lambda x: x[0])
    b = sorted(b, key=lambda x: x[1])
    diff = 0
    curA = 0
    curB = 0 #Not all tracts have entries for all times 
    for i in range(max(len(a), len(b))):
        aVal = 0
        bVal = 0
        if a[curA] == i:
            aVal = a[curA]
            curA += 1 
        if b[curB] == i:
            bVal = b[curB]
            curB += 1
        diff += np.square(aVal - bVal)
    return diff
            


def calcDifferences(data, weekday):
    differences = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            diff = compareSets(data[i][1], data[i][1])
            if diff == 0:
                continue
            print diff
            differences.append([data[i][0] + "-" + str(weekday), data[j][0] + "-" + str(weekday), diff])
    return differences

def splitStringArray(x):
    toReturn = []
    for line in x:
        line = line.split(',')
        line[0] = int(line[0])
        toReturn.append(line)
    return toReturn

dataset = sc.wholeTextFiles(indir + "/*.csv")

dataset1 = dataset.map(lambda x: (x[0].split("/")[-1].split(".csv")[0], x[1].split()[1:-1]))
dataset2 = dataset1.map(lambda x: (x[0], splitStringArray(x[1])))
KeyedByWeekday = dataset2.map(lambda x: (x[0][-1], [(x[0][:-2], x[1])]))
GroupedByWeekday = KeyedByWeekday.reduceByKey(lambda x, y: x +y)
differences = GroupedByWeekday.map(lambda x: calcDifferences(x[1], x[0]))
sortedDifferences = differences.map(lambda x: sorted(x, key=lambda y: y[2]))
sortedDifferences.saveAsTextFile(indir + "/out")
mixedDifferences = sorted(sortedDifferences.flatMap(lambda x: x).collect(), key=lambda y: y[2])

#print out to a file
with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(["tract-weekday-1", "tract-weekday-1", "squared-difference"])
    for record in mixedDifferences:
        writer.writerow(record)
