# recaptcha_v3
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

# Put the proxy and recaptcha_v3 data
# recaptcha_v3 requires 'action' that is the action that triggers
# recaptcha_v3 validation
# if 'action' isn't provided we use the default value "verify"
# also you need to provide 'min_score', a number from 0.1 to 0.9,
# this is the minimum score acceptable from recaptchaV3

Captcha_dict = {
    'proxy': 'http://user:password@127.0.0.1:1234',
    'proxytype': 'HTTP',
    'googlekey': '6LdyC2cUAAAAACGuDKpXeDorzUDWXmdqeg-xy696',
    'pageurl': 'https://recaptchav3.demo.com/scores.php',
    'action': "examples/v3scores",
    'min_score': 0.3}

# Create a json string
json_Captcha = json.dumps(Captcha_dict)

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type and Json payload here:
    captcha = client.decode(type=5, token_params=json_Captcha)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] item it's a list of "coordinates".
        print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])
except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print("error: Access to DBC API denied, check your credentials and/or balance")
