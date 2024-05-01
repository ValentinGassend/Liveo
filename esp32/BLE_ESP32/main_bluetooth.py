import bluetooth
import time
from BLE_ESP32.ble_simple_peripheral import BLESimplePeripheral

class Ble(BLESimplePeripheral):
    def __init__(self, ble, name="mpy-uart"):
        super().__init__(ble, name)
        self.value = False
        self.connected = False  # Ajoute l'attribut connected
        self.response = None  # Variable pour stocker la réponse

    def on_rx(self, v):
        message = v.decode()  # Décode les octets en utilisant l'encodage UTF-8
        print("Message reçu :", message)
        self.value = message

    def get_value(self):
        sended_value = self.value
        if sended_value:
            self.value = False  # Réinitialise la valeur
            return sended_value

    def is_connected(self):
        return self.connected
    
    def on_connect(self, client_config):
        self.connected = True
    
    def on_disconnect(self, client_config):
        self.connected = False

ble = bluetooth.BLE()
ble_obj = Ble(ble)
ble_obj.on_write(ble_obj.on_rx)
while True:
    received_data = ble_obj.get_value()
    if received_data:
        message = received_data.strip()
        print("Message reçu :", message)
        time.sleep(0.1)
        # Vérifiez le contenu du message et répondez en conséquence
        if message == "Hello server!":
            ble_obj.response = "Hi client!"  # Stocke la réponse dans la variable
        else:
            ble_obj.response = "Unknown command"

        if ble_obj.response is not None:
            ble_obj.send(ble_obj.response)  # Envoie la réponse via BLE
            print("Réponse envoyée :", ble_obj.response)
            ble_obj.response = None  # Réinitialise la variable de réponse
    
    if ble_obj.is_connected():
        # Attendez un court instant avant d'envoyer un message
        time.sleep(0.1)
        message = "Server message"
        print("Message envoyé :", message)
        ble_obj.send(message.encode())  # Envoyer un message au client connecté
