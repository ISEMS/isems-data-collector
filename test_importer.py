import datetime
from unittest.mock import patch, MagicMock

from importer import Importer
from models import Measurement


def test_parse_line_invalid():
    assert Importer.parse_line("") is None


def test_parse_line_version_1():
    line = "Elektra-Dach;1;1530364575;ATmega8_A_1;711;0;18.614;18.614;14.073;100;100;28;11.67;14.086;7;20;52.507309;13.458635"
    measurement = Importer.parse_line(line)

    # We save here to make sure that sqlalchemy converts the strings to ints/floats
    measurement.save()
    assert isinstance(measurement, Measurement)
    assert measurement.nodeId == "Elektra-Dach"
    assert measurement.isemsRevision == "1"
    assert measurement.timestamp == datetime.datetime(2018, 6, 30, 15, 16, 15)
    assert measurement.timeToShutdown == 711.0
    assert measurement.isPowerSaveMode is False
    assert measurement.openCircuitVoltage == 18.614
    assert measurement.mppVoltage == 18.614
    assert measurement.batteryVoltage == 14.073
    assert measurement.batteryChargeEstimate == 100
    assert measurement.batteryHealthEstimate == 100
    assert measurement.batteryTemperature == 28
    assert measurement.lowVoltageDisconnectVoltage == 11.67
    assert measurement.temperatureCorrectedVoltage == 14.086
    assert measurement.rateBatteryCapacity == 7
    assert measurement.ratedSolarModuleCapacity == 20
    assert measurement.latitude == 52.507309;
    assert measurement.longitude == 13.458635
    assert measurement.status is None


def test_parse_line_version_2():
    line = "Elektra-Dach-Neu;1;1530364575;ATmega8_A_1;711;0;18.614;18.614;14.073;100;100;28;11.67;14.086;7;20;52.507309;13.458635;300"
    measurement = Importer.parse_line(line)

    # We save here to make sure that sqlalchemy converts the strings to ints/floats
    m = measurement.save()
    assert isinstance(measurement, Measurement)
    assert measurement.nodeId == "Elektra-Dach-Neu"
    assert measurement.isemsRevision == "1"
    assert measurement.timestamp == datetime.datetime(2018, 6, 30, 15, 16, 15)
    assert measurement.timeToShutdown == 711.0
    assert measurement.isPowerSaveMode is False
    assert measurement.openCircuitVoltage == 18.614
    assert measurement.mppVoltage == 18.614
    assert measurement.batteryVoltage == 14.073
    assert measurement.batteryChargeEstimate == 100
    assert measurement.batteryHealthEstimate == 100
    assert measurement.batteryTemperature == 28
    assert measurement.lowVoltageDisconnectVoltage == 11.67
    assert measurement.temperatureCorrectedVoltage == 14.086
    assert measurement.rateBatteryCapacity == 7
    assert measurement.ratedSolarModuleCapacity == 20
    assert measurement.latitude == 52.507309;
    assert measurement.longitude == 13.458635
    assert measurement.status == int("300", 16)


@patch("importer.Importer.parse_line")
def test_from_lines(mock_parse_line):
    mock_measurement = Measurement()
    mock_measurement.save = MagicMock(return_value=1)
    mock_parse_line.return_value = mock_measurement

    inserted_count = Importer.from_lines(["line1", "line2"])

    assert inserted_count == 2



