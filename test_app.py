from datetime import datetime, timedelta

from models import Measurement

base_measurement = {'batteryChargeEstimate': None,
                    'batteryHealthEstimate': None,
                    'batteryTemperature': None,
                    'batteryVoltage': None,
                    'isPowerSaveMode': None,
                    'isemsRevision': '1',
                    'latitude': None,
                    'longitude': None,
                    'lowVoltageDisconnectVoltage': None,
                    'mppVoltage': None,
                    'nodeId': 'node-1',
                    'openCircuitVoltage': None,
                    'openMPPTFirmwareVersion': None,
                    'rateBatteryCapacity': None,
                    'ratedSolarModuleCapacity': None,
                    'status': '0x000',
                    'temperatureCorrectedVoltage': None,
                    'timeToShutdown': None}


def test_empty_db(client):
    rv = client.get('/measurements/latest')
    assert rv.json == {"measurements": []}


def test_some_data(client):
    # Arrange
    timestamp = datetime.now()
    Measurement(nodeId="node-1", isemsRevision="1", timestamp=timestamp).save()
    Measurement(nodeId="node-2", isemsRevision="1", timestamp=timestamp).save()

    # Act
    rv = client.get('/measurements/latest')

    # Assert
    assert rv.json == {'measurements': [{**base_measurement,
                                         'id': 1,
                                         'nodeId': 'node-1',
                                         'timestamp': timestamp.isoformat()},
                                        {**base_measurement,
                                         'id': 2,
                                         'nodeId': 'node-2',
                                         'timestamp': timestamp.isoformat()}]}


def test_filters_old_measurements(client):
    # Arrange
    timestamp = datetime.now()
    Measurement(nodeId="node-1", isemsRevision="1", timestamp=timestamp - timedelta(days=45)).save()
    Measurement(nodeId="node-2", isemsRevision="1", timestamp=timestamp).save()

    # Act
    rv = client.get('/measurements/latest')

    # Assert
    assert rv.json == {'measurements': [{**base_measurement,
                                         'id': 2,
                                         'nodeId': 'node-2',
                                         'timestamp': timestamp.isoformat()}]}


def test_filters_old_measurements_can_be_disabled(client):
    # Arrange
    timestamp = datetime.now()
    old_timestamp = timestamp - timedelta(days=45)
    Measurement(nodeId="node-1", isemsRevision="1", timestamp=old_timestamp).save()
    Measurement(nodeId="node-2", isemsRevision="1", timestamp=timestamp).save()

    # Act
    rv = client.get('/measurements/latest?all=true')

    # Assert
    assert rv.json == {'measurements': [{**base_measurement,
                                         'id': 1,
                                         'nodeId': 'node-1',
                                         'timestamp': old_timestamp.isoformat()},
                                        {**base_measurement,
                                         'id': 2,
                                         'nodeId': 'node-2',
                                         'timestamp': timestamp.isoformat()}]}
