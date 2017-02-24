import csv
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)
inFile1 = '/home/sir/Neighborhoods/Data/Test/Buckets-Out-Arrival/2016-1/csv-out/out-difference-combined.csv'
inFile2 = '/home/sir/Neighborhoods/Data/Test/Weekday-15min-Arrival-Buckets/csv-out/ranked-differences-combined.csv'
outfile1 = '/home/sir/Neighborhoods/Data/poly-line-compare/combined-diff-jan-2016.csv'

data1 = sc.textFile(inFile1)
data2 = sc.textFile(inFile2)

header = data1.first()
data1 = data1.filter(lambda x: x != header)

header = data2.first()
data2 = data2.filter(lambda x: x != header)

dataAll = data1.union(data2)

dataAll = dataAll.map(lambda x: x.split(','))

def splitKey(x):
    v = x[0].split("&")
    return (v[0], v[1], (x[1][0]/x[1][1]))

data = dataAll.map(lambda x: (x[0] + "&" + x[1], (float(x[2]), 1)))
data = data.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

data = data.filter(lambda x: x[1][1] == 2)
data = data.map(lambda x: splitKey(x))
data = sorted(data.collect(), key = lambda x: x[2])

with open(outfile1, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(["tract", "tract", "squared-difference"])
    for record in data:
        writer.writerow(record)

