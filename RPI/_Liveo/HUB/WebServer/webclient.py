import socketio

class WebSocketClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.sio = socketio.Client()
        self.connected = False

        @self.sio.event
        def connect():
            self.connected = True 
            self.send_message('Init')# Envoyer le message lorsque la connexion est établie

        @self.sio.event
        def disconnect():
            self.connected = False

    def connect(self):
        self.sio.connect(self.server_address)

    def isConnected(self):
        return self.connected

    def disconnect(self):
        self.sio.disconnect()

    def send_message(self, message):
        self.sio.emit('message', message)

# client = WebSocketClient('http://192.168.1.16:3000/')
# client.connect()
# while True:
#     if client.isConnected():
#         # Vous pouvez placer d'autres actions ici avant d'envoyer un message
#         client.send_message("This is my data")
#         # client.disconnect()
#     # Vous pouvez ajouter une pause ou un délai ici si nécessaire

