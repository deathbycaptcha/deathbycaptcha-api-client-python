# cutcaptcha
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

# Put the proxy and cutcaptcha data
Captcha_dict = {
    'proxy': 'http://user:password@127.0.0.1:1234',
    'proxytype': 'HTTP',
    'apikey': 'SAs61IAI',
    'miserykey': '56a9e9b989aa8cf99e0cea28d4b4678b84fa7a4e',
    'pageurl': 'https://filecrypt.cc/Contact.html'
}

# Create a json string
json_Captcha = json.dumps(Captcha_dict)

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type and Json payload here:
    captcha = client.decode(type=19, cutcaptcha_params=json_Captcha)
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] its text token solution.
        print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])

except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print("error: Access to DBC API denied, check your credentials and/or balance")
