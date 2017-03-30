#!/usr/bin/python
from datetime import datetime
from datetime import timedelta
import os

dirTwo = "/home/sir/Neighborhoods/visualization/061/kmeansclusters/"
dirOne = "/home/sir/Neighborhoods/visualization/061/2015clusters/"
outPercentages = "/home/sir/Neighborhoods/code/cluster-comparison/comparisons/kmeans-2015-consistency.csv"
def calcAverage(percentages):
    averageSimilarity = 0.0
    count = 0.0
    for d in percentages:
        count += 1
        averageSimilarity += d[2]

    if averageSimilarity == 0 or count == 0:
        return 0.0
    
    averageSimilarity = averageSimilarity / count 
    return averageSimilarity

def printSimilarities(percentages):
    for v in percentages:
        print v[2] , "\t" , v[0] , "\t" , v[1]


def getAverageSimilarities(clusterOne, clusterTwo):
    clustersOne = []
    clustersTwo = [] 
    similarityPercentages = []

    with open(clusterOne, "r") as f:
        for line in f:
            line = line.strip()
            clustersOne.append(line.split(","))

    with open(clusterTwo, "r") as f:
        for line in f:
            line = line.strip()
            clustersTwo.append(line.split(","))

    #Compare every cluster to every other cluster
    for one in clustersOne:
        if len(one) < 2:
            continue
        oneSet = set(one)
        for two in clustersTwo:
           if len(two) < 2:
               continue
           common = oneSet.intersection(set(two)) 
           percentage = float(len(common)) / float(len(one))
           if percentage != 0:
               similarityPercentages.append((one, two, percentage))

    similarityPercentages.sort(key= lambda x: x[2])

    averageSimilarity = calcAverage(similarityPercentages)
    return averageSimilarity

similarities = []
for f in os.listdir(dirOne):
    for q in os.listdir(dirTwo):
       averages = getAverageSimilarities(dirOne + f, dirTwo + q) 
       similarities.append((f, q, averages))

similarities.sort(key=lambda x: x[2], reverse=True)
printSimilarities(similarities)


