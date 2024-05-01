ble = bluetooth.BLE()
ble.active(True)

    # Création de l'objet BLE
ble_obj = Ble(ble)

while True:
    if ble_obj.get_value():
        received_data = ble_obj.get_value()
        message = received_data.strip()
        print("Message reçu :", message)

            # Vérifiez le contenu du message et répondez en conséquence
        if message == "Hello server!":
            response = "Hi client!"
        else:
            response = "Unknown command"

        ble_obj.send(response)  # Envoyer la réponse via BLE
        print("Message envoyé :", response)