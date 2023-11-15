from ezdrm import EZDrm


def main():
    url = "https://cpix.ezdrm.com/keygenerator/cpix2.aspx"
    kid = "b44f9e30-2fb6-49b4-990f-01f3fc4bfe2d"
    user = ""
    password = ""
    content = "Mp4box-test01"
    drm = EZDrm(url, kid, content, user, password).fetch().parseKeys()
    drm.parseKeys()
    drm.writeDRMXML()


if __name__ == "__main__":
    main()
