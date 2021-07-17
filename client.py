# client

import socket
import csv

HOST = "localhost"  # will send to localhost (127.0.0.1)
PORT = 19999  # will send to port 19999

# data csv filename
filename = "sample.csv"


# loads csv file when given a filename (in folder) or path (anywhere in machine)
def load_csv(path: str) -> [float]:
    try:
        with open(path, mode="r") as file:
            reader = csv.reader(file, delimiter=',')        # loading file with csv library

            data = []                                       # this will be the uniform list of floats to be returned

            mass_column = reader.__next__().index("Mass")   # skipping the first row and using it to find the Mass row
            for row in reader:                              # adding any non-empty entry in the "Mass" column to the data list (in float form)
                if row[mass_column] != "":
                    data.append(float(row[mass_column]))
        return data
    except FileNotFoundError:
        print("Error in file path")
        return []


# loading data before establishing connection so, if there is a client-side file error, the server is not bothered
data = load_csv(filename)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(repr(data), 'utf-8'))  # encoding, sending float list
        print(sock.recv(2048).decode('utf-8'))  # receiving, decoding, outputting list of basecallings
except ConnectionError:
    print("Connection lost or not established, please try again")
