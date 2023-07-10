import asyncio
from keys import HOST, PORT, PRODUCT_LIST, PRICE_LIST
from globals import DISCONN_MSG, NOTFOUND_MSG

# init product dictionary
PRODUCT_DICT = dict(zip(PRODUCT_LIST, PRICE_LIST))


async def handle_client(reader, writer):
    # collect the data sent by the client
    data = await reader.read(1024)
    addr, data = writer.get_extra_info("peername"), data.decode()

    # log the request
    print(f"[RECEIVED] {addr}: {data}")

    # check data in product_dict
    if data == DISCONN_MSG:
        print("[DISCONNECTING] Client disconnecting...")
        writer.write(data)
        await writer.drain()
    # handle invalid request i.e. product code doesn't exist
    if not PRODUCT_DICT.get(data):
        print("[ERROR] That product code is not handled by this server...")
        writer.write(NOTFOUND_MSG.encode())
        await writer.drain()
    # handle valid request
    else:
        print(f"[PASSING] List Price: {PRODUCT_DICT[data]}")
        data = PRODUCT_DICT[data].encode()
        writer.write(data)
        await writer.drain()

    # terminate connection
    print("[DISCONNECTING] Server disconnecting...")
    writer.close()
    await writer.wait_closed()


async def main():
    sock = await asyncio.start_server(handle_client, HOST, PORT)
    addrs = ", ".join(str(sock.getsockname()) for sock in sock.sockets)
    print(f"[SERVER] Serving on {addrs}")

    async with sock:
        await sock.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
