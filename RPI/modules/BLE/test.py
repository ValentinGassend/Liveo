import pygatt

# Adresse MAC du périphérique ESP32
# Remplacez par l'adresse MAC de votre ESP32
ESP32_MAC_ADDRESS = '0C:B8:15:F8:6E:02'

# UUID de la caractéristique Bluetooth
CHARACTERISTIC_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'

# Création de l'objet de connexion Bluetooth
adapter = pygatt.GATTToolBackend()

try:
    adapter.start()

    # Connexion au périphérique ESP32
    device = adapter.connect(ESP32_MAC_ADDRESS)

    # Lecture de la valeur de la caractéristique Bluetooth
    value = device.char_read(CHARACTERISTIC_UUID)
    print("Valeur lue :", value.decode())

    # Écriture d'une valeur sur la caractéristique Bluetooth
    device.char_write(CHARACTERISTIC_UUID, bytearray(b"Hello, ESP32!"))

finally:
    adapter.stop()
