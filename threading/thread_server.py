import socket
import threading
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.setup import PRODUCT_LIST, PRICE_LIST
from config.globals import HEADER, DISCONN_MSG, NOTFOUND_MSG, HOST, PORT

# init product dictionary
PRODUCT_DICT = dict(zip(PRODUCT_LIST, PRICE_LIST))


def main() -> None:
    # create socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to the host and PORT
    sock.bind((HOST, PORT))
    # set 30 second timeout for server
    sock.settimeout(30.0)
    print("[STARTING] Server is starting...")
    # execute start_socket function
    start_socket(sock)
    # close the socket
    sock.close()


def handle_client(conn, addr) -> None:
    """this function runs concurrently for each client"""
    print(f"[NEW CONNECTION] New connection by {addr}")
    while True:
        # receive decoded header (decoded using utf-8 format)
        data_len = conn.recv(HEADER).decode()
        if data_len:
            # convert data_len to int
            data_len = int(data_len)
            # receive decoded request
            data = conn.recv(data_len).decode()
            # handle disconnecting client from server
            if data == DISCONN_MSG:
                print("[DISCONNECTING] Client disconnecting...")
                data = DISCONN_MSG.encode()
                conn.send(data)
                break
            # handle invalid request i.e. product code doesn't exist
            if not PRODUCT_DICT.get(data):
                print("[ERROR] That product code is not handled by this server...")
                data = NOTFOUND_MSG.encode()
                conn.send(data)
                break
            # handle valid request
            else:
                print(f"[PASSING] List Price: {PRODUCT_DICT[data]}")
                data = PRODUCT_DICT[data].encode()
                conn.send(data)
    # close connection between server and client
    conn.close()


def start_socket(sock: socket) -> None:
    """start the socket up"""
    print(f"[LISTENING] Server is listening on {HOST}...")
    # set socket to listen for requests
    sock.listen()
    try:
        while True:
            # set new timeout each time loop runs
            sock.settimeout(30.0)
            # wait for client to connect with a request
            conn, addr = sock.accept()
            # assign thread to execute handle_client function, enabling handler to manage the connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            # start the thread
            thread.start()
            # print total connections during this run
            print(f"Total connections: {threading.active_count() - 1}")
    # handle if server times out after 30 seconds of inactivity
    except TimeoutError:
        print("[TIMEOUT] Server timed out...")
    finally:
        return


if __name__ == "__main__":
    main()
