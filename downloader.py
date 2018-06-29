import os

import requests

DEFAULT_IP = "10.36.158.33"


class Downloader:
    @staticmethod
    def get_sources():
        ips = os.environ.get("ISEMS_ROUTER_IPS", DEFAULT_IP).split(",")
        return ["http://{}/ISEMS/ffopenmppt.log".format(ip) for ip in ips]

    @classmethod
    def download_all(cls):
        for source in cls.get_sources():
            yield cls.download(source)

    @classmethod
    def download(cls, source):
        response = requests.get(source)
        return response.text.splitlines()
