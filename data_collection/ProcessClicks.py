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
	~/ProcessClicks.py
"""

def writeClickRecords(time, rdd):
	try:
		connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
		sqlContext = SQLContext(rdd.context)
		if rdd.isEmpty() == False:
			click = sqlContext.jsonRDD(rdd) # Create dataframe from json
			clickFinal = click.select("visitorID","customerID","propertyID","pagePath","referringPath","clickTime") #Get in the correct order before inserting
			clickFinal.write.jdbc("jdbc:mysql://localhost/crm", "VisitorClicks", properties=connectionProperties)
	except:
		pass


if __name__ == "__main__":
	sc = SparkContext(appName="Process Clicks")
	ssc = StreamingContext(sc, 2) # 2 second batches
	
	#Process Clicks
	streamClicks = KafkaUtils.createDirectStream(ssc, ["VisitorClick"], {"metadata.broker.list": "localhost:9092"})
	linesClicks = streamClicks.map(lambda x: x[1])
	linesClicks.foreachRDD(writeClickRecords)

	ssc.start()
	ssc.awaitTermination()
 

