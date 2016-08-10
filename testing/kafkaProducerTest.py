#!/usr/bin/env python
import time
from kafka import KafkaProducer
import json
import random
import csv

"""
Usage:  bin/spark-submit ~/spark/kafkaProducrerTest.py
"""
producer = KafkaProducer(bootstrap_servers='localhost:9092')
pitch = 0
position = 0

def getRandomPitch(min,max):
    pitch = random.uniform(min,max)
    if pitch < -25:
        position=2
    elif pitch < -15:
        position=1
    else:
        position=0
    return pitch, position


def sendSensorReadings(iterations):
	packet = {
				"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
				"readingTime":"2016-07-25T15:45:07.12",
				"metricTypeID":6,
				"uomID":4,
				"actual":{"y":-30,"p":-45,"r":120},
				"setPoints":{"y":25,"p":45,"r":100},
				"prevAvg":{"y":15,"p":40,"r":88}
			 }

	for i in range(iterations): 
		producer.send('LumbarSensorReadings', json.dumps(packet))

def sendSensorTrainingReadings(iterations):
	
	for i in range(iterations): 
		pitch, position = getRandomPitch(-50,25)
		if pitch <= -15:
			if pitch <= -25:
				position = 2.0
			elif pitch > -25:
				if pitch <= -15:
					position = 1.0
		packet = {
					"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
					"positionID":position,
					"readingTime":"2016-07-25T15:45:07.12",
					"metricTypeID":6,
					"uomID":4,
					"actual":{"y":18,"p":pitch,"r":120},
					"setPoints":{"y":25,"p":45,"r":100},
					"prevAvg":{"y":15,"p":40,"r":88}
				 }
		producer.send('LumbarSensorTrainingReadings', json.dumps(packet))
		
def main():
	sendSensorReadings(5)
	sendSensorTrainingReadings(5)


if __name__ == "__main__":
    main()
