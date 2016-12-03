#!/usr/bin/python
import shapefile
import json

pathToFile = "C:/Users/joseph/Documents/Code/BigData/Neighborhoods/data/census/tl_2010_36_tabblock10/tl_2010_36_tabblock10"
pathOut = "C:/Users/joseph/Documents/Code/BigData/Neighborhoods/data/census/blockData.json"
sf = shapefile.Reader(pathToFile)

#Pull out othe points that we want saved
indicies = []

#Counties that we care about

#Queens - 081
#Kings = 047
#New York = 061
#Bronx = 005
#Richmond = 085

counties = ['081','047','061','005','085']
newYorkFIPS = '36'

fields = sf.fields
records = sf.shapeRecords()

dataToExport = []


for i in range(len(records)):
    if (records[i].record[1] in counties and records[i].record[0] == newYorkFIPS):
        row = {}
        for j in range(len(fields)-1):
            if (type(records[i].record[j]) is bytes):
                row[fields[j + 1][0]] = str(records[i].record[j])
            else:
                row[fields[j+1][0]] = records[i].record[j]
        row["points"] = records[i].shape.points
        dataToExport.append(row);


with open(pathOut, 'w+') as fp:
    json.dump(dataToExport, fp)
