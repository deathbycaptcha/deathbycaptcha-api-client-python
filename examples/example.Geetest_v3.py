# geetest v3
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

# IMPORTANT: challenge parameter changes everytime
# target site realoads the page
# in this case we can see parameters here
# https://www.geetest.com/demo/gt/register-enFullpage-official?t=1664547919370
# just in this case, every site is different
# we must examine the api calls to geetest to get the challenge

# Put the proxy and Geetest token data

Captcha_dict = {
    'proxy': 'http://user:password@127.0.0.1:1234',
    'proxytype': 'HTTP',
    'gt': '022397c99c9f646f6477822485f30404',
    'challenge': '536b43c61236cf1964dc93bfde421126',
    'pageurl': 'https://www.geetest.com/en/demo'}


# Create a json string
json_Captcha = json.dumps(Captcha_dict)

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type and Json payload here:
    captcha = client.decode(type=8, geetest_params=json_Captcha)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] item its response.
        print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        # # To access the response by item
        # print ("challenge:", captcha["text"]["challenge"])
        # print ("validate:", captcha["text"]["validate"])
        # print ("seccode:", captcha["text"]["seccode"])

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print ("error: Access to DBC API denied," +
           "check your credentials and/or balance")
