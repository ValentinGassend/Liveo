import websocket

address = '192.168.1.16'
port = 8081

def on_message(ws, message):
    print(f"Message reçu : {message}")

def on_error(ws, error):
    print(f"Erreur : {error}")

def on_close(ws):
    print("Connexion WebSocket fermée")

def on_open(ws):
    print("Connexion WebSocket ouverte")
    ws.send("ID")

websocket.enableTrace(True)
ws = websocket.WebSocketApp(f"ws://{address}:{port}/",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open(ws)
ws.run_forever()
