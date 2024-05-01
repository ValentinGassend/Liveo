import socket
import select
import time

class WSServerState:
    def handle_clients(self, server):
        pass

    def handle_message(self, server, message, client_socket):
        pass


class WSServerStateRunning(WSServerState):
    def __init__(self, led_state_machine):
        self.led_state_machine = led_state_machine

    def handle_message(self, server, message, client_socket):
        if message == "START":
            server.send_to_all_clients("Server is running")
        elif message == "STOP":
            server.send_to_all_clients("Server is stopped")
        elif message == "DISCONNECT":
            server.send_to_all_clients("Client disconnected: " + str(client_socket.getpeername()))
            server.clients.remove(client_socket)
            client_socket.close()
        elif message == "LED":
            server.send_to_all_clients("LED_static")
            self.led_state_machine.handle_command("LED_static")  # Nouvelle commande pour la machine à état de LED
        elif message == "LED_STATE":
            server.send_to_all_clients("Current state: " + self.led_state_machine.get_led_status())  # Utilise la machine à état de LED pour obtenir l'état
        else:
            print("Invalid command")

    def get_current_state(self):
        return self.led_state_machine.get_led_status()

    def handle_clients(self, server):
        inputs = [server.server_socket] + server.clients
        outputs = []

        try:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs)

            for sock in readable:
                if sock is server.server_socket:
                    # Nouvelle connexion entrante
                    client_socket, client_address = server.server_socket.accept()
                    print("Nouvelle connexion client :", client_address)
                    client_socket.setblocking(0)
                    server.clients.append(client_socket)
                    server.send_to_all_clients("ID")
                else:
                    # Données reçues d'un client existant
                    try:
                        message = sock.recv(1024)
                        if message:
                            # Traitez le message reçu ici
                            message = message.decode("utf-8")
                            print("Message reçu :", message)
                            server.received_messages.append(message)
                            self.handle_message(server, message, sock)  # Appel de la méthode handle_message mise à jour
                        else:
                            # Connexion fermée par le client
                            print("Connexion fermée :", sock.getpeername())
                            sock.close()
                            server.clients.remove(sock)
                    except:
                        pass
        except:
            pass


class WSServer:
    def __init__(self, address, port, led_state_machine):
        self.server_address = address
        self.server_port = port
        self.server_socket = None
        self.clients = []
        self.received_messages = []
        self.state = WSServerStateRunning(led_state_machine)

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Serveur WebSocket démarré.")

    def handle_clients(self):
        self.state.handle_clients(self)

    def send_to_all_clients(self, message):
        for client_socket in self.clients:
            try:
                print("Message envoyé : " + message)
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
    def __init__(self, server_address, server_port, client_id):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.client_id = client_id

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.sendall(message.encode("utf-8"))

    def is_server_active(self):
        # Envoie un message spécial au serveur
        self.send_message("PING")

        # Attend une réponse du serveur pendant 1 seconde
        start_time = time.time()
        while time.time() - start_time < 1:
            received_message = self.receive_message()
            if received_message == "LED_PONG":
                return True

        return False

    def receive_message(self):
        if self.client_socket:
            message = self.client_socket.recv(1024)
            if message:
                return message.decode("utf-8")
        return None

    def get_id(self):
        return self.client_id

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            print("Disconnected from the WebSocket server.")
