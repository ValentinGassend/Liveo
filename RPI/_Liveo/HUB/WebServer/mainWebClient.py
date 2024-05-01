from webclient import WebSocketClient

client = WebSocketClient('http://192.168.1.16:3000/')
client.connect()
while True:
    if client.isConnected():
        # Vous pouvez placer d'autres actions ici avant d'envoyer un message
        client.send_message("This is my data")