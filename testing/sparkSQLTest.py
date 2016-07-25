#!/usr/bin/env python
import time
from pyspark import SparkContext
from pyspark.sql import SQLContext
import json

"""
Usage:  bin/spark-submit ~/spark/kafkaProducrerTest.py
"""
sc = SparkContext()
sqlContext = SQLContext(sc)
packet = [{'name':'erik', 'value':1}]

def main():
	jd = sc.parallelize(packet)
	people = sqlContext.jsonRDD(jd)
	people.printSchema()

if __name__ == "__main__":
    main()