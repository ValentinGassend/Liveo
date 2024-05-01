import socket
import select
from datetime import datetime, timezone, timedelta


class WSServer:
    def __init__(self, address, port):
        self.server_address = address
        self.server_port = port
        self.received_messages = []
        self.clients = []

        # @self.app.route('/')
        # def index():
        #     current_time = datetime.now(timezone(timedelta(hours=2)))  # Adjust the timezone offset as per France
        #     formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        #     return render_template('index.html', current_time=formatted_time)

        # @self.app.route('/send', methods=['POST'])
        # def receive_message():
        #     message = request.form.get('message')
        #     if message:
        #         self.received_messages.append(message)
        #     return "Message received."

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_address, self.server_port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Serveur WebSocket démarré.")

    def handle_clients(self):
        inputs = [self.server_socket]
        outputs = []

        try:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs, 0.1)

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
