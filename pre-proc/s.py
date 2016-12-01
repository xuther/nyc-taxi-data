tracts = []

for i in blocks.records():
    if (i[2] not in tracts):
        print i[2]
        tracts.append(i[2])

print len(tracts)


countiesInTract = []

for tractIndex in countiesToTracts['061']:
    print str(tractIndex) + " -> " + tracts.record(tractIndex)[2]
    if(tracts.record(tractIndex)[2] == '003001'):
        print "FOUND!!!!!!!!!!!" 
    countiesInTract.append(tracts.record(tractIndex)[2])


for i in range(len(blocks.shapeRecords())): 
    if(blocks.record(i)[3] == '1001'):
        print i
