import bluetooth
import random
import struct
import time
from esp32_RFID_BLE_sendfile.BLE_ESP32.ble_advertising import advertising_payload
from esp32_RFID_BLE_sendfile.BLE_ESP32.ble_simple_peripheral import *
from micropython import const

class Ble(BLESimplePeripheral):
    def __init__ (self, ble, name="mpy-uart"):
        super().__init__(ble, name)
        self.value = False
    def on_rx(self,v):
        print(type(v))
        print(v)
        self.value = v.decode()
        print(v.decode())
    
    def getvalue(self):
        sendedvalue = self.value
        if sendedvalue:
            return sendedvalue
        self.value = False
        
# p.is_connected()
# p.send(data)