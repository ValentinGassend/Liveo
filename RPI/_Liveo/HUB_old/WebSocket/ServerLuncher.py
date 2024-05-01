import socket
import select
import signal
import sys

from WSServer import WSServer

def signal_handler(signal, frame):
    print('Arrêt du serveur WebSocket.')
    sys.exit(0)


server_address = '192.168.1.16'
server_port = 8765
server = WSServer(server_address, server_port)
server.start()

signal.signal(signal.SIGINT, signal_handler)
while True:
    server.handle_clients()
    
    received_messages = server.get_received_messages()
    if received_messages:
        print("Messages reçus :", received_messages)
        for message in received_messages:
            if message == "PC":
                server.send_to_all_clients("Whisper")
            elif message.split(" #", 1)[0] =="PC Whisper":
                value = message.split(" #", 1)[1] # Resort l'analyse Whisper
                server.send_to_all_clients("Whisper data_recieved") # Met en pause Whisper
                nlu = MyTraductor.run(text=value)
    else:
        server.send_to_all_clients("ID")



        message = "PC Whisper #*musique*"
        parts = message.split("#", 1)  # Divise le message en deux parties en utilisant "#" comme délimiteur
        text_before_hash = parts[0]