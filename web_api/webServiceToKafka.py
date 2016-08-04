from flask import Flask, Response, request, json, render_template
from kafka import KafkaProducer

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Default end point
@app.route('/', methods = ['GET'])
def api_root():
	data = {
		"title":"IOT Back Brace REST API",
		"sensorReading":{
					"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
					"readingTime":"2016-07-25T15:45:07.12",
					"metricTypeID":6,
					"uomID":4,
					"actual":{"y":18,"p":17.50,"r":120},
					"setPoints":{"y":25,"p":45,"r":100},
					"prevAvg":{"y":15,"p":40,"r":88}
				 },
		"trainingReading":{
					"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
					"readingTime":"2016-07-25T15:45:07.12",
					"metricTypeID":6,
					"uomID":4,
					"currentPostureID":2,
					"actual":{"y":18,"p":17.50,"r":120},
					"setPoints":{"y":25,"p":45,"r":100},
					"prevAvg":{"y":15,"p":40,"r":88}
				 }
	}
	
	try:
		return render_template("index.html", data = data )
	except Exception, e:
		return str(e)

#  End point for posting sensor readings.
@app.route('/LumbarSensorReading',  methods = ['POST'])
def post_readings():
	if request.headers['Content-Type'] == 'application/json':
		producer.send('LumbarSensorReadings', json.dumps(request.json))
		return "JSON Message: " + json.dumps(request.json)
	else:
		return "415 Unsupported Media Type"
		
# End point for training the Machine Learning Model
@app.route('/LumbarSensorTraining',  methods = ['POST'])
def post_trainingData():
	if request.headers['Content-Type'] == 'application/json':
		producer.send('LumbarSensorTraining', json.dumps(request.json))
		return "JSON Message: " + json.dumps(request.json)
	else:
		return "415 Unsupported Media Type"

if __name__ == '__main__':
    app.run(host="0.0.0.0")