#!/usr/bin/python

from numpy import genfromtxt
import sys

#Get the arguemnts - input output county tract block
inFile = sys.argv[1]
outFile = sys.argv[2]
county = sys.argv[3]
tract = sys.argv[4]
block = sys.argv[5]

inData = genfromtxt(inFile,delimiter=",")

inData
