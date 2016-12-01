tracts = []

for i in blocks.records():
    if (i[2] not in tracts):
        print i[2]
        tracts.append(i[2])

print len(tracts)
