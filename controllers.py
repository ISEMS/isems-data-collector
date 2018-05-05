from sqlalchemy import func

from models import Measurement, db


class MeasurementController:
    @staticmethod
    def latest():
        results = db.session.query(Measurement)\
            .group_by(Measurement.nodeId) \
            .having(func.max(Measurement.timestamp)) \
            .all()
        return results

