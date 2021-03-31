import datetime
import os

from sqlalchemy import func, desc

from models import Measurement, db


def get_cutoff_days():
    default_days = 30
    try:
        return int(os.environ.get('HIDE_INACTIVE_AFTER_DAYS', default_days))
    except ValueError:
        return default_days


class MeasurementController:
    @staticmethod
    def latest(show_inactive=False):
        query = db.session.query(Measurement) \
            .group_by(Measurement.nodeId) \
            .having(func.max(Measurement.timestamp))
        if not show_inactive:
            min_days = get_cutoff_days()
            min_timestamp = datetime.datetime.now() - datetime.timedelta(days=min_days)
            query = query.having(Measurement.timestamp > min_timestamp)
        results = query.all()
        return results

    @staticmethod
    def latest_for_id(node_id):
        results = db.session.query(Measurement) \
            .filter(Measurement.nodeId == node_id) \
            .order_by(desc(Measurement.timestamp)) \
            .limit(60 * 24) \
            .all()
        return results
