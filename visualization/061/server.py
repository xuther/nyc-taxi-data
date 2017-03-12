import web
import json
from os import listdir
import addclusterdata

urls = ('/json/(.*)', 'get_json',
        '/count/(.*)', 'getNumberOfClustersAtSize',
        '/levels', 'getLevels')

app = web.application(urls, globals())

clusterList = []

def getClusterCount(f):
    count = 0
    with open(f, "r") as fi:
        for line in fi:
            if len(line.split(',')) > 1:
                count +=1 
    return count    

def getAllJSON():
    for f in listdir("./clusters"):
        clusterList.append((float(f), f))
    clusterList.sort(key=lambda x: x[0])
    print clusterList

def getClusterIncrements():
    return json.dumps(clusterList) 

#Get the level that is directly above the provided value
def getNext(level):
    for j in clusterList:
        print j
        if j[0] >= level:
            return j[1]
    return clusterList[len(clusterList) -1][1]

#Get the leve that is directly below
def getPrev(level):
    prev = ""
    for j in clusterList:
        if j[0] >= level:
            return prev
        else:
            prev = j[1]

class getLevels:
    def GET(self):
        return getClusterIncrements()

class getNumberOfClustersAtSize:
    def GET(self, value):
        f = getNext(float(value))
        count = getClusterCount("./clusters/" + f)
        return str(count)
        

class get_json:
    def GET(self, value):
       f = getNext(float(value))
       print f 
       addclusterdata.insert("./clusters/" + f, "./cur-out.clusterList")
       fi = open("./cur-out.clusterList")
       return fi.read()

getAllJSON()

if __name__ == "__main__":
    app.run()
