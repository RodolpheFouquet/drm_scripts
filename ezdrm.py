import requests
from typing import Self
import xmltodict
import urllib.parse
import base64
import jinja2

PLAYREADY_SYSID = "9A04F07998404286AB92E65BE0885F95"
WIDEVINE_SYSID = "EDEF8BA979D64ACEA3C827DCD51D21ED"

#only works for 1 audio 1 video
DRM_TEMPLATE= """<?xml version="1.0" encoding="UTF-8" ?>
<GPACDRM type="CENC AES-CTR">
    
  <!-- Widevine- ->
  <DRMInfo type="pssh" version="0">
		<BS ID128="{{ widevine_id }}"/>
		<BS ID128="0x{{ iv }}"/>
		<BS data64="{{ widevine_pssh }}"/>
	</DRMInfo>

  <!-- Playready -->
  <DRMInfo type="pssh" version="0">
		<BS ID128="{{ playready_id }}"/>
		<BS ID128="0x{{ iv }}"/>
		<BS data64="{{ playready_pssh }}"/>
	</DRMInfo>


  <CrypTrack trackID="1" IsEncrypted="1" first_IV="0x{{ iv }}" saiSavedBox="senc">
    <key KID="0x{{ kid }}" value="0x{{ secret_key}}"/>
  </CrypTrack>

    <CrypTrack trackID="2" IsEncrypted="1" first_IV="0x{{ iv }}" saiSavedBox="senc">
    <key KID="0x{{ kid }}" value="0x{{ secret_key}}"/>
  </CrypTrack>
</GPACDRM>
"""

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
        url = "{url}?{params}".format(
                url=self.url, params=urllib.parse.urlencode(params)
            )
            
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
        self.psshList = dict(
            [
                (
                    x["@systemId"].upper().replace("-", ""),
                    x["cpix:PSSH"]
                )
                for x in filter(
                    lambda attr: True if "cpix:PSSH" in attr else False,
                    root["cpix:DRMSystemList"]["cpix:DRMSystem"],
                )
            ]
        )
        self.widevine_pssh = (
            self.psshList[WIDEVINE_SYSID] if WIDEVINE_SYSID in self.psshList else None
        )
        self.playready_pssh = (
            self.psshList[PLAYREADY_SYSID] if PLAYREADY_SYSID in self.psshList else None
        )
        return self

    def writeDRMXML(self):
        environment = jinja2.Environment()
        template = environment.from_string(DRM_TEMPLATE)
        output = template.render(
            kid=self.kid.replace('-', '').upper(),
            secret_key =  self.secretKey,
            iv =self.explicitIV, 
            playready_id=PLAYREADY_SYSID,
            widevine_id=WIDEVINE_SYSID,
            widevine_pssh= self.widevine_pssh ,
            playready_pssh=self.playready_pssh 
        )
        print(output)