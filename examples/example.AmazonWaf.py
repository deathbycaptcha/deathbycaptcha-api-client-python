# Amazon Waf
import os
import sys

import deathbycaptcha
import json

# Put your DBC account username and password here.
username = "username"
password = "password"

# you can use authtoken instead of user/password combination
# activate and get the authtoken from DBC users panel
authtoken = "authtoken"

# to use socket client
# client = deathbycaptcha.SocketClient(username, password)

# to use authtoken
# client = deathbycaptcha.SocketClient(username, password, authtoken)

client = deathbycaptcha.HttpClient(username, password)

# Put the proxy and captcha data
Captcha_dict = {
    'proxy': 'http://user:password@127.0.0.1:1234',
    'proxytype': 'HTTP',
    'sitekey': 'AQIDAHjcYu/GjX+QlghicBgQ/7bFaQZ+m5FKCMDnO+vTbNg96AHDh0IR5vgzHNceHYqZR+GOAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMsYNQbVOLOfd/1ofjAgEQgDuhVKc2V/0XTEPc+9X/xAodxDqgyNNNyYJN1rM2gs4yBMeDXXc3z2ZxmD9jsQ8eNMGHqeii56iL2Guh4A==',
    'pageurl': 'https://efw47fpad9.execute-api.us-east-1.amazonaws.com/latest',
    'iv': 'CgAFRjIw2vAAABSM',
    'context': 'zPT0jOl1rQlUNaldX6LUpn4D6Tl9bJ8VUQ/NrWFxPiiFujn5bFHzpOlKYQG0Di/UrO/p0xItkf7oGrknHqnj+UjvWv+i0BFbm3vGKceNaGtjrg4wvydL2Li5XjwRUOMW4o+NgO3JPJhkgwRKSyK62cIIzrThlOBD+gmtvKW0JNtH8efKR8Y5mBf0gi8JokjUxq/XbyB6h83tfaiWrp3dkOJsEXHLkT/wwQlFZysA919LCA+XVqgJ9lurUZqHWar+9JHqWnc0ghckKCnUzubvSQzJl+eSIAIoYZrpuZQszOwWzo4='
}

# Create a json string
json_Captcha = json.dumps(Captcha_dict)

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type and Json payload here:
    captcha = client.decode(type=16, waf_params=json_Captcha)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] its text token solution.
        print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])

except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print("error: Access to DBC API denied, check your credentials and/or balance")
