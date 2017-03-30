#!/usr/bin/python
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import json
import csv

InFile = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/points.csv"
Labels ="/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/indicies.csv"
OutDir = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/"

matrix = np.loadtxt(open(InFile, "rv"), delimiter = ",")

IndexLabels = []

with open(Labels) as f: 
    reader = csv.reader(f)
    for line in reader:
        IndexLabels.append(line)

for i in range(len(matrix)):
    matrix[i] = matrix[i] / matrix[i].max()

def clusterAndSave(clusterCount):
    km = KMeans(n_clusters = clusterCount, max_iter = 10000, n_jobs = -1).fit(matrix)

    km_labels = km.labels_

    labeledTracts = []
    clusters = {}
    for i in range(len(IndexLabels)):
        labeledTracts.append((IndexLabels[i][1], km_labels[i]))
        if km_labels[i] not in clusters:
            clusters[km_labels[i]] = [IndexLabels[i][1]]
        else:
            clusters[km_labels[i]].append(IndexLabels[i][1]) 

    with open(OutDir +"/clusters/" + str(clusterCount), "w+") as f:
        writer = csv.writer(f)
        for k in clusters:
            writer.writerow(clusters[k])

for i in range(2, 50):
    clusterAndSave(i)
