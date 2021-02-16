import os

from importer import Importer
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self):
        self.client.connect(os.environ.get("MQTT_SERVER"), 1883, 60)
        self.client.loop_forever()

    @staticmethod
    def _on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("/isems/+/csvlog")

    @staticmethod
    def _on_message(client, userdata, msg):
        lines = msg.payload.decode('utf-8').splitlines()
        Importer.from_lines(lines)

