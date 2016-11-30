#!/usr/bin/python

import shapefile

shapeFileLocation = "/home/sir/Neighborhoods/Data/Census/Blocks/tl_2016_36_tabblock10"

#These are the county codes (COUNTYFP10) associated with the counties we care about
# Bronx - 005
# New York - 061
# Queens - 081
# Kings  -047
# Richmond -085 

# For completion we include the counties in surrounding areas
# Nassau - 059
# Rockland - 087
# West-Chester - 119

importantCounties = {'005','061','081','047','085'}#,'059','087','119'} 

sf = shapefile.Reader(shapeFileLocation)
shapes = sf.shapes()
records = sf.records()

#Find all indexes of records/shapes that we care about (they're included in the counties 
#in importantCounties

indicies = [];

for i in range(len(records)):
    if records[i][1] in importantCounties: 
        indicies.append(i)

shape[162].shapetype


