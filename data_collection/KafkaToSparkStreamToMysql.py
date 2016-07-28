import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark.sql.functions import explode

"""IMPORTANT
MUST use class paths when using spark-submit
/usr/local/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ~/Devel/Spark-CRM-App/data_collection/KafkaToSparkStreamToMysql.py
"""


def getDBConnectionProps():
	# Open MYSQL credentials file to get username and password
	with open('/home/erik/mysql_credentials.txt', 'r') as f:
		creds = json.load(f)

	# Establish an object that will hold the MYSQL database connection properties
	connectionProperties = {
	"user":creds["user"],
	"password":creds["password"],
	"driver":"com.mysql.jdbc.Driver",
	"table":"sparkTest",
	"mode":"append"
	}
	
	return connectionProperties

def writeVisitRecords(time, rdd):
	#try:
	# Convert RDDs of the words DStream to DataFrame and run SQL query
	connectionProperties = getDBConnectionProps()
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		visit = sqlContext.jsonRDD(rdd) # Create dataframe from json
		visitFinal = visit.select("customerID","propertyID","visitTime","deviceID","appID") #Get in the correct order before inserting
		visitFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerVisits", properties=connectionProperties)
	#except:
	#	pass

def writeClickRecords(time, rdd):
	connectionProperties = getDBConnectionProps()
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		click = sqlContext.jsonRDD(rdd) # Create dataframe from json
		clickFinal = click.select("visitorID","customerID","propertyID","pagePath","referringPath","clickTime") #Get in the correct order before inserting
		clickFinal.write.jdbc("jdbc:mysql://localhost/crm", "VisitorClicks", properties=connectionProperties)

def writeTransactionRecords(time, rdd):
	connectionProperties = getDBConnectionProps()
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		transaction = sqlContext.jsonRDD(rdd) # Create dataframe from json
		#transaction.printSchema()
		transactionFinal = transaction.select("customerID","propertyID","posID","posTransactionID","deviceID","cartID","appID","transactionType","transactionTime") #Get in the correct order before inserting
		transactionFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerTransactions", properties=connectionProperties)
		#Products are nested in JSON.  Handle them separately
		#products = transaction.select("customerID","property
		#productLines = transaction.map(lambda x: x[1])
		products = transaction.select("propertyID","posID","posTransactionID","transactionTime",explode("products").alias("product"))
		productsFinal = products.select("propertyID","posID","posTransactionID","product.productID","product.price","product.qty","product.promoCode","product.discountAmount","transactionTime")
		productsFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerTransactionProducts", properties=connectionProperties)

def writeInteractionRecords(time, rdd):
	connectionProperties = getDBConnectionProps()
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		interaction = sqlContext.jsonRDD(rdd) # Create dataframe from json
		interactionFinal = interaction.select("customerID","offerID","interactionTypeID","interactionTime") #Get in the correct order before inserting
		interactionFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerInteractions", properties=connectionProperties)


if __name__ == "__main__":
	sc = SparkContext(appName="Kafka To Spark Stream To MYSQL")
	ssc = StreamingContext(sc, 2) # 2 second batches

	#Process Visits
	streamVisit = KafkaUtils.createDirectStream(ssc, ["CustomerVisit"], {"metadata.broker.list": "localhost:9092"})
	linesVisit = streamVisit.map(lambda x: x[1])
	linesVisit.foreachRDD(writeVisitRecords)
	
	#Process Clicks
	streamClicks = KafkaUtils.createDirectStream(ssc, ["VisitorClick"], {"metadata.broker.list": "localhost:9092"})
	linesClicks = streamClicks.map(lambda x: x[1])
	linesClicks.foreachRDD(writeClickRecords)
	
	#Process Transactions
	streamTransaction = KafkaUtils.createDirectStream(ssc, ["CustomerTransaction"], {"metadata.broker.list": "localhost:9092"})
	linesTransaction = streamTransaction.map(lambda x: x[1])
	linesTransaction.foreachRDD(writeTransactionRecords)
	
	#Process Interactions
	streamInteraction = KafkaUtils.createDirectStream(ssc, ["CustomerInteraction"], {"metadata.broker.list": "localhost:9092"})
	linesInteraction = streamInteraction.map(lambda x: x[1])
	linesInteraction.foreachRDD(writeInteractionRecords)

	ssc.start()
	ssc.awaitTermination()
 

