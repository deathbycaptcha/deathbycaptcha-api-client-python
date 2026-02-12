import deathbycaptcha
import sys

# get credentials from the command line
username = sys.argv[1]
password = sys.argv[2]
is_http = sys.argv[3]
authtoken = ""


# client = deathbycaptcha.SocketClient(username, password, authtoken)
# to use http client client = deathbycaptcha.HttpClient(username, password)

if is_http == "HTTP":

    http_client = deathbycaptcha.HttpClient(username, password, authtoken)

    try:
        balance = http_client.get_balance()
        print("Python3 http", balance)
        balance_float = float(balance)
        sys.exit(0)
    except Exception as e:
        # Access to DBC API denied, check your credentials and/or balance
        print ("***** PYTHON3 HTTP FAILED *****")
        print(e)
        sys.exit(1)

else:

    socket_client = deathbycaptcha.SocketClient(
        username, password, authtoken)

    try:
        balance = socket_client.get_balance()
        print("Python3 sockets", balance)
        balance_float = float(balance)
        sys.exit(0)
    except Exception as e:
        # Access to DBC API denied, check your credentials and/or balance
        print ("***** PYTHON3 SOCKETS FAILED *****")
        print(e)
        sys.exit(1)
