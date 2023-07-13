import unittest
from asyncio import open_connection

from config.setup import HOST, PORT
from config.globals import HEADER


class TestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.reader, self.writer = await open_connection(HOST, PORT)

    async def test_response(self):
        data = "LT07-517".encode()
        data_len = len(data)
        send_length = str(data_len).encode()
        send_length += b" " * (HEADER - len(send_length))
        self.writer.write(send_length)
        self.writer.write(data)
        response = await self.reader.read(10)
        self.assertEqual(response.decode(), "£105")

    async def asynctearDown(self):
        self.reader.close()
        self.writer.close()
        await self.reader.wait_closed()
        await self.writer.wait_closed()


if __name__ == "__main__":
    unittest.main()
