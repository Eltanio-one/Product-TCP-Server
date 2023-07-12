import asyncio
import sys
from resources.globals import DISCONN_MSG, NOTFOUND_MSG, HEADER, HOST, PORT


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
    data = sys.argv[1].encode()
    data_len = len(data)
    send_length = str(data_len).encode()
    send_length += b" " * (HEADER - len(send_length))
    # send message to server
    writer.write(send_length)
    writer.write(sys.argv[1].encode())
    # flush write buffer
    await writer.drain()
    # wait for response from server
    # 10 bytes as the largest string that could be passed is the disconnect message
    list_price = await reader.read(10)
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
