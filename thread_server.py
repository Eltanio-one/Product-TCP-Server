import socketserver
from setup_files.setup import PRODUCT_LIST, PRICE_LIST
from setup_files.globals import (
    HEADER,
    DISCONN_MSG,
    NOTFOUND_MSG,
    HOST,
    PORT,
)

# init product dictionary
PRODUCT_DICT = dict(zip(PRODUCT_LIST, PRICE_LIST))


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data_len = self.request.recv(HEADER).decode().strip()
        if data_len:
            # convert data_len to int
            data_len = int(data_len)
            # receive decoded request
            data = self.request.recv(data_len).decode()
            # handle disconnecting client from server
            if data == DISCONN_MSG:
                print("[DISCONNECTING] Client disconnecting...")
                data = DISCONN_MSG.encode()
                self.request.send(data)

            # handle invalid request i.e. product code doesn't exist
            if not PRODUCT_DICT.get(data):
                print("[ERROR] That product code is not handled by this server...")
                data = NOTFOUND_MSG.encode()
                self.request.send(data)
            # handle valid request
            else:
                print(f"[PASSING] List Price: {PRODUCT_DICT[data]}")
                data = PRODUCT_DICT[data].encode()
                self.request.send(data)


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    # create socket object
    with socketserver.TCPServer((HOST, PORT), Handler_TCPServer) as sock:
        # set 30 second timeout for server
        sock.serve_forever()
