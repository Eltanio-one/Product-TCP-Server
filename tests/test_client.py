import unittest
import asyncio
from resources.setup import HOST, PORT


class TestCase(unittest.TestCase):
    def setUp(self):
        client_socket = asyncio.open_connection(HOST, PORT)
