#!/usr/bin/python
from os import listdir

directory = "./061/clusters"

def getClusteringLevels():
    i = 0
    clusterList = []
    clusterDict = {}
    for f in listdir(directory):
        clusterList.append((float(f), f))
    clusterList.sort(key=lambda x: x[0])
    for l in clusterList:
        clusterDict[i] = l
        i += 1 
    return clusterDict

def getClusterCount(f):
    count = 0
    with open(directory + "/" + f, 'r') as fi:
        for line in fi:
            if len(line.split(',')) > 1:
                count += 1
    return count

clusterDict = getClusteringLevels()

counts = []
for i in range(len(clusterDict)):
    counts.append(str(i) + "," + str(getClusterCount(clusterDict[i][1])))

print counts

with open('./counts.csv', 'w+') as f:
    for line in counts:
        f.write(line + "\n")
