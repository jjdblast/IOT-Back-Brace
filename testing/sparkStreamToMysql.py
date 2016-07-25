import sys
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import Row


"""IMPORTANT
MUST use class paths when using spark-submit
bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ~/spark/sparkStreamToMysql.py localhost:9092 my-topic
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

def writeRecords(time, rdd):
	#try:
	# Convert RDDs of the words DStream to DataFrame and run SQL query
	print("=====PROCESSING==== %s =========" % str(time))
	connectionProperties = getDBConnectionProps()
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		people = sqlContext.jsonRDD(rdd) # Create dataframe from json
		#people.printSchema()
		#print people.take(1)
		peopleFinal = people.select("name","city","userid").where(people["name"] == "erik") #Get in the correct order before inserting
		peopleFinal.write.jdbc("jdbc:mysql://localhost/gymandtrail", "sparkTest", properties=connectionProperties)
	#except:
	#	pass
		
if __name__ == "__main__":
	sc = SparkContext(appName="StreamKafkaToSparkToMysql")
	ssc = StreamingContext(sc, 2) # 2 second batches
	
	brokers, topic = sys.argv[1:]

	stream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})

	lines = stream.map(lambda x: x[1])

	lines.foreachRDD(writeRecords)

	ssc.start()
	ssc.awaitTermination()
 

