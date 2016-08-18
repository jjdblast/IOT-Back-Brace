from flask import Flask, Response, request, json, render_template
from kafka import KafkaProducer
import uuid
import datetime

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Default end point
@app.route('/', methods = ['GET'])
def api_root():
	data = {
		"title":"IOT Back Brace REST API",
		"sensorReading":{
					"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
					"metricTypeID":6,
					"uomID":4,
					"actual":{"y":18,"p":17.50,"r":120},
					"setPoints":{"y":25,"p":45,"r":10}
				 },
		"trainingReading":{
					"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
					"metricTypeID":6,
					"uomID":4,
					"currentPostureID":2,
					"actual":{"y":18,"p":17.50,"r":120},
					"setPoints":{"y":25,"p":45,"r":100}
				 }
	}
	
	try:
		print(request.headers)
		return render_template("index.html", data = data )
	except Exception, e:
		return str(e)

#  End point for posting sensor readings.
@app.route('/LumbarSensorReading',  methods = ['POST'])
def post_readings():
	if request.headers['Content-Type'] == 'application/json':
		
		# Create readingTime
		readingTime = datetime.datetime.now().isoformat()
		
		# Create readingID
		readingID = str(uuid.uuid4())
		
		# Add these to json object
		request.json['readingTime'] = readingTime
		request.json['readingID'] = readingID
		
		# Send to Kafka producer
		producer.send('LumbarSensorReadings', json.dumps(request.json))
		return "JSON Message: " + json.dumps(request.json)
	else:
		return "415 Unsupported Media Type"
		
# End point for training the Machine Learning Model
@app.route('/LumbarSensorTraining',  methods = ['POST'])
def post_trainingData():
	if request.headers['Content-Type'] == 'application/json':
	
		# Create readingTime
		readingTime = datetime.datetime.now().isoformat()
		
		# Create readingID
		readingID = str(uuid.uuid4())
		
		# Add these to json object
		request.json['readingTime'] = readingTime
		request.json['readingID'] = readingID
		
		# Send to Kafka producer
		producer.send('LumbarSensorTraining', json.dumps(request.json))
		print(request.headers)

		return "JSON Message: " + json.dumps(request.json)
	else:
		return "415 Unsupported Media Type"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=1)
