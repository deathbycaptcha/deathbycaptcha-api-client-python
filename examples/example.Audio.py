# Audio
import os
import sys
import base64

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

# Read the audio file and get the base64 string
try:
    with open('images/audio.mp3', 'rb') as file:
        audio_data = file.read()
        base_string = base64.b64encode(audio_data).decode()
except Exception as e:
    print("An error occurred while converting the file to base64: " + str(e))

try:
    balance = client.get_balance()
    print(balance)

    # Put your CAPTCHA type, the base64 string and the language:
    captcha = client.decode(type=13, audio=base_string, language="en")
    if captcha:
        # The CAPTCHA was solved; captcha["captcha"] item holds its
        # numeric ID, and captcha["text"] its text token solution.
        print("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))

        if '':  # check if the CAPTCHA was incorrectly solved
            client.report(captcha["captcha"])

except deathbycaptcha.AccessDeniedException:
    # Access to DBC API denied, check your credentials and/or balance
    print("error: Access to DBC API denied, check your credentials and/or balance")
