import socket
from keys import HOST, PORT

HEADER = 64
FORMAT = "utf-8"
DISCONN_MSG = "!DISCONNECT"


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    send_data("hello, world", client)
    send_data(DISCONN_MSG, client)


def send_data(data, client):
    data = data.encode(FORMAT)
    data_len = len(data)
    send_length = str(data_len).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(data)


if __name__ == "__main__":
    main()
