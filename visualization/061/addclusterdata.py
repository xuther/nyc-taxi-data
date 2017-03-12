#!/bin/python

import json

jsonin = './tl_2010_36061_tract10.geojson'
jsonout = './staic/jsonout.geojson'
results = '../../Data/Test/2015-aggregated/heriarchical-clusters.csv'
# results = "./Combined_Results.csv"

def insert(infile, outfile):
    clusterAssignments = {}

    i = 0

    for line in open(infile):
        line = line.strip()
        vals = line.split(",")
        if len(vals) < 2:
            continue
        for val in vals:
            clusterAssignments[val.strip()] = i 
        i += 1
    data = []

    with open(jsonin) as js:
        data = json.load(js)

    for i in data['features']:
            clusterName = i["properties"]["COUNTYFP10"] + "-" + i["properties"]["TRACTCE10"]
            if clusterName in clusterAssignments: 
                i["properties"]["cluster"] = clusterAssignments[clusterName]
            else:
                i["properties"]["cluster"] = -1
                 

    with open(outfile, 'w+') as js:
        json.dump(data, js) 

if __name__ == "__main__":
    insert(results, jsonout)
