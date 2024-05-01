import pexpect
import time

class BLE:
    def __init__(self):
        self.child = pexpect.spawn("gatttool -I")
        self.DEVICE = "0C:B8:15:F8:6E:02"  # Replace with your device's MAC address
        self.connected = False
        self.line = ""

    def connect(self):
        if not self.connected:
            self.child.sendline("connect {}".format(self.DEVICE))
            try:
                self.child.expect("Connection successful", timeout=10)
                self.connected = True
                print("Connexion BLE établie.")
            except pexpect.exceptions.TIMEOUT:
                print("Échec de la connexion BLE.")

    def disconnect(self):
        if self.connected:
            self.child.sendline("disconnect")
            self.child.expect("disconnect successfully", timeout=60)
            self.connected = False
            print("BLE est maintenant déconnecté.")

    def send_message(self, message):
        if self.connected:
            encoded_message = message.encode("ascii").hex()
            self.child.sendline("char-write-req 0x0018 {}".format(encoded_message))
            try:
                self.child.expect("Characteristic value was written successfully", timeout=5)
                self.line = self.child.readline().decode()
                print("Message envoyé :", message)
            except pexpect.exceptions.TIMEOUT:
                print("Échec de l'envoi du message.")
                try:
                    self.disconnect()
                except:
                    pass
                self.connect()
                if self.connected:
                    self.send_message(message)
        else:
            print("Pas de connexion BLE établie. Tentative de connexion...")
            self.connect()
            if self.connected:
                encoded_message = message.encode("ascii").hex()
                self.child.sendline("char-write-req 0x0018 {}".format(encoded_message))
                try:
                    self.child.expect("Characteristic value was written successfully", timeout=5)
                    self.line = self.child.readline().decode()
                    print("Message envoyé :", message)
                except pexpect.exceptions.TIMEOUT:
                    print("Échec de l'envoi du message.")
                    try:
                        self.disconnect()
                    except:
                        pass
                    self.connect()

    def receive_message(self):
        if self.connected:
            self.line = self.child.readline().decode()
            if "value:" in self.line:
                    hex_data = self.line.split("value:")[1].strip()
                    byte_array = bytearray.fromhex(hex_data)
                    received_message = byte_array.decode("utf-8")
                    print("Message reçu :", received_message)
            else:
                print("Aucune notification reçue.")
        else:
            print("Pas de connexion BLE établie.")

    def check_connection(self):
        return self.connected


class State:
    def check_connection(self, ble):
        raise NotImplementedError()

    def check_acknowledge(self, ble):
        raise NotImplementedError()

    def launch(self, ble):
        raise NotImplementedError()

    def disconnect(self, ble):
        raise NotImplementedError()

    def write_data(self, ble):
        raise NotImplementedError()


class ConnectedState(State):
    def check_connection(self, ble):
        return True

    def check_acknowledge(self, ble):
        pass

    def launch(self, ble):
        print("BLE is already connected")

    def disconnect(self, ble):
        ble.child.sendline("disconnect")
        ble.child.expect("disconnect successfully", timeout=60)
        ble.connected = False
        ble.change_state(DisconnectedState())

    def write_data(self, ble):
        pass


class ConnectingState(State):
    def check_connection(self, ble):
        return False

    def check_acknowledge(self, ble):
        pass

    def launch(self, ble):
        print("BLE is already connecting")

    def disconnect(self, ble):
        ble.child.sendline("disconnect")
        ble.child.expect("disconnect successfully", timeout=60)
        ble.connected = False
        ble.change_state(DisconnectedState())

    def write_data(self, ble):
        pass


class DisconnectedState(State):
    def check_connection(self, ble):
        return False

    def check_acknowledge(self, ble):
        pass

    def launch(self, ble):
        ble.check_connection()
        ble.change_state(ConnectingState())

    def disconnect(self, ble):
        print("BLE is already disconnected")

    def write_data(self, ble):
        pass


def check_BLE_connection(ble_obj, nb_try=3):
    counter = 0
    launched = False
    while True:
        if counter >= nb_try:
            print("Connection Failed")
            return False
        if ble_obj.check_connection():
            print("Connected")
            return True
        counter += 1
        if not launched:
            ble_obj.launch()
            launched = True
        print("Failed, retry ({})".format(counter))


def check_BLE_is_ready(ble_obj, nb_try=3):
    connection_state = check_BLE_connection(ble_obj, nb_try)
    if connection_state:
        ack_state = ble_obj.check_acknowledge()
        return ack_state
    else:
        return False
