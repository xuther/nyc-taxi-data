import csv
import sys

if len(sys.argv) != 3:
    print ("Usage: python heirarchical-cluster.py [in file] [out file]")
    exit(-1)

in_file = sys.argv[1]
out_file = sys.argv[2]

sortedDistances = [] #Tuples to be sorted by distances.
clusterDistances = {}
clusters = {} # Clusters is a list of tracts in a cluster - number -> list.
clusterAssignment = {} #The individual assignments of tracts to clusters. Tract -> Cluster. 
currentClusterCount = 0
combinations = [] #The list steps we took to combine the clusters - first to last.

class distanceWrapper(object):
    def __init__(self, distance, a, b):
        self.distance = distance
        self.a = a
        self.b = b
    def __str__(self):
        return "(" + str(self.a) + "," + str(self.b) + ", dist: " + str(self.distance) + ")"
    def __repr__(self):
        return "(" + str(self.a) + "," + str(self.b) + ", dist: " + str(self.distance) + ")"


#Check to see if tract is already in a cluster. 
#If not, assign it to it's own. 
def checkToAdd(tract):
    global currentClusterCount
    if tract not in clusterAssignment:
        clusterAssignment[tract] = currentClusterCount
        clusterDistances[currentClusterCount] = {}
        clusters[currentClusterCount] = [tract]
        currentClusterCount = currentClusterCount + 1

def addDistances(a,b, dist):
    toInsert = distanceWrapper(dist, clusterAssignment[a],clusterAssignment[b])
    sortedDistances.append(toInsert)
    clusterDistances[clusterAssignment[b]][clusterAssignment[a]] = toInsert
    clusterDistances[clusterAssignment[a]][clusterAssignment[b]] = toInsert

def saveClusters(clusters, val):
    combinations.append((clusters, val)) #this is terribly inefficient, but allows for a really easy slider to see different combination thresholds

def recalculateDifferences(a,b):
    #take every distance for a and b, and average them together. 
    for key in clusterDistances[a]:
        if key in clusterDistances[b] and b != key:
            newDistance = ((clusterDistances[a][key].distance * len(clusters[a])) + (clusterDistances[b][key].distance * len(clusters[b]))) / (len(clusters[a]) + len(clusters[b]))
            clusterDistances[a][key].distance = newDistance #reassign distance
            clusterDistances[key].pop(b)
            sortedDistances.remove(clusterDistances[b][key]) #remove b -> key from array as it is now represented in the distance from a -> key
        elif b == key:
            continue
        else:
            print 'error, key ' + str(key) + ' not found for distance from cluster ' + str(b)
    clusterDistances.pop(b)
    sortedDistances.remove(clusterDistances[a][b])
    sortedDistances.sort(key=lambda x: x.distance) #Resort the sorted distances 
    clusterDistances[a].pop(b)


def combineClusters(a, b):
    recalculateDifferences(a,b)
    for toReassign in clusters[b]:
        clusterAssignment[toReassign] = a
    clusters[a] = clusters[a] + clusters[b]
    clusters.pop(b) # Remove b

def setup():
    #Setup
    with open(in_file) as f: 
        for line in csv.reader(f):
            #check to see if we've read in either of the tracts before, if not, add them to ther own cluster.
            checkToAdd(line[1])
            checkToAdd(line[0])
            addDistances(line[0],line[1], float(line[2]))
    sortedDistances.sort(key=lambda x: x.distance)


setup() #setup 
saveClusters(clusters.copy(), 0)

while len(clusters) > 1:
    curCombine = sortedDistances[0]
    if curCombine.a <= curCombine.b:
        combineClusters(curCombine.a, curCombine.b)
    else:
        combineClusters(curCombine.b, curCombine.a)
    saveClusters(clusters.copy(),curCombine.distance)

with open(out_file, "w+") as f:
    i = 0
    for c in combinations:
        toWrite =""
        f.write(str(c[1]) + " | " + str(c[0]) + "\n") 
        print str(i) + "," + str(c[1])
        i +=1 
