import asyncio
import sys
from keys import HOST, PORT
from globals import DISCONN_MSG, NOTFOUND_MSG


async def main():
    # handle command line arguments
    if len(sys.argv) != 2:
        print("Usage: client.py <product code>")
        return
    # await connection to be made via the global host and port
    # returns reader and writer objects
    reader, writer = await asyncio.open_connection(HOST, PORT)
    # log message sending
    print(f"[SENDING] {sys.argv[1]}")
    # send message to server
    writer.write(sys.argv[1].encode())
    # flush write buffer
    await writer.drain()
    # wait for response from server
    # 13 bytes as the largest product code covered in the dict is 12 bytes
    list_price = await reader.read(13)
    # decode response
    list_price = list_price.decode()
    # handle not found and disconnecting messages
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
