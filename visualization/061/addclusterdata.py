#!/bin/python

import json

jsonin = './tl_2010_36061_tract10.geojson'
jsonout = './jsonout.geojson'
results = './final-clusters.csv'
# results = "./Combined_Results.csv"

clusterAssignments = {}

i = 0

for line in open(results):
    line = line.strip()
    vals = line.split(",")
    for val in vals:
        clusterAssignments[val.strip()] = i 
    i += 1
print(clusterAssignments)
data = []

with open(jsonin) as js:
    data = json.load(js)

for i in data['features']:
        clusterName = i["properties"]["COUNTYFP10"] + "-" + i["properties"]["TRACTCE10"]
        if clusterName in clusterAssignments: 
            i["properties"]["cluster"] = clusterAssignments[clusterName]
            print "Labeling tract into cluster"
        else:
            i["properties"]["cluster"] = -1
             

with open(jsonout, 'w+') as js:
    json.dump(data, js) 
