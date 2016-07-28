import json
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode
#custom modules
import MySQLConnection

"""
IMPORTANT:  MUST use class paths when using spark-submit
$SPARK_HOME/bin/spark-submit \ 
	--packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 \
	~/ProcessTransactions.py
"""

def writeTransactionRecords(time, rdd):
	try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
		connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
		sqlContext = SQLContext(rdd.context)
		if rdd.isEmpty() == False:
			transaction = sqlContext.jsonRDD(rdd) # Create dataframe from json
			transactionFinal = transaction.select("customerID","propertyID","posID","posTransactionID","deviceID","cartID","appID","transactionType","transactionTime") #Get in the correct order before inserting
			transactionFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerTransactions", properties=connectionProperties)
			#Products are nested in JSON.  Handle them separately
			products = transaction.select("propertyID","posID","posTransactionID","transactionTime",explode("products").alias("product"))
			productsFinal = products.select("propertyID","posID","posTransactionID","product.productID","product.price","product.qty","product.promoCode","product.discountAmount","transactionTime")
			productsFinal.write.jdbc("jdbc:mysql://localhost/crm", "CustomerTransactionProducts", properties=connectionProperties)
	except:
		pass
		
if __name__ == "__main__":
	sc = SparkContext(appName="Process Transactions")
	ssc = StreamingContext(sc, 2) # 2 second batches

	#Process Transactions
	streamTransaction = KafkaUtils.createDirectStream(ssc, ["CustomerTransaction"], {"metadata.broker.list": "localhost:9092"})
	linesTransaction = streamTransaction.map(lambda x: x[1])
	linesTransaction.foreachRDD(writeTransactionRecords)

	ssc.start()
	ssc.awaitTermination()
 

