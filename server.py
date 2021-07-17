# server

import socket

HOST = "localhost"  # will listen on localhost (127.0.0.1)
PORT = 19999        # will listen on port 9999

bases = {           # given number differences for RNA bases
    'A': 329.0525,
    'C': 305.0413,
    'G': 345.0474,
    'U': 306.0253,
}


# looks for basecallings, packs any that are found in a list of tuples
def processData(data):
    results = []
    for i in range(len(data) - 1):
        floatv = data[i]
        floatu = data[i + 1]
        base = findBase(floatv, floatu)
        if base is not None:
            results.append((floatv, floatu, base))
    return results


# checks to see if there are any matches with known differences for RNA bases
def findBase(begin, end):
    difference = abs(end - begin)
    for base in bases:
        if abs(bases[base] - difference) <= 1E-6:
            return base
    return None


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()       # listening on the specified host and port
    while True:
        with sock.accept()[0] as connection:        # runs every time a client establishes a connection
            message = connection.recv(2048).decode("utf-8")
            data = [float(i.strip()) for i in message.strip('[]').split(',')]   # processing the received bytes to a float list
            results = processData(data)                         # getting list of basecallings
            connection.sendall(bytes(repr(results), 'utf-8'))   # encoding, sending the basecallings to the client