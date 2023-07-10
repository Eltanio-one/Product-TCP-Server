import asyncio
import sys
from keys import HOST, PORT
from globals import DISCONN_MSG, NOTFOUND_MSG


async def main():
    if len(sys.argv) != 2:
        print("Usage: client.py <product code>")
        return
    # connect client socket to host and port
    reader, writer = await asyncio.open_connection(HOST, PORT)
    # log message sending
    print(f"[SENDING] {sys.argv[1]}")
    writer.write(sys.argv[1].encode())
    await writer.drain()

    list_price = await reader.read(1024)
    list_price = list_price.decode()
    if list_price == NOTFOUND_MSG:
        print("[ERROR] That product code is not handled by this server...")
        writer.close()
        await writer.wait_closed()
    # handle if attempting to disconnect
    elif list_price == DISCONN_MSG:
        print("[DISCONNECT] Connection terminated...")
        writer.close()
        await writer.wait_closed()
    # handle valid request, print list price
    else:
        print(f"[RECEIVED] List Price: {list_price}")
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
