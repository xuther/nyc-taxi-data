#!/usr/bin/python

import numpy as np
import json
import csv
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)
file1 = '/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/csv-out/lines-of-fit.json'
outfile1 = '/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/csv-out/ranked-differences.csv'

data1 = json.loads(open(file1).read())[1:]

data = sc.parallelize(data1)

#Compare each poly, point by point, from 0 to range. Basically we we just take
#the difference calculated at each point, and add them up, that will give us the 'distance'
def comparePolys(poly1, poly2, r):
    first = np.array(poly1)
    second = np.array(poly2)

    a = np.poly1d(first)
    b = np.poly1d(second)

    diff = 0
    for i in range(r):
        diff += np.square(a(i) - b(i))
    return diff

def calcDifferences(data):
    differences = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            diff = comparePolys(data[i][2], data[j][2], 96)
            differences.append([str(data[j][0])+"-"+str(data[j][1]), str(data[i][0])+'-'+str(data[i][1]), diff])
    return differences


weekdayGrouping = data.map(lambda x: (x[1], [x]))
weekdayGrouping = weekdayGrouping.reduceByKey(lambda x, y: x+y)

differences = weekdayGrouping.map(lambda x: calcDifferences(x[1]))

sortedDifferences = differences.map(lambda x: sorted(x, key=lambda y: y[2]))
mixedDifferences = sorted(sortedDifferences.flatMap(lambda x: x).collect(), key=lambda y: y[2])

#print out to a file
with open(outfile1, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(["tract-weekday-1", "tract-weekday-1", "squared-difference"])
    for record in mixedDifferences:
        writer.writerow(record)
