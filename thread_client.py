import socket
import sys
from keys import HOST, PORT
from globals import HEADER, DISCONN_MSG, NOTFOUND_MSG


def main():
    # ensure required CLI arguments passed
    if len(sys.argv) != 2:
        print("Usage: client.py <product code>")
        return
    # initialise socket client-side, running on IPv4.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect client socket to host and port
    client.connect((HOST, PORT))
    # send the data passed at the command line and client to the send_data func
    send_data(sys.argv[1], client)
    # receive incoming data from server
    data = client.recv(1024).decode()
    # handle if invalid product code passed to server
    if data == NOTFOUND_MSG:
        print("[ERROR] That product code is not handled by this server...")
        client.close()
    # handle if attempting to disconnect
    elif data == DISCONN_MSG:
        print("[DISCONNECT] Connection terminated...")
        client.close()
    # handle valid request, print list price
    else:
        print(f"List Price: {data}")
        client.close()


def send_data(data, client):
    """send product code to server"""
    # encode the data pre-send
    data = data.encode()
    data_len = len(data)
    # generate send-length based on header
    send_length = str(data_len).encode()
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(data)


if __name__ == "__main__":
    main()
