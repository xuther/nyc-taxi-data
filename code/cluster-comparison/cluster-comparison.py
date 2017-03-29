from pyspark import SparkConf, SparkContext
from datetime import datetime
from datetime import timedelta
import locale

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)


clusterList = "/home/sir/Neighborhoods/visualization/061/clusters/2.27176221836"
DataIn = "/home/sir/Neighborhoods/Data/Taxi/2015/all-processed.csv"

clusterDictionary = {}

clusters = sc.textFile(clusterList)

clusters = clusters.map(lambda x: x.split(","))
clusters = clusters.filter(lambda x: len(x) > 1) # Remove all unclustered clusters. 
clusters = clusters.map(lambda x: map(lambda x: x.strip(), x))
clusters = clusters.zipWithIndex()

clusters = clusters.map(lambda x: map(lambda e: (x[1], e), x[0])) # Create a list of tuples of cluster -> tract

#Create dictionary for lookup purposes later
local = clusters.flatMap(lambda x: x).collect()

def labelWithTrafficCluster(x):
    if x[2] + "-" + x[3] in clusterDictionary:
        x.append(clusterDictionary[x[2] + "-" + x[3]])
    else:
        x.append("9999999")
    if x[4] + "-" + x[5] in clusterDictionary:
        x.append(clusterDictionary[x[4] + "-" + x[5]])
    else:
        x.append("9999999")
    return x

for tract in local:
    clusterDictionary[tract[1]] = tract[0]


traffic = sc.textFile(DataIn)
Header = traffic.filter(lambda l: "tpep_pickup" in l)
traffic = traffic.subtract(Header)
traffic = traffic.map( lambda x : x.split(',') )

# -----
# For now we only care about Manhattan
# -----
traffic = traffic.filter(lambda x: x[6] == '061' and x[9] == '061')

def convertToDatetime(x):
    x[0] = datetime.strptime(x[0],'%Y-%m-%d %H:%M:%S')
    x[1] = datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S')
    x.append(x[0].weekday())
    x.append(x[1].weekday())
    return x  


#Throw out the indicies we don't care about for this to make the rdd smaller. 
traffic = traffic.map(lambda x: [x[0], x[1], x[6], x[7], x[9], x[10]])
#---------------------------------------------------------------------
#|StartTime|EndTime|StartCounty|StartTract|EndCounty|EndTract|StartCluster|EndCluster|
#|   0     |    1  |    2      |  3       |    4    |   5    |    6       |    7     |
#

#Label each trip with their start and end cluster.
clusterLabeledTraffic = traffic.map(lambda x: labelWithTrafficCluster(x))


#At this point we groups reduced by start tract - end cluster.
#We're gonna bucket the data. 

def convertToDatetime(x):
    x[0] = datetime.strptime(x[0],'%Y-%m-%d %H:%M:%S')
    x[1] = datetime.strptime(x[1],'%Y-%m-%d %H:%M:%S')
    x.append(x[0].weekday())
    x.append(x[1].weekday())
    return x

def BucketTime(x):
    x[0] = x[0] - timedelta(minutes=x[0].minute % 15, seconds = x[0].second, microseconds = x[0].microsecond)
    x[1] = x[1] - timedelta(minutes=x[1].minute % 15, seconds = x[1].second, microseconds = x[1].microsecond)
    return x


def convertAndBucket(x):
    x = convertToDatetime(x)
    x = BucketTime(x)
    return x

def timeToIndex(t):
    time = t.split(":")
    time[0] = locale.atoi(time[0])
    
    if time[1] == '0':
        time[1] == '00'
    
    time[1] = locale.atoi(time[1])
    y =  (time[1]/15) + (time[0] * 4)
    return y

def mapToTractAndCluster(x):
    toReturn = []
    split = x[0].split("-")
    toReturn.append(split[0] + "-" + split[1])
    toReturn.append([(split[2] + "-" + str(timeToIndex(split[3])), x[1])])
    return toReturn
        
bucketedLabelData = clusterLabeledTraffic.map(lambda x: convertAndBucket(x))
#---------------------------------------------------------------------
#|StartTime|EndTime|StartCounty|StartTract|EndCounty|EndTract|StartCluster|EndCluster|StartWeekday|EndWeekday|
#|   0     |    1  |    2      |  3       |    4    |   5    |    6       |    7     |     8      |    9     |
#

#Key with StartTract + EndCluster + StartWeekday + Start Bucket
trafficForCounting = bucketedLabelData.map(lambda x: (x[3] + "-" + str(x[7]) + "-" + str(x[8]) + "-" + str(x[1].hour)+":" + str(x[1].minute), 1))

#Count trips in bucket  
TrafficCounts = trafficForCounting.reduceByKey(lambda x, y: x + y) 

#Combine by start tract + end Cluster. Sort.

GroupByTractCluster = TrafficCounts.map(lambda x: mapToTractAndCluster(x))


GroupByTractCluster = GroupByTractCluster.reduceByKey(lambda x, y: x + y)
GroupByTractClusterSorted = GroupByTractCluster.map(lambda x: (x[0], sorted(x[1], key=lambda y: y[0])))


for tract in collected:
    with open("./list/" + tract[0], "w+") as f:
        w = csv.writer(f)
        for q in tract[1]:
            w.writerow(q)
            
