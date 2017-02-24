import numpy as np
import csv
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy
from pylab import figure, axes, pie, title, show
import scipy.sparse as sparse
from sklearn import metrics
import matplotlib.pyplot as plt

TractToIndex = {}
IndexToTract = {}

#We need to build our distance matrix
infile = '/home/sir/Neighborhoods/Data/poly-line-compare/combined-diff-jan-2016.csv'

with open(infile, 'rb') as f:
    reader = csv.reader(f)
    reader.next()
    data = list(reader)

#we need to figure out how big our matrix is going to be and assign each to an index.
tracts = set()
for i in data:
    tracts.update({i[0], i[1]})

#assign each tract an Index
i = 0
for tract in tracts:
    TractToIndex[tract] = i
    IndexToTract[i] = tract
    i += 1

#Build the matrix
distanceMatrix = sparse.coo_matrix((len(tracts), len(tracts)))
distanceMatrix = distanceMatrix.tocsr()

#fill our matrix
for i in data:
    index1 = TractToIndex[i[0]]
    index2 = TractToIndex[i[1]]
    distanceMatrix[index1, index2] = float(i[2])
    distanceMatrix[index2, index1] = float(i[2])

for i in range(len(tracts)):
    distanceMatrix[i,i] = 0

z = linkage(distanceMatrix.toarray(), 'average', 'euclidean')

fig1 = plt.figure()
dn = hierarchy.dendrogram(z)
hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
dn1 = hierarchy.dendrogram(z, ax=axes[0], above_threshold_color='y',
    orientation='top')
fig2 = plt.figure()

fig.savefig("./test1.png")
fig1.savefig("./test2.png")
fig2.savefig("./test3.png")
