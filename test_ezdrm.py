# test_ezdrm.py
from ezdrm import EZDrm
import requests_mock
import xmltodict


def test_init():
    d = EZDrm("https://test", "kid", "content", "user", "passwd")
    assert d.url == "https://test"
    assert d.kid == "kid"
    assert d.contentId == "content"
    assert d.user == "user"
    assert d.password == "passwd"


def test_fetch():
    with requests_mock.Mocker() as m:
        m.get(
            "https://test?c=content&k=kid&u=user&p=passwd",
            text=open("tests/data.xml").read(),
        )
        d = EZDrm("https://test", "kid", "content", "user", "passwd")
        d.fetch()
        expected = xmltodict.parse(open("tests/data.xml").read())
        assert d.content_dict == expected


def test_parse():
    d = EZDrm("https://test", "kid", "content", "user", "passwd")
    d.content_dict = expected = xmltodict.parse(open("tests/data.xml").read())
    d.parseKeys()

    assert d.version == "2.3"
    assert d.contentId == "Mp4box-test01"
    assert d.explicitIV == "B44F9E302FB649B4990F01F3FC4BFE2D"
    assert d.secretKey == "7103438F487FB7AB0BFAF18FF19677F8"
    assert d.psshList == [
        "AAAAP3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAB8SELRPnjAvtkm0mQ8B8/xL/i0aBWV6ZHJtSOPclZsG",
        "AAACuHBzc2gAAAAAmgTweZhAQoarkuZb4IhflQAAApiYAgAAAQABAI4CPABXAFIATQBIAEUAQQBEAEUAUgAgAHgAbQBsAG4AcwA9ACIAaAB0AHQAcAA6AC8ALwBzAGMAaABlAG0AYQBzAC4AbQBpAGMAcgBvAHMAbwBmAHQALgBjAG8AbQAvAEQAUgBNAC8AMgAwADAANwAvADAAMwAvAFAAbABhAHkAUgBlAGEAZAB5AEgAZQBhAGQAZQByACIAIAB2AGUAcgBzAGkAbwBuAD0AIgA0AC4AMAAuADAALgAwACIAPgA8AEQAQQBUAEEAPgA8AFAAUgBPAFQARQBDAFQASQBOAEYATwA+ADwASwBFAFkATABFAE4APgAxADYAPAAvAEsARQBZAEwARQBOAD4APABBAEwARwBJAEQAPgBBAEUAUwBDAFQAUgA8AC8AQQBMAEcASQBEAD4APAAvAFAAUgBPAFQARQBDAFQASQBOAEYATwA+ADwASwBJAEQAPgBNAEoANQBQAHQATABZAHYAdABFAG0AWgBEAHcASAB6AC8ARQB2ACsATABRAD0APQA8AC8ASwBJAEQAPgA8AEMASABFAEMASwBTAFUATQA+AGIAQgBmAEkAZwBnADgAaABaAGMAYwA9ADwALwBDAEgARQBDAEsAUwBVAE0APgA8AEwAQQBfAFUAUgBMAD4AaAB0AHQAcABzADoALwAvAHAAbABhAHkAcgBlAGEAZAB5AC4AZQB6AGQAcgBtAC4AYwBvAG0ALwBjAGUAbgBjAHkALwBwAHIAZQBhAHUAdABoAC4AYQBzAHAAeAA/AHAAWAA9AEUAMAAxADgAMwBGADwALwBMAEEAXwBVAFIATAA+ADwALwBEAEEAVABBAD4APAAvAFcAUgBNAEgARQBBAEQARQBSAD4A",
    ]
