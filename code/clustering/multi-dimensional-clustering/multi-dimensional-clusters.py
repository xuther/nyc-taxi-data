import numpy as np
from sklearn.cluster import DBSCAN
import json
import csv

InFile = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/points.csv"
Labels ="/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/indicies.csv"

matrix = np.loadtxt(open(InFile, "rv"), delimiter = ",")

for i in range(len(matrix)):
    matrix[i] = matrix[i] / matrix[i].max()


db = DBSCAN(min_samples=10, metric="manhattan").fit_predict(matrix)
labels = db.labels_

cluster_count = len(set(labels)) - (1 if -1 in labels else 0)

