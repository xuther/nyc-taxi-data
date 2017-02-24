import csv
import operator
import sys

if len(sys.argv) != 4:
	print("not enough args")
	print("usage is: python cluster-in-out.py [departure file] [arrival file] [outfile]")
	exit(-1)

departure_file = sys.argv[1]
arrival_file = sys.argv[2]
out_file = sys.argv[3]

cluster_hash = {}
individual_hash = {}
combined = {}
error = {}
used = {}
tolarge = {}

with open(departure_file) as csvfile:
     reader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in reader:	     
	     key = row[0] + "#" + row[1]
	     combined[key] = row[2]

with open(arrival_file) as csvfile2:
	reader = csv.reader(csvfile2, delimiter=',', quotechar='|')
	for row in reader:
		key = row[1] + "#" + row[0]
		if key in combined:
			if row[2] != "squared-difference":
				combined[key] = (combined[key]+ row[2])/2
		else:
			combined[key] = row[2]

sorted_list = sorted(combined.items(), key=operator.itemgetter(1))
for tup in sorted_list:
	tracts = tup[0].split("#")
	if tup[1] != "squared-difference" and float(tup[1]) > 20:
		tolarge[tup[0]] = tup[1]
	elif tracts[0] in used:
		if tracts[1] not in used:
			cluster_hash[used[tracts[0]]].add(tracts[1])
			used[tracts[1]] = used[tracts[0]]
	elif tracts[1] in used:
		if tracts[0] not in used:
			cluster_hash[used[tracts[1]]].add(tracts[0])
			used[tracts[0]] = used[tracts[1]]
	else:
		new_set = set()
		new_set.add(tracts[1])
		cluster_hash[tracts[0]] = new_set
		used[tracts[0]] = tracts[0]
		used[tracts[1]] = tracts[0]

final_list = sorted(cluster_hash.items(), key=operator.itemgetter(1))
with open(out_file, 'w', newline='') as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for tup in final_list:
		line = []
		line.append(tup[0])
		line.append(tup[1])
		writer.writerow(line)

for item in tolarge.items():
	print(item)
