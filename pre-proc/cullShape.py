import shapefile 

pathToFile = ("/mnt/c/Users/joseph/Documents/Code/BigData/Neighborhoods/data/census/counties/tl_2016_us_county")
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

records = sf.shapeRecords()

for i in range(len(records)):
    if (records[i].record[1] in counties and records[i].record[0] == newYorkFIPS):
        indicies.append(i)

print indicies

#open the shapefile for reading. 
#Remove all records/shapes execpt for the five that were found above.

e = shapefile.Editor(pathToFile)

for i in range (len(records)-1, 0, -1):
    if (i not in indicies):
        e.delete(i)
        del e.records[i]
    else: 
        print i 

e.save(pathToFile)

