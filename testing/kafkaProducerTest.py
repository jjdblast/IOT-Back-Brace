#!/usr/bin/env python
import time
from kafka import KafkaProducer
import json

"""
Usage:  bin/spark-submit ~/spark/kafkaProducrerTest.py
"""



def main():
	producer = KafkaProducer(bootstrap_servers='localhost:9092')
	#while True:
	for i in range(5000): #Send 5000 packets
		packet = {'name':'erik', 'city':'Knoxville','userid':i}
		producer.send('my-topic', json.dumps(packet))
		time.sleep(0.05) # At a rate of 20 per second

if __name__ == "__main__":
    main()