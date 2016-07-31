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
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ~/ProcessSensorReadings.py
"""

def writeLumbarReadings(time, rdd):
	#try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
	connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		lumbarReading = sqlContext.jsonRDD(rdd)
		lumbarReadingFinal = lumbarReading.selectExpr("deviceID","readingTime","metricTypeID","uomID","actual.y AS actualYaw","actual.p AS actualPitch","actual.r AS actualRoll","setPoints.y AS setPointYaw","setPoints.p AS setPointPitch","setPoints.r AS setPointRoll", "prevAvg.y AS prevAvgYaw","prevAvg.p AS prevAvgPitch","prevAvg.r AS prevAvgRoll")
		lumbarReadingFinal.write.jdbc("jdbc:mysql://localhost/biosensor", "SensorReadings", properties=connectionProperties)
	#except:
	#	pass
		
if __name__ == "__main__":
	sc = SparkContext(appName="Process Lumbar Sensor Readings")
	ssc = StreamingContext(sc, 2) # 2 second batches

	#Process Transactions
	streamLumbarSensor = KafkaUtils.createDirectStream(ssc, ["LumbarSensorReadings"], {"metadata.broker.list": "localhost:9092"})
	lineSensorReading = streamLumbarSensor.map(lambda x: x[1])
	lineSensorReading.foreachRDD(writeLumbarReadings)

	ssc.start()
	ssc.awaitTermination()
 

