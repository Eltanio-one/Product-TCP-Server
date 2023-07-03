import socket
import sys
from keys import HOST, PORT


def main():
    if len(sys.argv) != 2:
        print("Usage: client.py <product_code>")
        return
    # create a socket object with the IP family IPv4 and using TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect to the global host and port
        s.connect((HOST, PORT))
        # send "Hello, world"
        s.sendall(b"Hello, world")
        # read the servers reply
        data = s.recv(1024)
    # print the servers reply
    print(f"Received {data!r}")
