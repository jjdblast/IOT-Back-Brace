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

def create_labeled_point(line_split):
    # leave_out = [0] since it is a label
    clean_line_split = line_split[1:]
    print(clean_line_split)

    # convert label to binary label
    #stooping = 1.0
    #if line_split[0]=='0':
    #    stooping = 0.0
    
    stooping = line_split[0]
    
    return LabeledPoint(stooping, array([float(x) for x in clean_line_split]))

sc = SparkContext()
sqlContext = SQLContext(sc)
connectionProperties = MySQLConnection.getDBConnectionProps('/home/erik/mysql_credentials.txt')
data = sqlContext.read.jdbc("jdbc:mysql://localhost/biosensor", "SensorTrainingReadings", properties=connectionProperties).selectExpr("deviceID","metricTypeID","uomID","positionID","actualPitch", "actualYaw")


print "Train data size is {}".format(data.count())

(trainingDataTable, testDataTable) = data.randomSplit([0.7, 0.3])

trainingDataTable.show()
testDataTable.show()


def featurize(u):
	return LabeledPoint(u.positionID, [u.actualPitch, u.actualYaw])

#SQL results are RDDs so can be used directly in Mllib.
trainingData = trainingDataTable.map(featurize)
testData = testDataTable.map(featurize)

# Train the classifier/Build the model
t0 = time()

#Decision Tree Model
#model = DecisionTree.trainClassifier(
#    trainingData,
#    numClasses=3,
#    categoricalFeaturesInfo={},
#    impurity='gini',
#    maxDepth=5,
#    maxBins=32)

#Random Forest Model
model = RandomForest.trainClassifier(trainingData, numClasses=3, categoricalFeaturesInfo={},
                                     numTrees=3, featureSubsetStrategy="auto",
                                     impurity='gini', maxDepth=4, maxBins=32)

tt = time() - t0

print "Classifier trained in {} seconds".format(round(tt,3))


# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
print('Test Error = ' + str(testErr))
print('Learned classification forest model:')
print(model.toDebugString())
