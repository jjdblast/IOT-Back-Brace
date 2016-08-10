import json
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import explode
from pyspark.ml.feature import VectorAssembler
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.sql.functions import udf
from pyspark.sql.types import DecimalType

#custom modules
import MySQLConnection

"""
IMPORTANT:  MUST use class paths when using spark-submit
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ProcessSensorReadings.py
"""

#loadedModel = RandomForestModel.load(sc, "../machine_learning/models/IoTBackBraceRandomForest.model")


def writeLumbarReadings(time, rdd):
	#try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
	connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
	sqlContext = SQLContext(rdd.context)
	if rdd.isEmpty() == False:
		lumbarReadings = sqlContext.jsonRDD(rdd)
		lumbarReadingsIntermediate = lumbarReadings.selectExpr("deviceID","readingTime","metricTypeID","uomID","actual.y AS actualYaw","actual.p AS actualPitch","actual.r AS actualRoll","setPoints.y AS setPointYaw","setPoints.p AS setPointPitch","setPoints.r AS setPointRoll", "prevAvg.y AS prevAvgYaw","prevAvg.p AS prevAvgPitch","prevAvg.r AS prevAvgRoll")
		assembler = VectorAssembler(
					inputCols=["actualYaw", "actualPitch", "actualRoll"],
					outputCol="features")
		lumbarReadingsIntermediate = assembler.transform(lumbarReadingsIntermediate)

		
		predictions = loadedModel.predict(lumbarReadingsIntermediate.map(lambda x: x.features))
		prediction= predictions.collect()
		print(prediction)
		#print(predictions)
		#labelsAndPredictions = lumbarReadingsIntermediate.map(lambda x: x["uomID,deviceID"]).zip(predictions).toDF()
		#labelsAndPredictions = lumbarReadingsIntermediate.map(lambda x: x).zip(predictions).toDF()
		labelsAndPredictions = lumbarReadingsIntermediate.map(lambda x: (x.deviceID,x.actualPitch)).zip(predictions).collect()#.toDF()
		print(labelsAndPredictions)
		#labelsAndPredictions.show()
		#labelsAndPredictions.show()
		#loadedModel = RandomForestModel.load(sc, "../machine_learning/models/IoTBackBraceRandomForest.model")

		#lumbarReadingFinal.write.jdbc("jdbc:mysql://localhost/biosensor", "SensorReadings", properties=connectionProperties)
	#except:
	#	pass
	
def writeLumbarTrainingReadings(time, rddTraining):
	#try:
		# Convert RDDs of the words DStream to DataFrame and run SQL query
	connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
	sqlContext = SQLContext(rddTraining.context)
	if rddTraining.isEmpty() == False:
		lumbarTrainingReading = sqlContext.jsonRDD(rddTraining)
		lumbarTrainingReadingFinal = lumbarTrainingReading.selectExpr("deviceID","readingTime","metricTypeID","uomID","positionID","actual.y AS actualYaw","actual.p AS actualPitch","actual.r AS actualRoll","setPoints.y AS setPointYaw","setPoints.p AS setPointPitch","setPoints.r AS setPointRoll", "prevAvg.y AS prevAvgYaw","prevAvg.p AS prevAvgPitch","prevAvg.r AS prevAvgRoll")
		lumbarTrainingReadingFinal.write.jdbc("jdbc:mysql://localhost/biosensor", "SensorTrainingReadings", properties=connectionProperties)
	#except:
	#	pass
		
if __name__ == "__main__":
	sc = SparkContext(appName="Process Lumbar Sensor Readings")
	ssc = StreamingContext(sc, 2) # 2 second batches
	loadedModel = RandomForestModel.load(sc, "../machine_learning/models/IoTBackBraceRandomForest.model")

	#Process Readings
	streamLumbarSensor = KafkaUtils.createDirectStream(ssc, ["LumbarSensorReadings"], {"metadata.broker.list": "localhost:9092"})
	lineSensorReading = streamLumbarSensor.map(lambda x: x[1])
	lineSensorReading.foreachRDD(writeLumbarReadings)
	
	#Process Training Readings
	streamLumbarSensorTraining = KafkaUtils.createDirectStream(ssc, ["LumbarSensorTrainingReadings"], {"metadata.broker.list": "localhost:9092"})
	lineSensorTrainingReading = streamLumbarSensorTraining.map(lambda x: x[1])
	lineSensorTrainingReading.foreachRDD(writeLumbarTrainingReadings)

	# Run and then wait for termination signal
	ssc.start()
	ssc.awaitTermination()
 

