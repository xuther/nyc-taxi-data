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
file1 = '/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/csv-out/ranked-differences.csv'
outfile1 = '/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals/csv-out/ranked-differences-combined.csv'

data = sc.textFile(file1)
header = data.first()
data1 = data.filter(lambda x: x != header)

def buildUniqueKey(a, b):
    a = a.split("-")
    a = a[0] + "-" + a[1]

    b = b.split("-")
    b = b[0] + "-" + b[1]
    vals = sorted([a,b])

    return vals[0]+"&"+vals[1]

def splitKey(x):
    v = x[0].split("&")
    return (v[0], v[1], (x[1][0]/x[1][1]))

data = data1.map(lambda x: x.split(","))

data = data.map(lambda x: (buildUniqueKey(x[0],x[1]), (float(x[2]), 1)))

data = data.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
data = data.map(lambda x: splitKey(x))
data = sorted(data.collect(), key = lambda x: x[2])


with open(outfile1, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(["tract", "tract", "squared-difference"])
    for record in data:
        writer.writerow(record)
