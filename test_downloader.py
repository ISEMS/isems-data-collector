from collections import namedtuple
from unittest.mock import patch, call

from downloader import Downloader


@patch("os.environ.get", return_value="1.1.1.1,1.2.2.2")
def test_get_sources_with_env(*args):
    expected = [
        "http://1.1.1.1/ISEMS/ffopenmppt.log",
        "http://1.2.2.2/ISEMS/ffopenmppt.log"
    ]
    assert Downloader.get_sources() == expected


@patch("downloader.Downloader.download")
@patch("downloader.Downloader.get_sources", return_value=["source1", "source2"])
def test_download_all(mock_get_sources, mock_download):
    for _ in Downloader.download_all():
        pass
    mock_download.assert_has_calls([call("source1"), call("source2")])


@patch("requests.get")
def test_download(mock_get):
    Response = namedtuple("Response", ["text"])
    mock_get.return_value = Response("line1\nline2")

    assert Downloader.download("source_url") == ["line1", "line2"]
    mock_get.assert_called_once_with("source_url")


