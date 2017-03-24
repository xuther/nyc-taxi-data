from __future__ import print_function
import sys
import re
from operator import add
from pyspark.sql import SparkSession
import csv


def splitter(words):
	list = words.split(",")
	start = list[6] + "" + list[7] #+ list[7] + list[8]
	end = list[9] + "" + list[10] #+ list[10] + list[11]
	#start-county,start-tract,start-block,end-county,end-tract,end-block 
	return (start+","+end,1)

if __name__ == "__main__":
		if len(sys.argv) != 3:
				print("Not enough args")
				exit(-1)
		spark = SparkSession\
				 .builder\
				 .appName("Builder")\
				 .getOrCreate()

		lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
		counts = lines.map(lambda x: (splitter(x))) \
									.reduceByKey(add)\
									.filter(lambda x: x[1] > 50)\
									.sortBy(lambda a: a[1], ascending=False)
		output = counts.collect()

		# f = open(sys.argv[2], 'w')
		# for line in output:
		#     f.write(line)
		with open(sys.argv[2], 'w+') as csvfile:
			writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for line in output:
				newlist = line[0].split(",")
				writer.writerow(newlist)
spark.stop()
