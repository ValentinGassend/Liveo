# Import des classes et fonctions nécessaires
from Websocket.WebsocketManager import WSClient
from Led_Strip.led import LedMode

# Adresse et port du serveur WebSocket
server_address = '192.168.1.16'
server_port = 8081
from rpi_ws281x import Color
# Création d'une instance du client WebSocket
websocket_client = WSClient(server_address, server_port, "LED")
LedManager = LedMode()
# Connexion au serveur WebSocket
websocket_client.connect()

# Boucle principale du client
while True:
    # Envoi d'un message au serveur WebSocket pour demander le mode de LED actuel
    # websocket_client.send_message('LED_MODE')

    # Réception de la réponse du serveur WebSocket
    response = websocket_client.receive_message()
    print('Mode de LED actuel :', response)
    if not response =="LED_static_2":
        LedManager.handle_message(response)
    else :
        LedManager.handle_message(response,2)

    # Pause entre chaque vérification du mode de LED
    # time.sleep(1)

# Fermeture de la connexion au serveur WebSocket
websocket_client.close()
