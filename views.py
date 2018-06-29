from flask.json import jsonify

from app import app
from controllers import MeasurementController


@app.route('/measurements/latest')
def latest_measurements():
    data = MeasurementController.latest()
    dictified = [entry.to_dict() for entry in data]
    return jsonify(measurements=dictified)


@app.route('/measurements/<node_id>/latest')
def measurements_for_id(node_id):
    data = MeasurementController.latest_for_id(node_id)
    dictified = [entry.to_dict() for entry in data]
    return jsonify(measurements=dictified)
