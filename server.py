import socket
import threading
from keys import HOST, PORT

HEADER = 64
FORMAT = "utf-8"
DISCONN_MSG = "!DISCONNECT"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    print("[STARTING] Server is starting...")
    start_socket(sock)


def handle_client(conn, addr):
    """this function runs concurrently for each client"""
    print(f"[NEW CONNECTION] New connection by {addr}")
    while True:
        data_len = conn.recv(HEADER).decode(FORMAT)
        if data_len:
            data_len = int(data_len)
            data = conn.recv(data_len).decode(FORMAT)
            if data == DISCONN_MSG:
                print("[DISCONNECTING] Client disconnecting...")
                break
            print(f"[{addr}]: {data}")
    conn.close()


def start_socket(sock):
    """start the socket up"""
    print(f"[LISTENING] Server is listening on {HOST}...")
    sock.listen()
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
