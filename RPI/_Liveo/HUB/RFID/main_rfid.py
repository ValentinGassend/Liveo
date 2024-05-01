from rfid import RfidTrigger

rfid_trigger = RfidTrigger(numDevice=2)

while True:
    rfid_trigger.read()  # This will run indefinitely
    card_state = rfid_trigger.get_state()
    print(card_state)

    if card_state:
        # Lancer le Bluetooth uniquement lorsque l'état de la carte passe à True
        print("Running BLE")
        # Code pour lancer le Bluetooth
        # ...

        # Attendre que l'état de la carte passe à False
        while card_state:
            rfid_trigger.read()
            card_state = rfid_trigger.get_state()

    else:
        # Vérifier la valeur du bouton et l'heure
        # ...
        print("Button value:")
        print("Current time:")

