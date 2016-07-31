from flask import Flask, Response, request, json
from kafka import KafkaProducer

app = Flask(__name__)

producer = KafkaProducer(bootstrap_servers='localhost:9092')

@app.route('/', methods = ['GET'])
def api_root():
	data = {
				"deviceID":"5d681c54e66ff4a5654e55c6d5a5b54",
				"readingTime":"2016-07-25T15:45:07.12",
				"metricTypeID":6,
				"uomID":4,
				"actual":{"y":18,"p":17.50,"r":120},
				"setPoints":{"y":25,"p":45,"r":100},
				"prevAvg":{"y":15,"p":40,"r":88}
			 }
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/lumbarSensorReading',  methods = ['POST'])
def post_transactions():
	if request.headers['Content-Type'] == 'application/json':
		producer.send('LumbarSensorReadings', json.dumps(request.json))
		return "JSON Message: " + json.dumps(request.json)
	else:
		return "415 Unsupported Media Type"

if __name__ == '__main__':
    app.run(host="0.0.0.0")