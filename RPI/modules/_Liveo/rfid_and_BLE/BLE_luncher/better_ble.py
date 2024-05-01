import pexpect
import sys
from datetime import datetime
from pygatt.backends import BGAPIBackend
from binascii import hexlify
from time import time, sleep
from TTS.tts import TTS

# -----------------------
# -----------------------

class BLEState:
    def updatestate(self):
        pass

    def description(self):
        pass

class BLEAckFaildeState(BLEState):
    def updatestate(self):
        pass

    def description(self):
        return "Ack failed"

class BLEAckSuccessState(BLEState):
    def updatestate(self):
        pass

    def description(self):
        return "Ack Success"

class BLEISReadyState(BLEState):
    def updatestate(self):
        pass

    def description(self):
        return "Ble is ready"

class BLENotConnectedState(BLEState):
    def updatestate(self):
        pass

    def description(self):
        return "Ble is not connected"

class BLEConnectedState(BLEState):
    def updatestate(self):
        pass

    def description(self):
        return "Ble is connected"

# -----------------------
# -----------------------

# -----------------------
# -----------------------

class DistanceSensorState:
    def updatestate(self):
        pass

    def description(self):
        pass

class SensorIsReadyState(DistanceSensorState):
    def updatestate(self):
        pass

    def description(self):
        return "Ack failed"

class UnpluggedSensorState(DistanceSensorState):
    def updatestate(self):
        pass

    def description(self):
        return "Ack failed"

# -----------------------
# -----------------------

class Ble:
    def __init__(self):
        self.state = BLEISReadyState()
        self.connection = None
        self.tts = TTS()

    def read_data(self):
        if self.state.description() == "Ble is connected":
            pass  # Ajoutez le code pour lire les données BLE

    def write_data(self):
        if self.state.description() == "Ble is connected":
            pass  # Ajoutez le code pour écrire les données BLE

    def lunch(self):
        if self.state.description() == "Ble is connected":
            pass  # Ajoutez le code pour envoyer le signal "Lunch" via BLE

    def checkBLEConnection(self):
        if self.connection:
            self.state = BLEConnectedState()
        else:
            self.state = BLENotConnectedState()

    def checkBLEIsReady(self):
        if self.state.description() == "Ble is ready":
            return True
        else:
            return False

# -----------------------
# -----------------------

def checkBLEConnection(bleObj, timeout):
    start_time = time()
    while (time() - start_time) < timeout:
        bleObj.checkBLEConnection()
        if bleObj.state.description() == "Ble is connected":
            return True
        sleep(1)
    return False

def checkBLEIsReady(bleObj, timeout):
    start_time = time()
    while (time() - start_time) < timeout:
        if bleObj.checkBLEIsReady():
            return True
        sleep(1)
    return False

# -----------------------
# -----------------------

def bleTrouble(msg):
    print(f"Ble Trouble: {msg}")
