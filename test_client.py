import unittest
import asyncio
from setup_files.setup import HOST, PORT
from setup_files.globals import HEADER


class TestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.reader, self.writer = await asyncio.open_connection(HOST, PORT)

    async def test_response(self):
        data = "LT07-517".encode()
        data_len = len(data)
        send_length = str(data_len).encode()
        send_length += b" " * (HEADER - len(send_length))
        self.writer.write(send_length)
        self.writer.write(data)
        response = await self.reader.read(10)
        response = response.decode()
        self.assertEqual(response, "£105")
