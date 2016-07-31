#!/usr/bin/env python
import time
from kafka import KafkaProducer
import json

"""
Usage:  bin/spark-submit ~/spark/kafkaProducrerTest.py
"""
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def sendSensorReadings(iterations):
	packet = {
				"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
				"readingTime":"2016-07-25T15:45:07.12",
				"metricTypeID":6,
				"uomID":4,
				"actual":{"y":18,"p":17.50,"r":120},
				"setPoints":{"y":25,"p":45,"r":100},
				"prevAvg":{"y":15,"p":40,"r":88}
			 }

	for i in range(iterations): 
		producer.send('LumbarSensorReadings', json.dumps(packet))

def main():
	sendSensorReadings(5)


if __name__ == "__main__":
    main()
