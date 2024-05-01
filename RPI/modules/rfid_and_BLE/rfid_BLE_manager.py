from BLE_luncher.better_ble import Ble, BLEAlertManager, bleTrouble, checkBLEIsReady
from rfid_RPI.better_rfid import Rfid_Trigger, RFIDAlertManager, rfidTrouble, checkRFIDIsReady


class Rfid_BLE_manager:
    def __init__(self):
        self.rfid = Rfid_Trigger()
        self.myBle = Ble()

    def lunch(self):
        self.rfid.read()
        if self.rfid.read() and not self.myBle.lunch():
            self.myBle.lunch()


MyManager = Rfid_BLE_manager()


# __________________________ #
# __________________________ #


# bleAlertManager = BLEAlertManager(bleTrouble)
# myBleObj = Ble(bleAlertManager)


print("Testing BLE connection:")
# bleIsReady = checkBLEIsReady(myBleObj, 5)


# RFIDAlertManager = RFIDAlertManager(rfidTrouble)
# myrfidObj = Rfid_Trigger(RFIDAlertManager)


print("Testing RFID detection :")
# rfidIsReady = checkRFIDIsReady(myrfidObj, 5)


# __________________________ #
# __________________________ #


# while True:
#     MyManager.lunch()
