from ble import BLE, check_BLE_is_ready, ConnectedState, ConnectingState, DisconnectedState

ble_client = BLE()

# Connexion BLE
ble_client.connect()

# Envoi d'un message au serveur
message = "Hello server!"
  # Envoi initial du message

while True:
    ble_client.check_connection()  # Vérifie la connexion BLE
    ble_client.send_message(message)
    received_message = ble_client.receive_message()
    if received_message is not None:
        # Process the received message here
        print("Received message:", received_message)

    # Effectue d'autres opérations ici
