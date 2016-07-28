import json
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
#custom modules
import MySQLConnection

"""
IMPORTANT:  MUST use class paths when using spark-submit
$SPARK_HOME/bin/spark-submit \ 
	--packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 \
	~/ProcessVisits.py
"""

def writeVisitRecords(time, rdd):
	try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
		connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
		sqlContext = SQLContext(rdd.context)
		if rdd.isEmpty() == False:
			visit = sqlContext.jsonRDD(rdd) # Create dataframe from json
			visitFinal = visit.select("customerID","propertyID","visitTime","deviceID","appID") #Get in the correct order before inserting
			visitFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerVisits", properties=connectionProperties)
	except:
		pass

if __name__ == "__main__":
	sc = SparkContext(appName="Process Visits")
	ssc = StreamingContext(sc, 2) # 2 second batches
	
	#Process Visits
	streamVisit = KafkaUtils.createDirectStream(ssc, ["CustomerVisit"], {"metadata.broker.list": "localhost:9092"})
	linesVisit = streamVisit.map(lambda x: x[1])
	linesVisit.foreachRDD(writeVisitRecords)

	ssc.start()
	ssc.awaitTermination()
 

