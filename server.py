# server

import socket
import struct
from threading import Thread

HOST = "localhost"  # will listen on localhost (127.0.0.1)
PORT = 19999        # will listen on port 9999

bases = {           # given number differences for RNA bases
    'A': 329.0525,
    'C': 305.0413,
    'G': 345.0474,
    'U': 306.0253,
}


def connectionHandler(connection, address):
    print(f"Connection established with {address[0]}:{address[1]}")
    message = connection.recv(8192)
    data = unpackData(message)                                  # processing the received bytes to a float list
    results = processData(data)                                 # getting list of basecallings
    connection.sendall(packCallings(results))                   # encoding, sending the basecallings to the client
    connection.close()
    print(f"Connection closed with {address[0]}:{address[1]}")


# looks for basecallings, packs any that are found in a list of tuples
def processData(data):
    results = []
    for i, _ in enumerate(data):
        for j in range(i+1, data.__len__()):
            floatv = data[i]
            floatu = data[j]
            base = findBase(floatv, floatu)
            if base is not None:
                results.append((floatv, floatu, base))
    return results


# checks to see if there are any matches with known differences for RNA bases
def findBase(begin, end):
    difference = abs(end - begin)
    for base in bases:
        if abs(bases[base] - difference) <= 1E-6 * bases[base]:
            return base
    return None


# decoding bytes to list of floats
def unpackData(packedData: bytes):
    unpacked = struct.unpack(f"!{int(packedData.__len__()/8)}d", packedData)
    return unpacked


# encoding list of tuples in form (float, float, str) to bytes
def packCallings(unpackedCallings: [tuple]):
    packed = b""
    for calling in unpackedCallings:
        packed += struct.pack(f"!dds", calling[0], calling[1], bytes(calling[2], "utf-8"))
    return packed


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()                                   # listening on the specified host and port
    print(f"Listening on {HOST}:{PORT}")
    while True:
        conn, addr = sock.accept()
        if conn is not None:
            Thread(target=connectionHandler, args=(conn, addr,)).start()     # runs every time a client establishes a connection
