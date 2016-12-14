from datetime import datetime
from datetime import timedelta

test = sc.textFile("/home/sir/Neighborhoods/Data/Taxi/2016-out/1-yellow-out.csv")

Header = test.filter(lambda l: "tpep_pickup" in l)
pruned = test.subtract(Header)
array = pruned.map( lambda x : x.split(',') )

def convertToDatetime(x):
    x[0] = datetime.strptime(x[0],'%Y-%m-%d %H:%M:%S')
    x[1] = datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S')
    x.append(x[0].weekday())
    x.append(x[1].weekday())
    return x  

array1 = array.map( lambda x: convertToDatetime(x))

def BucketTime(x): 
    x[0] = x[0] - timedelta(minutes=x[0].minute % 5, seconds = x[0].second, microseconds = x[0].microsecond)
    x[1] = x[1] - timedelta(minutes=x[1].minute % 5, seconds = x[1].second, microseconds = x[1].microsecond)
    return x


array2 = array1.map(lambda x: BucketTime(x))
#map to county + Tract + block + day of week + hour + minute (Bucket))
array3 = array2.map(lambda x: (x[6]+":"+x[7]+":"+x[8]+"-"+str(x[12])+":"+str(x[0].hour)+":"+str(x[0].minute), 1))
step4 = array3.reduceByKey( lambda a,b: a+b)

#Map these now to a list of county/tract/block with week hour minute county

def SplitOnCounty(x):
    toReturn = []
    splitVals = x[0].split("-")
    toReturn.append(splitVals[0])
    date = datetime.strptime(splitVals[1], "%w:%H:%M")    
    toReturn.append(([date],[x[1]]))
    return toReturn

step5 = step4.map( lambda x: SplitOnCounty(x))    
step6 = step5.reduceByKey( lambda a,b: (a[0] + b[0], a[1]+b[1]))

data = step6.collect()



import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

def mapData(Data):
    dates = matplotlib.dates.date2num(Data[1][0])
    pyplot.plot_date(dates, Data[1][1])
    pyplot.savefig("/home/sir/Neighborhoods/Data/"+Data[0].replace(":", "-")+".png")

