from datetime import datetime

from models import Measurement


class Importer:
    @classmethod
    def from_lines(cls, lines):
        counter = 0
        for line in lines:
            measurement = cls.parse_line(line)
            if measurement:
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
            timestamp=datetime.fromtimestamp(int(parts[2])),
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

