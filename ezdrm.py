import requests
from typing import Self
import xmltodict
import urllib.parse
import base64


class EZDrm:
    def __init__(self, url: str, kid: str, contentId: str, user: str, password: str):
        self.url = url
        self.kid = kid
        self.contentId = contentId
        self.user = user
        self.password = password

    def fetch(self) -> Self:
        params = {
            "c": self.contentId,
            "u": self.user,
            "p": self.password,
            "k": self.kid,
        }
        r = requests.get(
            "{url}?{params}".format(
                url=self.url, params=urllib.parse.urlencode(params)
            ),
            stream=True,
        )
        # decompress if we are receiving GZip
        r.raw.decode_content = True
        self.content_dict = xmltodict.parse(r.raw)
        return self

    def parseKeys(self) -> Self:
        root = self.content_dict["cpix:CPIX"]
        self.contentId = root["@contentId"]
        self.version = root["@version"]
        contentKey = root["cpix:ContentKeyList"]["cpix:ContentKey"]
        self.explicitIV = (
            base64.b64decode(contentKey["@explicitIV"].encode("ascii")).hex().upper()
        )
        secret = contentKey["cpix:Data"]["pskc:Secret"]["pskc:PlainValue"]
        self.secretKey = base64.b64decode(secret.encode("ascii")).hex().upper()
        self.encryption = contentKey["@commonEncryptionScheme"]
        self.psshList = [
            x["cpix:PSSH"]
            for x in filter(
                lambda attr: True if "cpix:PSSH" in attr else False,
                root["cpix:DRMSystemList"]["cpix:DRMSystem"],
            )
        ]
        return self

    # def fragmentMP4(f: str):
