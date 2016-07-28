#!/usr/bin/env python
import time
from kafka import KafkaProducer
import json

"""
Usage:  bin/spark-submit ~/spark/kafkaProducrerTest.py
"""
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def sendClicks(iterations):
	packet = {
				"visitorID":"a8d8c66535e67f65c5a43d",
				"customerID":1234,
				"propertyID":3,
				"pagePath":"/products/category/1234",
				"referringPath":"/products/category/15",
				"clickTime":"2016-07-25T15:45:07.12"
			 }
	for i in range(iterations): 
		producer.send('VisitorClick', json.dumps(packet))

def sendVisits(iterations):
	packet = {
				"customerID":1234,
				"propertyID":3,
				"visitTime":"2016-07-25T15:45:07.12",
				"deviceID":"456e56c645b6e64ff465a516b6c",
				"appID":10
			 }
	for i in range(iterations): 
		producer.send('CustomerVisit', json.dumps(packet))

def sendTransactions(iterations):
	packet = {
				"customerID":1234,
				"propertyID":3,
				"transactionTime":"2016-07-25T15:45:07.12",
				"deviceID":"456e56c645b6e64ff465a516b6c",
				"posID":8,
				"posTransactionID":1528,
				"cartID":"f5d46546e884a681c516b456a",
				"appID":10,
				"transactionType":"sale",
				"products":[
							{"productID":14538,"price":17.50,"qty":1,"promoCode":"asdf","discountAmount":0},
							{"productID":17638,"price":7.25,"qty":1,"promoCode":"asdf","discountAmount":0},
							{"productID":14823,"price":13.10,"qty":1,"promoCode":"asdf","discountAmount":0},
							{"productID":11537,"price":8.99,"qty":1,"promoCode":"asdf","discountAmount":0}
				]
			 }
	for i in range(iterations): 
		producer.send('CustomerTransaction', json.dumps(packet))
		
def sendInteractions(iterations):
	packet = {
				"customerID":1234,
				"offerID":157,
				"interactionTypeID":3,
				"interactionTime":"2016-07-25T15:45:07.12"
			 }
	for i in range(iterations):
		producer.send('CustomerInteraction', json.dumps(packet))
		
def main():
	sendClicks(5)
	sendVisits(5)
	sendTransactions(5)
	sendInteractions(5) 

if __name__ == "__main__":
    main()
