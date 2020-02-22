from datetime import datetime
import pendulum
from sqlalchemy import func, desc
from sqlalchemy.exc import IntegrityError

from models import Measurement, db


class Importer:
    @classmethod
    def from_lines(cls, lines):
        measurements = [cls.parse_line(line) for line in lines]

        try:
            insert_count = cls._bulk_import_new_measurements(measurements)
        except IntegrityError:
            insert_count = cls._one_by_one_import_all(measurements)
        return insert_count

    @classmethod
    def _bulk_import_new_measurements(cls, measurements):
        max_timestamp = Measurement.get_latest_timestamp(measurements[0].nodeId)
        if max_timestamp:
            max_timestamp = max_timestamp.replace(tzinfo=pendulum.timezone("Europe/Berlin"))
            new_measurements = [m for m in measurements if m.timestamp > max_timestamp]
        else:
            new_measurements = measurements
        db.session.bulk_save_objects(new_measurements)
        db.session.commit()
        return len(new_measurements)

    @classmethod
    def _one_by_one_import_all(cls, measurements):
        counter = 0
        for measurement in [m for m in measurements if m is not None]:
            counter += measurement.save()
        return counter

    @classmethod
    def parse_line(cls, line):
        parts = line.split(";")
        VALID_FIELD_COUNTS = [
            18,  # without status
            19   # with new status field
        ]
        field_count = len(parts)

        try:
            assert (field_count in VALID_FIELD_COUNTS)
        except AssertionError:
            print("Assertion failed for line: {}".format(line))
            return None

        measurement = Measurement(
            nodeId=parts[0],
            isemsRevision=parts[1],
            timestamp=datetime.fromtimestamp(int(parts[2]), tz=pendulum.timezone("Europe/Berlin")),
            openMPPTFirmwareVersion=parts[3],
            timeToShutdown=parts[4],
            isPowerSaveMode=(parts[5] == "1"),
            openCircuitVoltage=parts[6],
            mppVoltage=parts[7],
            batteryVoltage=parts[8],
            batteryChargeEstimate=parts[9],
            batteryHealthEstimate=parts[10],
            batteryTemperature=parts[11],
            lowVoltageDisconnectVoltage=parts[12],
            temperatureCorrectedVoltage=parts[13],
            rateBatteryCapacity=parts[14],
            ratedSolarModuleCapacity=parts[15],
            latitude=float(parts[16]),
            longitude=float(parts[17])
        )
        if field_count == 19:
            measurement.status = int(parts[18], 16)

        return measurement

