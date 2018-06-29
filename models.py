from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nodeId = db.Column(db.String)
    isemsRevision = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    openMPPTFirmwareVersion = db.Column(db.String)
    timeToShutdown = db.Column(db.Float)
    isPowerSaveMode = db.Column(db.Boolean)
    openCircuitVoltage = db.Column(db.Float)
    mppVoltage = db.Column(db.Float)
    batteryVoltage = db.Column(db.Float)
    batteryChargeEstimate = db.Column(db.Float)
    batteryHealthEstimate = db.Column(db.Float)
    batteryTemperature = db.Column(db.Float)
    lowVoltageDisconnectVoltage = db.Column(db.Float)
    temperatureCorrectedVoltage = db.Column(db.Float)
    rateBatteryCapacity = db.Column(db.Float)
    ratedSolarModuleCapacity = db.Column(db.Float)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.Integer)

    __table_args__ = (UniqueConstraint('nodeId',
                                       'timestamp',
                                       name='node_timestamp'),
                      )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except IntegrityError:
            db.session.rollback()
            return 0

    def to_dict(self):
        raw_dict = dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
        raw_dict["status"] = "{0:#05x}".format(raw_dict["status"] or 0)
        return raw_dict
