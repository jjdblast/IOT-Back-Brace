import json
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
#custom modules
import MySQLConnection
import ProcessInteractions
import ProcessVisits
import ProcessClicks
import ProcessTransactions

"""
IMPORTANT:  MUST use class paths when using spark-submit
$SPARK_HOME/bin/spark-submit \ 
	--packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 \
	~/ProcessAll.py
"""

if __name__ == "__main__":
	sc = SparkContext(appName="Kafka To Spark Stream To MYSQL")
	ssc = StreamingContext(sc, 2) # 2 second batches

	#Process Visits
	streamVisit = KafkaUtils.createDirectStream(ssc, ["CustomerVisit"], {"metadata.broker.list": "localhost:9092"})
	linesVisit = streamVisit.map(lambda x: x[1])
	linesVisit.foreachRDD(ProcessVisits.writeVisitRecords)
	
	#Process Clicks
	streamClicks = KafkaUtils.createDirectStream(ssc, ["VisitorClick"], {"metadata.broker.list": "localhost:9092"})
	linesClicks = streamClicks.map(lambda x: x[1])
	linesClicks.foreachRDD(ProcessClicks.writeClickRecords)
	
	#Process Transactions
	streamTransaction = KafkaUtils.createDirectStream(ssc, ["CustomerTransaction"], {"metadata.broker.list": "localhost:9092"})
	linesTransaction = streamTransaction.map(lambda x: x[1])
	linesTransaction.foreachRDD(ProcessTransactions.writeTransactionRecords)
	
	#Process Interactions
	streamInteraction = KafkaUtils.createDirectStream(ssc, ["CustomerInteraction"], {"metadata.broker.list": "localhost:9092"})
	linesInteraction = streamInteraction.map(lambda x: x[1])
	linesInteraction.foreachRDD(ProcessInteractions.writeInteractionRecords)

	ssc.start()
	ssc.awaitTermination()
 

