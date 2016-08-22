# IoT Back Brace Installation and Testing:
## I.  Create the database and required tables:
[SQL_Scripts/MySQL_Database_Scripts.sql]

Execute the following script using a mysql command prompt or a gui such as phpmyadmin.
``` 
mysql -u yourusername -p yourpassword < MySQL_Database_Scripts.sql
```
Dummy records have been created for many of the dimension/Lookup tables.  The actual fact tables are blank since they will be populated in subsequent processing.

## II.  Start up the Kafka message server
[data_collection/KafkaStartupServices.sh]

The following script will start up the Kafka server to listen on the default ports:

```
#!/bin/bash
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties > /dev/null 2>&1 &
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties > /dev/null 2>&1 &
```

## III.  Start up the job to process sensor readings.
[data_collection/ProcessSensorReadings.py]

Note that this requires the following packages:
* [spark-streaming-kafka](http://spark.apache.org/docs/latest/streaming-kafka-integration.html)
* [mysql-connector-java](https://dev.mysql.com/downloads/connector/j/)

The following command will create a spark job utilizing the spark-streaming-kafka and mysql-connector-java packages.

```
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.2,mysql:mysql-connector-java:5.1.28 ProcessSensorReadings.py
```

## IV. Start up the REST API that receives the readings from the devices
[web_api/webServiceToKafkaStartupScript.sh]

The following command will start up a Flask/Python web API listening on port 5000:

```
#!/bin/bash
python2 webServiceToKafka.py > /dev/null 2>&1 &
```

## V. Create mock readings to test the back-end processing

The following command will create 5 test "Training" readings and 5 test "Actual" readings.
```
python2 kafkaProducerTest.py
```
## VI.  Dashboard and Reporting
[reporting/index.html and reporting/api/index.php]

An example dashboard has been created that demonstrates the general concept of how readings from the devices can be displayed.  The api requries PHP and MySQL. The remaining files are using only HTML, JavaScript, and AngularJS.

  