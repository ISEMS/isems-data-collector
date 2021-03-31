from flask import request
from flask.json import jsonify

from app import app
from controllers import MeasurementController


@app.route('/measurements/latest')
def latest_measurements():
    show_inactive = request.args.get('all') == 'true'
    data = MeasurementController.latest(show_inactive=show_inactive)
    dictified = [entry.to_dict() for entry in data]
    return jsonify(measurements=dictified)


@app.route('/measurements/<node_id>/latest')
def measurements_for_id(node_id):
    data = MeasurementController.latest_for_id(node_id)
    dictified = [entry.to_dict() for entry in data]
    return jsonify(measurements=dictified)
