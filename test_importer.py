import datetime
from unittest.mock import patch, MagicMock

import pendulum
from sqlalchemy.exc import IntegrityError

from importer import Importer
from models import Measurement, db


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


@patch("importer.Importer._bulk_import_new_measurements", side_effect=IntegrityError("Mock", "Mock", "Mock"))
@patch("importer.Importer._one_by_one_import_all")
def test_from_lines(mock_one_by_one_import, mock_bulk_import):
    Importer.from_lines([])
    assert mock_one_by_one_import.called
    assert mock_bulk_import.called


def test__one_by_one_import_all():
    mock_measurement = Measurement()
    mock_measurement.save = MagicMock(return_value=1)
    measurements = [mock_measurement, mock_measurement]

    inserted_count = Importer._one_by_one_import_all(measurements)

    assert inserted_count == 2


def test_bulk_import_new_measurements():
    measurement = Measurement(timestamp=datetime.datetime(2017, 1, 1, 1, tzinfo=pendulum.timezone("Europe/Berlin")), nodeId='test_node')
    measurement.save()

    old_count = db.session.query(Measurement).count()
    import_measurements = [Measurement(timestamp=datetime.datetime(2017, 1, 1, 0, tzinfo=pendulum.timezone("Europe/Berlin")), nodeId='test_node'),
                           Measurement(timestamp=datetime.datetime(2017, 1, 1, 2, tzinfo=pendulum.timezone("Europe/Berlin")), nodeId='test_node')]
    insert_count = Importer._bulk_import_new_measurements(import_measurements)

    assert insert_count == 1
    assert db.session.query(Measurement).count() == old_count + 1
