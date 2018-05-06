import os

import requests

DEFAULT_IP = "http://10.36.158.33/ISEMS/ffopenmppt.log"


class Downloader:
    @staticmethod
    def get_sources():
        return os.environ.get("ISEMS_ROUTER_IPS", DEFAULT_IP).split(",")

    @classmethod
    def download_all(cls):
        for source in cls.get_sources():
            yield cls.download(source)

    @classmethod
    def download(cls, source):
        response = requests.get(source)
        return response.text.splitlines()
