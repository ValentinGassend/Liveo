# myESP32button = button(23)
# while True:
#     myESP32button.status()
#     sleep_ms(100)



# ble = bluetooth.BLE()
# p = Ble(ble,name="MemoRoom")
# while True:
#     p.on_write(p.on_rx)

from esp32_RFID_BLE_sendfile.RFID_ESP32.main import RFID
import esp32_RFID_BLE_sendfile.RFID_ESP32.libs.mfrc522 as mfrc522
from esp32_RFID_BLE_sendfile.BLE_ESP32.main_bluetooth import Ble
import bluetooth
from machine import Pin
from time import time
class RFID_BLE_manager:
    def __init__(self):
        self.rdr = mfrc522.MFRC522(5, 17, 16, 4, 18)
        self.MyRfid = RFID(self.rdr)
        self.ble = bluetooth.BLE()
        self.ble_started = False
        self.p = None
        self.dataSended = False
        self.DataTimeStarted = False

    def run(self):
        if self.p:
            self.p.on_write(self.p.on_rx)
            if self.p.is_connected():
                
                return True
            else:
                self.DataTimeStarted=False
                self.dataSended = False
                self.p = None
                return False            
        else:
            self.DataTimeStarted=False
            self.dataSended = False

            if self.MyRfid.read():
                print("reading")
                if not self.ble_started:
                    self.p = Ble(self.ble,name="LiveoESP")
                    self.ble_started = True
                else:
                    pass
            else:
                pass
    #     p.on_write(p.on_rx)
    
    
    def disconnected(self):
        self.ble.active()
        if self.p:
            if self.p.is_connected():
                self.p=None
                self.ble_started = False
                print("disconnected")
        
    def send(self, data):
        if self.p:
            if self.p.is_connected():
                self.p.send(data)
                print("data sended")
        else:
            print("Ble is not connected")
            
    def recieved(self, data):
        if self.p:
            if self.p.getvalue():
                if  self.p.getvalue() == data:
                    return True
            
            
        