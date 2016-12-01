#!/usr/bin/python

import shapefile
import csv


#given the list of counties (the shapefile) - find which county the x,y fall in and return the
#County FIPS code. 
def findCounty(x, y, counties):
    for county in counties: 
        if point_in_poly(x, y, county.shape.points):
            return county.record[1]

def findTract(x, y, tracts, indiciesToCheck):
    for i in indiciesToCheck:
        if point_in_poly(x,y,tracts[i].shape.points):
            return tracts[i].record[2]

    
def findBlock(x, y, blocks, indiciesToCheck):
    for i in indiciesToCheck:
        if point_in_poly(x,y,blocks[i].shape.points):
            return blocks[i].record[4]
    
#raycasting algorithm found at http://geospatialpython.com/
def point_in_poly(x,y,poly):
    #check if point is a vertex
    if (x,y) in poly: return 1
    
    # check if point is on a boundary
    for i in range(len(poly)):
        p1 = None
        p2 = None
        if i==0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i-1]
            p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
            return 1
      
    n = len(poly)
    inside = False
    
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    
    if inside: return 1
    else: return 0 


censusBasePath = "/home/sir/Neighborhoods/Data/Census/"

countiesPath = censusBasePath+"Counties/tl_2010_36_county10"
tractsPath = censusBasePath+"Tracts/tl_2010_36_tract10"
blockPath = censusBasePath+"Blocks/tl_2010_36_tabblock10"

#These are the county codes (COUNTYFP10) associated with the counties we care about
# Bronx - 005
# New York - 061
# Queens - 081
# Kings  -047
# Richmond -085 

counties = shapefile.Reader(countiesPath)
tracts = shapefile.Reader(tractsPath)
blocks = shapefile.Reader(blockPath)

countiesToTracts = {}
tractsToBlocks = {}
BlocksToBlockIndex = {}

#create maps mapping the parent groups to their collections of 

#for block record[3] correlates to the block number
#record[2] correlates to the Tract Code
count = 0

for i in range(len(blocks.records())-1):
    tract = blocks.record(i)[2]
    if tract in tractsToBlocks:
        tractsToBlocks[tract].append(i)
    else:
        tractsToBlocks[tract] = [i]
    BlocksToBlockIndex[blocks.record(i)[3]] = i
    count += 1
print "Done with block to tract " + str(len(tractsToBlocks)) + " tracts found."
print str(count) + " blocks mapped."

#record[1] corresponds to county
#build our counties to tracts now
count = 0
for i in range (len(tracts.records())-1):
    county = tracts.record(i)[1]
    if county in countiesToTracts:
        countiesToTracts[county].append(i)
    else:
        countiesToTracts[county] = [i]
    count +=1

print "Done with tract to county. " + str(len(countiesToTracts)) + " counties mapped."
print str(count) + " tracts mapped."


dataLocation = "/home/sir/Neighborhoods/Data/Taxi/temp.csv"
data = []
header = ""

print "Importing points"
f = open(dataLocation, 'rb')
reader = csv.reader(f)
rownum = 0
for row in reader:
    if(rownum == 0):
        header = row
    else:
        data.append(row)
    rownum += 1

f.close()


print "Found " + str(rownum) + " points."

print "Mapping points and removing superfluous data"

importantColums = [1,2,5,6,9,10]

#where the x,y points are in the newRow schema
dataIndies = [(2,3),(4,5)]

newData = []
newHeaders = []

for i in importantColums:
    newHeaders.append(header[i])

newHeaders.append("pickup_county_FP")
newHeaders.append("pickup_tract_id")
newHeaders.append("pickup_block_id")

newHeaders.append("dropoff_county_FP")
newHeaders.append("dropoff_tract_id")
newHeaders.append("dropoff_block_id")

#foundxy = {} 

for row in data:
    print "starting row"
    newRow = []
    
    #get important data
    for i in importantColums:
        newRow.append(row[i])
    print "removed extra data"
    
    #find the block that contains each point
    for xy in dataIndies:
        print "finding area for point: " + newRow[xy[1]]+ "," + newRow[xy[0]] 
        #check to is if by chance we've already mapped this point
        #if xy[0]+xy[1] in foundxy:
        #   newRow.append(foundxy[xy[0]+xy[1])
        #   continue
        
        curX = float(newRow[xy[0]])
        curY = float(newRow[xy[1]])

        #get the county
        found_county = findCounty(curX, curY, counties.shapeRecords())
        print "Found county: " + str(found_county)
        newRow.append(found_county)        
        
        found_tract = findTract(curX, curY, tracts.shapeRecords(), countiesToTracts[found_county])
        print "Found tract: " + str(found_tract)
        newRow.append(found_tract)
        
        found_block = findBlock(curX, curY, blocks.shapeRecords(), tractsToBlocks[found_tract])
        print "Found block: " + str(found_block)
        newRow.append(found_block)

print newHeaders
print newData
