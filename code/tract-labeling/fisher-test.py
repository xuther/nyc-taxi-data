import numpy as np
import json
import csv
import locale
from pyspark import SparkConf, SparkContext
import rpy2
from rpy2 import robjects
from rpy2.robjects.packages import importr

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)

#infile = '/home/sir/Neighborhoods/code/tract-labeling/test.txt'
#intracts =  '/home/sir/Neighborhoods/code/tract-labeling/test-tract.txt'
infile = '/home/sir/Neighborhoods/code/tract-labeling/usage-out.csv'
intracts =  '/home/sir/Neighborhoods/code/tract-labeling/index-out.csv'
outfile = '/home/sir/Neighborhoods/code/tract-labeling/fisher-out.csv'

raw = []

with open(infile, 'r') as f:
    for line in f:
       l = line.strip().split(',')
       for i in range(len(l)):
           l[i] = locale.atoi(l[i])
       raw.append(l) 

tractIndexes = []
with open(intracts, 'r') as f:
    for line in f:
       tractIndexes.append(line.strip()) 

concatenated = []
for i in range(len(raw)):
    concatenated.append((tractIndexes[i], raw[i]))

#Build our power set
fullSet = []
for i in range(len(concatenated)):
    for j in range(i+1, len(concatenated)):
        fullSet.append([concatenated[i], concatenated[j]])

sparkSet = sc.parallelize(fullSet)

#run our fisher's exact test on it now.

def runFishersTest(a):
    #We have a value that is a tuple of tuples in the form of 
    #((Tract, [values]), (Tract, [values]))
    #We have to have enough data in the set.
    doubleNonZeroCount = 0
    for i in range(len(a[0][1])):
        if (a[0][1][i] != 0 and a[1][1][i] != 0):
            doubleNonZeroCount += 1
    if (doubleNonZeroCount < 1):
        print "Not Enough Information", a
        return []
    data = robjects.r['matrix'](robjects.FloatVector(a[0][1]) + robjects.FloatVector(a[1][1]), nrow=2)
    pVal = robjects.r['fisher.test'](data, simulate_p_value = True, B = 10000)
    return [a[0][0], a[1][0], pVal[0][0]]

pValues = sparkSet.map(lambda x: runFishersTest(x))
pValues = pValues.filter(lambda x: len(x) > 0)

collectedVals = pValues.collect()

with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    for val in collectedVals:
        writer.writerow(val)

