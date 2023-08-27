from ezdrm import EZDrm


def main():
    url = "https://cpix.ezdrm.com/keygenerator/cpix2.aspx?k=b44f9e30-2fb6-49b4-990f-01f3fc4bfe2d&u=cpix@ezdrm.com&p=s3cur3!!02&c=Mp4box-test01"
    drm = EZDrm(url).fetch().parseKeys()
    print(drm.contentId)


if __name__ == "__main__":
    main()
