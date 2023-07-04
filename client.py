import socket
import sys
from keys import HOST, PORT

HOST = HOST
PORT = PORT
HEADER = 64
FORMAT = "utf-8"
DISCONN_MSG = "!DISCONNECT"


def main():
    if len(sys.argv) != 2:
        print("Usage: client.py <product code>")
        return
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    send_data(sys.argv[1], client)
    send_data(DISCONN_MSG, client)


def send_data(data, client):
    """send product code to server"""
    data = data.encode(FORMAT)
    data_len = len(data)
    send_length = str(data_len).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(data)


if __name__ == "__main__":
    main()
