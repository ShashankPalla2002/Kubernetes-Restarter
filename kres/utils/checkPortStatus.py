import socket

class CheckPortStatus:
    def __init__(self, port=5454):
        self.port = port

    def isPortOpen(self, ):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(("127.0.0.1", self.port)) == 0