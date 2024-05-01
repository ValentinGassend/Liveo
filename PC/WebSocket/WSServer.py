import socket
import select


class WSServer:
    def __init__(self, address, port):
        self.server_address = address
        self.server_port = port
        self.server_socket = None
        self.clients = []
        self.received_messages = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Serveur WebSocket démarré.")

    def handle_clients(self):
        inputs = [self.server_socket] + self.clients
        outputs = []

        try:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)

            for sock in readable:
                if sock is self.server_socket:
                    # Nouvelle connexion entrante
                    client_socket, client_address = self.server_socket.accept()
                    print("Nouvelle connexion client :", client_address)
                    client_socket.setblocking(0)
                    self.clients.append(client_socket)
                    self.send_to_all_clients("ID")
                else:
                    # Données reçues d'un client existant
                    try:
                        message = sock.recv(1024)
                        if message:
                            # Traitez le message reçu ici
                            message = message.decode("utf-8")
                            print("Message reçu :", message)
                            self.received_messages.append(message)
                        else:
                            # Connexion fermée par le client
                            print("Connexion fermée :", sock.getpeername())
                            sock.close()
                            self.clients.remove(sock)
                    except:
                        pass
        except:
            pass

    def send_to_all_clients(self, message):
        for client_socket in self.clients:
            try:
                print("Message envoyé : "+message)
                client_socket.sendall(message.encode("utf-8"))
            except ConnectionResetError:
                client_socket.close()
                self.clients.remove(client_socket)
                print("Connexion réinitialisée :", client_socket.getpeername())

    def get_received_messages(self):
        messages = self.received_messages.copy()
        self.received_messages.clear()
        return messages

    def stop(self):
        for client_socket in self.clients:
            client_socket.close()
        self.clients = []

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            print("Serveur WebSocket arrêté.")

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
