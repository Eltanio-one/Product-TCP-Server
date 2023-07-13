import unittest
import socket
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from config.setup import HOST, PORT
from config.globals import HEADER


class TestCase(unittest.TestCase):
    def setUp(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def test_response(self):
        data = "LT07-517".encode()
        data_len = len(data)
        send_length = str(data_len).encode()
        send_length += b" " * (HEADER - len(send_length))
        self.sock.send(send_length)
        self.sock.send(data)
        self.assertEqual(self.sock.recv(1024).decode(), "£105")

    def tearDown(self):
        self.sock.close()


if __name__ == "__main__":
    unittest.main()
