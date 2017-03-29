import numpy as np
import json
import csv
from pyspark import SparkConf, SparkContext

conf = (SparkConf()
        .setMaster("local[*]")
        .setAppName("My app")
        .set("spark.executor.memory", "8g")
        .set("spark.executor.cores", "8"))

sc = SparkContext(conf = conf)

InDirDepart = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/departures"
InDirArrive = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/arrivals"
OutDir = "/home/sir/Neighborhoods/Data/Test/2015-aggregated/high-dimensional-clustering/"

