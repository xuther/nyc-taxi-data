import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import json
import csv

InFile = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/points.csv"
Labels ="/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/indicies.csv"

matrix = np.loadtxt(open(InFile, "rv"), delimiter = ",")

IndexLabels = []
with open(Labels) as f: 
    reader = csv.reader(f)
    for line in reader:
        IndexLabels.append(line)

for i in range(len(matrix)):
    matrix[i] = matrix[i] / matrix[i].max()


db = DBSCAN(min_samples=10, metric="manhattan").fit(matrix)
labels = db.labels_

cluster_count = len(set(labels)) - (1 if -1 in labels else 0)

km = KMeans(n_jobs = -1).fit(matrix)

km_labels = km.labels_

labeledTracts = []
for i in range(len(IndexLabels)):
    labeledTracts.append((IndexLabels[i][1], km_labels[i]))

print labeledTracts
