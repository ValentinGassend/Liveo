from abc import ABC, abstractmethod
import socket
import select
class WebSocketState(ABC):
    @abstractmethod
    def handle_message(self, server, message, client_socket):
        pass

class AppointmentInfoState(WebSocketState):
    def handle_message(self, server, message, client_socket):
        if message == "ID":
            # Envoie la réponse appropriée au client
            if condition:  # Vérifiez la condition pour "PC"
                server.send_response(client_socket, "PC")
            else:  # Vérifiez la condition pour "LED"
                server.send_response(client_socket, "LED")
        else:
            # Gérez le traitement des informations du rendez-vous
            pass

class MakeChoiceState(WebSocketState):
    def handle_message(self, server, message, client_socket):
        # Gérez le traitement pour faire un choix
        pass

class BooleanState(WebSocketState):
    def handle_message(self, server, message, client_socket):
        # Gérez le traitement pour un booléen
        pass

class ReminderInfoState(WebSocketState):
    def handle_message(self, server, message, client_socket):
        # Gérez le traitement pour les informations de rappel
        pass

class WSServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.state = AppointmentInfoState()
        self.clients = []

    def set_state(self, state):
        self.state = state

    def handle_message(self, message, client_socket):
        self.state.handle_message(self, message, client_socket)

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
                            if not message == "PING":
                                print("Message reçu :", message)
                            server.received_messages.append(message)
                        else:
                            # Connexion fermée par le client
                            print("Connexion fermée :", sock.getpeername())
                            sock.close()
                            server.clients.remove(sock)
                    except:
                        pass
        except:
            pass

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.address, self.port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Serveur WebSocket démarré.")
