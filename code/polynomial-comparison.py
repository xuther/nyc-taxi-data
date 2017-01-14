#!/usr/bin/python

import numpy as np
import sys
import csv

print len(sys.argv)

#Get the two files containing the polynomials to compare arguments
file1 = sys.argv[1]

data1 = json.loads(open(file1).read())[1:]

#Compare each poly, point by point, from 0 to range. Basically we we just take
#the difference calculated at each point, and add them up, that will give us the 'distance'
def comparePolys(poly1, poly2, r):
    first = np.array(poly1)
    second = np.array(poly2)

    a = np.poly1d(first)
    b = np.poly1d(second)

    diff = 0
    for i in range(r):
        diff += np.square(a(i) - b(i))
    return diff

def calcDifferences(data):
    differences = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            diff = comparePolys(data[i][2], data[j][2], 96)
            differences.append([str(data[j][0])+"-"+str(data[j][1]), strdata[i][0]+'-'+data[i][1], diff])
    return differences
