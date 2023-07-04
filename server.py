import socket
import threading
from keys import HOST, PORT, PRODUCT_LIST, PRICE_LIST

HOST = HOST
PORT = PORT
HEADER = 64
FORMAT = "utf-8"
DISCONN_MSG = "DISCONNECT"
NOTFOUND_MSG = "NOT FOUND"

# init product dictionary
PRODUCT_DICT = dict(zip(PRODUCT_LIST, PRICE_LIST))


"""LOOK AT SYNCRONYSING REQUESTS WITH GLOBAL INTERPRETER LOCK, OR A QUEUE OF THE RESPONSES"""


def main():
    # create socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket to the host and PORT
    sock.bind((HOST, PORT))
    sock.settimeout(60.0)
    print("[STARTING] Server is starting...")
    start_socket(sock)


def handle_client(conn, addr, sock):
    """this function runs concurrently for each client"""
    print(f"[NEW CONNECTION] New connection by {addr}")
    while True:
        data_len = conn.recv(HEADER).decode(FORMAT)
        if data_len:
            data_len = int(data_len)
            data = conn.recv(data_len).decode(FORMAT)
            if data == DISCONN_MSG:
                print("[DISCONNECTING] Client disconnecting...")
                data = DISCONN_MSG.encode(FORMAT)
                conn.send(data)
                break
            # at this stage, we need to query the dictionary
            if not PRODUCT_DICT.get(data):
                print("[ERROR] That product code is not handled by this server...")
                data = NOTFOUND_MSG.encode(FORMAT)
                conn.send(data)
                break
            else:
                print(f"[PASSING] List Price: {PRODUCT_DICT[data]}")
                data = PRODUCT_DICT[data].encode(FORMAT)
                conn.send(data)
    sock.close()
    conn.close()


def start_socket(sock):
    """start the socket up"""
    print(f"[LISTENING] Server is listening on {HOST}...")
    sock.listen()
    try:
        while True:
            conn, addr = sock.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, sock))
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
    except sock.error:
        print("[DISCONNECTING] Keyboard Interrupt Detected...")
    finally:
        sock.close()
        return


if __name__ == "__main__":
    main()
