# geetest v4
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
client = deathbycaptcha.SocketClient(username, password)

# to use authtoken
# client = deathbycaptcha.SocketClient(username, password, authtoken)

# client = deathbycaptcha.HttpClient(username, password)

# Put the proxy and Geetest token data
Captcha_dict = {
    'proxy': 'http://user:password@127.0.0.1:1234',
    'proxytype': 'HTTP',
    'captcha_id': 'fcd636b4514bf7ac4143922550b3008b',
    'pageurl': 'https://www.geetest.com/en/adaptive-captcha-demo'}


# Create a json string
json_Captcha = json.dumps(Captcha_dict)

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type and Json payload here:
    captcha = client.decode(type=9, geetest_params=json_Captcha)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] item its response.
        print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        # # To access the response by item
        # print ("captcha_id:", captcha["text"]["captcha_id"])
        # print ("lot_number:", captcha["text"]["lot_number"])
        # print ("pass_token:", captcha["text"]["pass_token"])
        # print ("gen_time:", captcha["text"]["gen_time"])
        # print ("captcha_output:", captcha["text"]["captcha_output"])

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print ("error: Access to DBC API denied," +
           "check your credentials and/or balance")
