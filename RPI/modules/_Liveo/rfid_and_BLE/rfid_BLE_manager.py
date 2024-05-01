# Importations
from rfid_and_BLE.BLE_luncher.better_ble import Ble
from rfid_and_BLE.rfid_RPI.better_rfid import RfidTrigger, RFIDAlertManager, rfid_trouble, check_rfid_is_ready

class Rfid_BLE_manager:
    def __init__(self, numDevice=1):
        self.RFIDAlertManager = RFIDAlertManager(rfid_trouble)
        self.rfid = RfidTrigger(self.RFIDAlertManager, numDevice)
        self.myBle = Ble()
        myrfidObj = self.rfid
        print("Testing RFID detection:")
        
    def lunch(self):
        if self.rfid.read() and not self.myBle.lunch():
            self.myBle.lunch()
        if not self.rfid.read():
            # Appelle la méthode appropriée pour écrire les données BLE
            self.myBle.write_data()

    def checkResult(self):
        # Vérifie l'état actuel du RFID et met à jour self.rfidIsReady
        self.rfidIsReady = check_rfid_is_ready(self.rfid, 5)
        return self.rfidIsReady
