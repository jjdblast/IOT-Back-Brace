import pyspark
from pyspark import SparkContext
import urllib
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.sql import SQLContext
from time import time
import MySQLConnection

"""
USAGE: $SPARK_HOME/bin/spark-submit --packages mysql:mysql-connector-java:5.1.28 IoTBackBraceMachineLearning.py
"""

sc = SparkContext()
sqlContext = SQLContext(sc)
#  Get username and password from file in this format: {"user":"yourusername","password":"yourpassword"}
connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')

# Get training data from the database
data = sqlContext.read.jdbc("jdbc:mysql://localhost/biosensor", "SensorTrainingReadings", properties=connectionProperties).selectExpr("deviceID","metricTypeID","uomID","positionID","actualPitch", "actualYaw")
print "Train data size is {}".format(data.count())

# Split data into training and test dataasets
(trainingDataTable, testDataTable) = data.randomSplit([0.7, 0.3])

# The model requires labeldPoints which is a row with label and a vector of features.
def featurize(t):
	return LabeledPoint(t.positionID, [t.actualPitch, t.actualYaw])

trainingData = trainingDataTable.map(featurize)
testData = testDataTable.map(featurize)

# Train the classifier/Build the model
startTime = time()

#Random Forest Model
model = RandomForest.trainClassifier(
									trainingData, 
									numClasses=3, 
									categoricalFeaturesInfo={},
                                    numTrees=6, 
									featureSubsetStrategy="auto",
                                    impurity='gini', 
									maxDepth=4, 
									maxBins=32
									)

elapsedTime = time() - startTime

print "Classifier trained in {} seconds".format(round(elapsedTime,3))
# Save the madel for use in evaluating readings
model.save(sc,"models/IoTBackBraceRandomForest.model")

# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
print('Test Error = ' + str(testErr))
print('Learned classification forest model:')
print(model.toDebugString())

loadedModel = RandomForestModel.load(sc, "models/IoTBackBraceRandomForest.model")

for i in range(-50,10):
    prediction = loadedModel.predict([i])
    positions = {0 : "upright",
           1 : "back bent",
           2 : "stooped"
    }
    print str(i) + " => " + str(positions[prediction])
