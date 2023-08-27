# test_ezdrm.py
from ezdrm import EZDrm
import requests_mock
import xmltodict


def test_init():
    assert EZDrm("test").url == "test"


def test_fetch():
    with requests_mock.Mocker() as m:
        m.get("http://test?", text=open("tests/data.xml").read())
        d = EZDrm("http://test?")
        d.fetch()
        expected = xmltodict.parse(open("tests/data.xml").read())
        assert d.content_dict == expected
