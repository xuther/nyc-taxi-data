#!/usr/bin/python
#
# Based on the paper Comparing Clusterings, Marina Melia, University of Washington
# www.stat.washington.edu/mmp/Papers/compare-cold.pdf
#

import math
import sys
import numpy as np

elementNames = {}
clusterings = []
curElementCount = 0
test = True

class cluster:

    def addElement(self, element):
        self.elements.append(element)

    def containsElement(self, element):
        return (element in self.elements)

    def getRandVar(self):
        if not self.randCalculated:
            self.randVar = float(len(self.elements))/float(curElementCount)
            self.randCalculated = True
        return self.randVar

    def getElements(self):
        return self.elements

    def __init__(self):
        self.randVar = 0.0
        self.randCalculated = False 
        self.elements = []

class clustering:
    def addCluster(self, cluster):
        cluster.parent = self
        self.clusters.append(cluster)

    def getClusters(self):
        return self.clusters

    def getTotal(self):
        return len(self.clusters)

    def calculateEntroy(self):
        runningSum = 0.0
        for cluster in self.clusters:
            runningSum += (cluster.getRandVar() * math.log(cluster.getRandVar(), 2.0))
        runningSum = runningSum * -1
        self.entropy = runningSum
        self.entropyCalculated = True

    def getEntropy(self):
        if not self.entropyCalculated:
            self.calculateEntroy()
        return self.entropy

    def getSource(self):
        return self.source

    def __init__(self, source):
        self.clusters = []
        self.entropy = 0.0
        self.entropyCalculated = False
        self.source = source 

def jointDistRandVar(clusterA, clusterB):
    intersection = set(clusterA.getElements()).intersection(clusterB.getElements())
    return float(len(intersection))/float(len(elementNames))

def mutualInformation(clusteringA, clusteringB):
    runningTotal = 0.0
    for a in clusteringA.getClusters():
        for b in clusteringB.getClusters():
            jointVar = jointDistRandVar(a, b)
            if jointVar == 0:
                continue
            runningTotal += jointVar * math.log(jointVar/(a.getRandVar()*b.getRandVar()), 2.0)
    return runningTotal


def variationOfInformation(clusteringA, clusteringB):
    mutInfo = mutualInformation(clusteringA, clusteringB)
    return clusteringA.getEntropy() - mutInfo + clusteringB.getEntropy() - mutInfo

#We assume a file with one cluster per line, identifiers comma delimited
def buildCluster(infile):
    global curElementCount
    c = clustering(infile)
    with open(infile, 'r') as f:
        for line in f:
            curCluster = cluster()
            line = line.strip()
            elements = line.split(',')
            for element in elements:
                element = element.strip()
                if element in elementNames:
                    curCluster.addElement(elementNames[element])
                else:
                    elementNames[element] = curElementCount
                    curElementCount += 1
                    curCluster.addElement(elementNames[element])
            c.addCluster(curCluster)
    clusterings.append(c)

def getSpaces(num):
    toReturn = ""
    for i in range(num):
        toReturn += " "
    return toReturn

if __name__ == '__main__':
    args = sys.argv
    if '-t' in args:
        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/testa.txt")
        print clusterings[0].getClusters()[0].getElements()
        print clusterings[0].getClusters()[1].getElements()
        print elementNames
        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/testb.txt")
        print clusterings[1].getClusters()[0].getElements()
        print clusterings[1].getClusters()[1].getElements()
        print elementNames

        print "RandomVariable 0,0: ", clusterings[0].getClusters()[0].getRandVar()
        print "RandomVariable 0,1: ", clusterings[0].getClusters()[1].getRandVar()
        print "Entropy 0: ", clusterings[0].getEntropy()

        print "RandomVariable 1,0: ", clusterings[1].getClusters()[0].getRandVar()
        print "RandomVariable 1,1: ", clusterings[1].getClusters()[1].getRandVar()
        print "Entropy 1: ", clusterings[1].getEntropy()
        
        print "Mutual Info 0-1: ", mutualInformation(clusterings[1], clusterings[0])
        print "Variation Info 0-1: ", variationOfInformation(clusterings[1], clusterings[0])

        print "Mutual Info 0-0: ", mutualInformation(clusterings[0], clusterings[0])
        print "Variation Info 0-0: ", variationOfInformation(clusterings[0], clusterings[0])

        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/testg.txt") #2
        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/testh.txt") #3
        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/teste.txt") #4
        buildCluster("/home/sir/Neighborhoods/code/cluster-comparison/test/testf.txt") #5

        print "Mutual Info single cluster to singletons: ", mutualInformation(clusterings[4], clusterings[5])
        print "Variation Info single cluster to singletons: ", variationOfInformation(clusterings[4], clusterings[5])
        print "Mutual Info no Overlap: ", mutualInformation(clusterings[2], clusterings[3])
        print "Variation Info no overlap: ", variationOfInformation(clusterings[2], clusterings[3])
    elif '-f' in args:
        ifile = args[args.index('-f')+1]
        if '-o' in args:
            ofile = args[args.index('-o')+1]
            savevars = True
        with open(ifile, 'r') as f:
            for line in f:
                if len(line.strip()) ==0:
                    continue
                buildCluster(line.strip())
        mutInfo = np.zeros((len(clusterings), len(clusterings)))
        varInfo = np.zeros((len(clusterings), len(clusterings)))

        for i in range(len(clusterings)):
            for j in range(len(clusterings)):
                mutInfo[i][j] = mutualInformation(clusterings[i], clusterings[j])
                mutInfo[j][i] = mutInfo[i][j]
                varInfo[i][j] = variationOfInformation(clusterings[i], clusterings[j])
                varInfo[j][i] = varInfo[i][j]

        sys.stdout.write("\n\n\n")
        for i in range(len(clusterings)):
            sys.stdout.write(str(i) + getSpaces(12 -len(str(i))) + clusterings[i].getSource() + '\n')
        sys.stdout.write("\n\n\n")
        sys.stdout.write(getSpaces(12)+ "Mutual Information\n\n")
        sys.stdout.write(getSpaces(12))
        for i in range(len(clusterings)):
            sys.stdout.write(str(i) + getSpaces(12-len(str(i))))
        for i in range(len(mutInfo)):
            print ""
            sys.stdout.write(str(i) + getSpaces(12-len(str(i))))
            for j in range(len(mutInfo[i])):
                if len(str(mutInfo[i][j])) < 11:
                    sys.stdout.write(str(mutInfo[i][j]) + getSpaces(12 - len(str(mutInfo[i][j]))))
                else:
                    sys.stdout.write(str(mutInfo[i][j])[:11] + " ")

        sys.stdout.write("\n\n\n")
        sys.stdout.write(getSpaces(12) + "Variation Of Information\n\n")
        sys.stdout.write(getSpaces(12))
        for i in range(len(clusterings)):
            sys.stdout.write(str(i) + getSpaces(12-len(str(i))))
        for i in range(len(varInfo)):
            print ""
            sys.stdout.write(str(i) + getSpaces(12-len(str(i))))
            for j in range(len(varInfo[i])):
                if len(str(varInfo[i][j])) < 11:
                    sys.stdout.write(str(varInfo[i][j]) + getSpaces(12 - len(str(varInfo[i][j]))))
                else:
                    sys.stdout.write(str(varInfo[i][j])[:11] + " ")
        sys.stdout.write("\n\n\n")


