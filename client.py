# client

import socket
import csv
import struct
from sys import argv

HOST = "localhost"  # will send to localhost (127.0.0.1)
PORT = 19999  # will send to port 19999

# data csv filename
filename = "sample.csv"
if argv.__len__() >= 2:
    filename = argv[1]


# loads csv file when given a filename (in folder) or path (anywhere in machine)
def loadCSV(path: str):
    try:
        with open(path, mode="r") as file:
            reader = csv.reader(file, delimiter=',')            # loading file with csv library

            data = []                                           # this will be the uniform list of floats to be returned

            mass_column = reader.__next__().index("Mass")       # skipping the first row and using it to find the Mass row
            for row in reader:                                  # adding any non-empty entry in the "Mass" column to the data list (in float form)
                if row[mass_column] != "":
                    data.append(float(row[mass_column]))
        return data
    except FileNotFoundError:
        print("Error in file path")
        return []


# these two functions encode and decode data to be sent over the socket
def packData(data: [float]):
    return struct.pack(f"!{data.__len__()}d", *data)


def unpackResults(results: bytes):
    final = []
    for i in range(int(results.__len__()/17)):
        final.append(struct.unpack("!dds", results[i*17: i*17+17]))
    return final


# loading data before establishing connection so, if there is a client-side file error, the server is not bothered
data = packData(loadCSV(filename))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(data)                                      # encoding, sending float list
        for row in unpackResults(sock.recv(2048)):              # receiving, decoding, outputting list of basecallings
            print(row)
except ConnectionError:
    print("Connection lost or not established, please try again")
