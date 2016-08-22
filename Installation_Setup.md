# IoT Back Brace Installation and Testing:
## I.  Create the database and required tables:
[SQL_Scripts/MySQL_Database_Scripts.sql]
Execute this script using a mysql command prompt or a gui such as phpmyadmin.
```mysql -u yourusername -p yourpassword < MySQL_Database_Scripts.sql

Dummy records have been created for many of the dimension/Lookup tables.  The actual fact tables are blank since they will be populated in subsequent processing.

## II.  Start up the Kafka message server
The following script will start up the Kafka server to listen on the default ports:

[data_collection/KafkaStartupServices.sh]
#!/bin/bash
##### Start up data collection jobs ####
```/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties > /dev/null 2>&1 &
```/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties > /dev/null 2>&1 &

## III.  Start up the job to process sensor readings.

Note that this requires the following packages:
spark-streaming-kafka http://spark.apache.org/docs/latest/streaming-kafka-integration.html
mysql-connector-java https://dev.mysql.com/downloads/connector/j/
[data_collection/ProcessSensorReadings.py]
The following command will create a spark job utilizing the spark-streaming-kafka and mysql-connector-java packages.
```$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ProcessSensorReadings.py

## IV. Start up the REST API that receives the readings from the devices

The following command will start up a Flask/Python web API listening on port 5000:
[web_api/webServiceToKafkaStartupScript.sh]
```#!/bin/bash
```python2 webServiceToKafka.py > /dev/null 2>&1 &

## V. Create mock readings to test the back-end processing

The following command will create 5 test "Training" readings and 5 test "Actual" readings.
```python2 kafkaProducerTest.py



  