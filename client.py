# client

import socket

HOST = "localhost"  # will send to localhost (127.0.0.1)
PORT = 19999        # will send to port 19999

# data csv filename
filename = "sample.csv"


# loading data before establishing connection so, if there is a client-side file error, the server is not bothered
with open(file=filename, mode="rb") as file:    # file is left in bytes form because the connection will require bytes anyways
    data = file.read()


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(data)                      # sending data to server
except ConnectionError:
    print("Connection lost or not established, please try again")
