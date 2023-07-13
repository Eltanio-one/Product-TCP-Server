import socket
import sys
from config.globals import HEADER, DISCONN_MSG, NOTFOUND_MSG, HOST, PORT


def main():
    # ensure required CLI arguments passed
    if len(sys.argv) != 2:
        print("Usage: client.py <product code>")
        return
    # initialise socket client-side, running on IPv4.
    client = socket_setup(HOST, PORT)
    send_data(sys.argv[1], client)
    # send the data passed at the command line and client to the send_data func
    # send_data(sys.argv[1], client)
    # receive incoming data from server
    data = client.recv(1024).decode()
    handle_response(data, client)


def socket_setup(host, port):
    """setup client socket"""
    # initialise socket client-side, running on IPv4.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect client socket to host and port
    client.connect((host, port))
    return client


def send_data(data, client):
    """send product code to server"""
    # encode the data pre-send
    data = data.encode()
    data_len = len(data)
    # generate send-length based on header
    send_length = str(data_len).encode()
    # pad out the send length to be 64 bytes long
    # following TCP protocol of first sending the length of the message about to be sent
    # before sending the message itself
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(data)


def handle_response(data, client):
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


if __name__ == "__main__":
    main()
