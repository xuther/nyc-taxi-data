#!/usr/bin/python

import csv  
import locale
import numpy as np
import scipy.stats as stats

infile = '/home/sir/Neighborhoods/Data/Usage/usage-files-by-borough/MN.csv'
outfile ='/home/sir/Neighborhoods/Data/Usage/out/061-out.csv'
outfilepercentages ='/home/sir/Neighborhoods/Data/Usage/out/061-out-percentages.csv'

inData = []

BlockMap = {
        'MN': 061
        }

with open(infile, 'r') as f:
    for line in f:
        inData.append(line.strip().split(','))

def translateTract(tract):
    tstring = tract.strip("\"")
    tstring = tstring.split('.')
    tstring[0] = tstring[0].replace(" ", "0")
    if len(tstring) == 1:
        return tstring[0] + '00'
    return tstring[0] + tstring[1]

def ParseData(line):
    return [line[4], line[5], line[27], line[28]]

def changeTract(line):
    line[0] = translateTract(line[0])
    return line

def removeQuotes(line):
    for i in range(1, 4):
        line[i] = line[i].strip("\"")
    return line

filteredData = [i for i in inData if len(i[4]) > 0]

parsedData = map(lambda x: ParseData(x), filteredData)
MappedTract = map(lambda x: changeTract(x), parsedData)
ToSave = map(lambda x: removeQuotes(x), MappedTract)

with open(outfile, 'w+') as f:
    writer = csv.writer(f)
    for line in ToSave:
        writer.writerow(line)

#Do our counts here
TractUsageTotals = {}
for line in ToSave:
    if line[0] not in TractUsageTotals:
        TractUsageTotals[line[0]] = {}
    if line[3] not in TractUsageTotals[line[0]]:
        TractUsageTotals[line[0]][line[3]] = 1
    else:
        TractUsageTotals[line[0]][line[3]] += 1

def convertToPercentages(line):
    line = list(line)
    line[1] = list(line[1].items()) #Convert to a list of tuples
    total = 0
    for i in range(len(line[1])):
        line[1][i] = list(line[1][i])
        total += line[1][i][1]
    for pair in line[1]:
        pair[1] = float(pair[1])/float(total)
    return line

def sortPercentages(percentages):
    percentages[1] = sorted(percentages[1], key = lambda x: x[1], reverse = True)
    return percentages


TractUsagePercentages = map(lambda x: convertToPercentages(x), TractUsageTotals.items()) 
TractUsagePercentages = map(lambda x: sortPercentages(x), TractUsagePercentages)
TractUsagePercentages = [x for x in TractUsagePercentages if x[0] != 'CT201000']
TractUsagePercentages.sort(key = lambda x: x[1][0][1], reverse = True)

def getLIneByTract(tract):
    for line in TractUsagePercentages:
        if line[0] == tract:
            return line

print TractUsagePercentages

TractUsageTotalWithBlanks = []
TractIndexes = []

for item in TractUsageTotals.items():
    TractIndexes.append(item[0])
    toAdd = []
    for i in range(1, 12):
        strValue = ""
        if i < 10:
            strValue = '0' + str(i)
        else:
            strValue = str(i)
        if strValue in item[1]:
            toAdd.append(item[1][strValue])
        else:
            toAdd.append(0)
    TractUsageTotalWithBlanks.append(toAdd)

#Calculate a chi2 on each and store the difference in an array

differences = []

for i in range(len(TractUsageTotalWithBlanks)):
    print TractIndexes[i]
    for j in range(i+1, len(TractUsageTotalWithBlanks)):
        print '\t', TractIndexes[j]
        res = stats.chi2_contingency(np.array([TractUsageTotalWithBlanks[i], TractUsageTotalWithBlanks[j]]))
        toReturn = [res[1], TractIndexes[i], TractIndexes[j]]
        differences.append(toReturn)

