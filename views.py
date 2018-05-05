from flask.json import jsonify

from app import app
from controllers import MeasurementController


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/measurements/latest')
def measurement():
    data = MeasurementController.latest()
    dictified = [entry.to_dict() for entry in data]
    return jsonify(measurements=dictified)
