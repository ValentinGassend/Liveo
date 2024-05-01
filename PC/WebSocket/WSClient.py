import socket

class WSClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))
        print("Connecté au serveur WebSocket.")

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.sendall(message.encode("utf-8"))

    def receive_message(self):
        if self.client_socket:
            message = self.client_socket.recv(1024)
            if message:
                return message.decode("utf-8")
        return None

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print("Déconnecté du serveur WebSocket.")
