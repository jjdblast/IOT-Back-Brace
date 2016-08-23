# IOT Back Brace

## Background
This project was developed as part of an entry for the Apache Spark Maker's Build on [DevPost](http://apachespark.devpost.com/).  The goal of this hackathon was to build an application that solves real-world business problems using the Apache Spark ecosystem. 

The [Page for this project on Devpost](http://devpost.com/software/iot-back-brace) contains more information including a video and images.

## What it does
The IoT Back Brace is a device that helps identify - and report - activities that could potentially cause back injuries such as stooping, bending, and twisting.  This is accomplished by continually monitoring the posture of a person... with an embedded microcontroller, gyroscope, and accelerometer.  Although it is impossible to have perfect posture all of the time this device allows you to track of the number of movements that are classified as potentially harmful.
The back brace has an embedded Microcontroller outfitted with an Accelerometer/Gyroscope  that continuously measures the posture of the person wearing it.  Any activities that cause stooping or bending results in a reading being sent to a web API that then logs the reading through some back-end processing using the Apache Spark ecosystem (Spark Streaming, Spark SQL, and Spark Machine Learning).  

## The Brace Device
The device (currently in prototype) can be attached to any existing back brace/belt and is made with the following components:
*  Arduino Nano Microcontroller
*  GY-521 Accelerometer/Gyroscope IMU
*  ESP8266 Serial WiFi Module

## The Back-End
*  Web API:  Python WebPy script
*  Message Handling:  Apache Kafka Message Broker
*  Processing, Classification, and Database actions:  Apache Spark 
*  Database:  MySQL

## Reporting Dasbhoard
*  PHP and MySQL are utilized for the data layer.
*  AngularJS and HighCharts are used for the single-page dashboard.

##The Process
The process of reporting these metrics combines a wide range of open source technologies from the small Arduino microcontroller to Big Data and Machine Learning engines like Apache Spark.

As the posture of the person wearing the brace changes, an event is triggered, and a message containing the device readings is sent to the cloud where it is logged and categorized using a machine learning algorithm, and then finally those measurements are aggregated and surfaced in reporting.

Although this process seems very simple on the surface, in order for it to be successful on an enterprise scale there needs to be some key technologies at play.  Imagine a company with multiple locations - and dozens of braces - all reporting simultaneous events.  The back-end processing for this deployment would require low-latency response time as well as "near-real-time" reporting for management.  This back-end engine would also require easy scaling as they grow or expand the program.
 
So in order to ensure packets are not lost we have employed the use of a Kafka Messaging cluster.  Each message containing the reading values is sent to the Kafka cluster through a REST API.  This message is held in queue until the processing engine is ready to receive it.  The processing engine in this case is provided by Apache Spark Streaming.  With Spark Streaming, messages are opened and processed in a near continuous manner.  The great thing about Spark is the processing is distributed amongst multiple nodes so if more speed is required the environment can easily be scaled to fit the requirements. 

##Key Files in the Process (All can be found on GitHub)
Directory| File Name| Description
-------- | ----------| -------------
data_collection | [ProcessSensorReadings.py](https://github.com/kringen/IOT-Back-Brace/blob/master/data_collection/ProcessSensorReadings.py) | Creates a Spark Streaming job that reads messages from Kafka, then either treats as training data or actual data.  Then writes the data to MySQL database.
web_api    | [WebServiceToKafka.py](https://github.com/kringen/IOT-Back-Brace/blob/master/web_api/webServiceToKafka.py)  | REST service that listens for POST requests and creates a Kafka message.
Testing     | [KafkaProducerTest.py](https://github.com/kringen/IOT-Back-Brace/blob/master/testing/kafkaProducerTest.py) | Creates random readings and sends in JSON format to Kafka.  Use this to test the data collection process
>Note:  Look for the corresponding Jupyter Notebooks for these files for better explanation and a walk-through of the logic employed in this project.

## What's next for IOT Back Brace
This project is still in its infancy and it is needing some good code review/suggestions for improvement.

