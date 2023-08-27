import requests
from typing import Self
import xmltodict


class EZDrm:
    def __init__(self, url: str, kid: str, contentId: str, user: str, password: str):
        self.url = url
        self.kid = kid
        self.contentId = contentId
        self.user = user
        self.password = password

    def fetch(self) -> Self:
        r = requests.get(self.url, stream=True)
        print(r)
        # if r.status_code != 200:
        #     print("Error while getting EZDrm keys")
        #     return None
        # decompress if we are receiving GZip
        r.raw.decode_content = True
        self.content_dict = xmltodict.parse(r.raw)
        return self

    def parseKeys(self) -> Self:
        root = self.content_dict["cpix:CPIX"]
        self.contentId = root["@contentId"]
        self.version = root["@version"]
        contentKey = root["cpix:ContentKeyList"]["cpix:ContentKey"]
        self.explicitIV = contentKey["@explicitIV"]
        return self
