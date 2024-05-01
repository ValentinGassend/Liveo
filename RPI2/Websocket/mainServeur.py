from WebsocketManager import WSServer

address = '192.168.1.18'
port = 8082
server = WSServer(address, port)
server.start()
try:
    while True:
        server.handle_clients()

        messages = server.get_received_messages()
        for message in messages:
            for client_socket in server.clients:  # Parcours des clients connectés
                server.state.handle_message(server, message, client_socket)  # Utilisation de client_socket
except KeyboardInterrupt:
    server.stop()
