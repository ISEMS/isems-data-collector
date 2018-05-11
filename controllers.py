from sqlalchemy import func, desc

from models import Measurement, db


class MeasurementController:
    @staticmethod
    def latest():
        results = db.session.query(Measurement)\
            .group_by(Measurement.nodeId) \
            .having(func.max(Measurement.timestamp)) \
            .all()
        return results

    @staticmethod
    def latest_for_id(node_id):
        results = db.session.query(Measurement) \
            .filter(Measurement.nodeId == node_id)  \
            .order_by(desc(Measurement.timestamp)) \
            .limit(60*24) \
            .all()
        return results
