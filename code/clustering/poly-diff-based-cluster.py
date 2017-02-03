import numpy as np
import csv
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy
from pylab import figure, axes, pie, title, show
from sklearn import metrics
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

TractToIndex = {}
IndexToTract = {}

#We need to build our distance matrix
infile = '/home/sir/Neighborhoods/Data/poly-line-compare/combined-diff-jan-2016.csv'
outfile = '/home/sir/Neighborhoods/Data/poly-line-compare/cluster-mapping-jan-2016.csv'

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
distanceMatrix = np.zeros((len(tracts), len(tracts)))

#fill our matrix
for i in data:
    index1 = TractToIndex[i[0]]
    index2 = TractToIndex[i[1]]
    # we can't have zero distance - set it to something big.
    if (i[2] == 0):
        distanceMatrix[index1, index2] = float(50)
        distanceMatrix[index2, index1] = float(50)
    else:
        distanceMatrix[index1, index2] = float(i[2])
        distanceMatrix[index2, index1] = float(i[2])

def getDistance(x,y):
    return distanceMatrix[x[0],y[0]]

tractList = []
for i in range(len(tracts)):
    tractList.append([i])

b = pdist(tractList, getDistance)


z = linkage(b, 'average')

fig1 = plt.figure(figsize=(10,10))
hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
dn = hierarchy.dendrogram(z)

fig1.savefig("/home/sir/Neighborhoods/Data/poly-line-compare//dendogram.png")

num_clusters = 30
clusters = hierarchy.fcluster(z, num_clusters, 'maxclust')

TractClusterMapping = []

for i in range(len(clusters)):
    TractClusterMapping.append((IndexToTract[i], clusters[i]))

with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    writer.writerow(["tract", "cluster"])
    for record in TractClusterMapping:
        writer.writerow(record)

count = 0

for i in range(len(z)):
    if z[i][2] < 10:
        count += 1
    else:
        break

l = np.ndarray(shape=(count, 4), dtype=float)

c = 0
for i in range(len(z)):
    if z[i][2] < 10:
        l[i] = z[i]
    else:
        break
