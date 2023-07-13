import asyncio
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.setup import PRODUCT_LIST, PRICE_LIST
from config.globals import HEADER, DISCONN_MSG, NOTFOUND_MSG, HOST, PORT

# init product dictionary
PRODUCT_DICT = dict(zip(PRODUCT_LIST, PRICE_LIST))


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    # receive header length data_len that is first sent by client
    data_len = await reader.read(HEADER)
    data_len = int(data_len.decode())
    # collect the data sent by the client and their address
    # 11 bytes as the largest product code covered in the dict is 11 bytes
    data = await reader.read(data_len)
    addr, data = writer.get_extra_info("peername"), data.decode()

    # log the request
    print(f"[RECEIVING] {addr}: {data}")

    # check if client disconnected
    if data == DISCONN_MSG:
        # log to server that client is disconnecting
        print("[DISCONNECTING] Client disconnecting...")
        # write DISCONN_MSG back to the server
        writer.write(data.encode())
        # flush write buffer
        await writer.drain()
        # log disconnect ofserverside connection
        print("[DISCONNECTING] Server disconnecting...")
        # close connection
        writer.close()
        # don't finish executing until connection is closed, to ensure all write data has been flushed
        await writer.wait_closed()
    # handle invalid request i.e. product code doesn't exist
    elif not PRODUCT_DICT.get(data):
        print("[ERROR] That product code is not handled by this server...")
        # write NOTFOUND_MSG back to the server
        writer.write(NOTFOUND_MSG.encode())
        # flush write buffer, will return once buffer passes low watermark
        await writer.drain()
    # handle valid request
    else:
        # log the list price is being passed
        print(f"[PASSING] List Price: {PRODUCT_DICT[data]}")
        # write to client the list price
        writer.write(PRODUCT_DICT[data].encode())
        # flush the write buffer
        await writer.drain()


async def main():
    # initialise our socket server with a callback function, and the relevant host and port
    sock = await asyncio.start_server(handle_client, HOST, PORT)
    # collect server address to be printed
    addrs = ", ".join(str(sock.getsockname()) for sock in sock.sockets)
    print(f"[SERVER] Serving on {addrs}")
    # while sock is active
    async with sock:
        # accept connections until connection closed
        await sock.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
