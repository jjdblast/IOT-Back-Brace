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
	~/ProcessInteractions.py
"""

def writeInteractionRecords(time, rdd):
	try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
		connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
		sqlContext = SQLContext(rdd.context)
		if rdd.isEmpty() == False:
			interaction = sqlContext.jsonRDD(rdd) # Create dataframe from json
			interactionFinal = interaction.select("customerID","offerID","interactionTypeID","interactionTime") #Get in the correct order before inserting
			interactionFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerInteractions", properties=connectionProperties)
	except:
		pass

if __name__ == "__main__":
	sc = SparkContext(appName="Process Interactions")
	ssc = StreamingContext(sc, 2) # 2 second batches
	
	#Process Interactions
	streamInteraction = KafkaUtils.createDirectStream(ssc, ["CustomerInteraction"], {"metadata.broker.list": "localhost:9092"})
	linesInteraction = streamInteraction.map(lambda x: x[1])
	linesInteraction.foreachRDD(writeInteractionRecords)

	ssc.start()
	ssc.awaitTermination()
 

