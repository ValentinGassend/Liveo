

class Rfid_BLE_manager:
    def __init__(self, numDevice=1):
        from rfid_and_BLE.BLE_luncher.better_ble import Ble, BLEAlertManager, bleTrouble, checkBLEIsReady
        from rfid_and_BLE.rfid_RPI.better_rfid import Rfid_Trigger, RFIDAlertManager, rfidTrouble, checkRFIDIsReady
        RFIDAlertManager = RFIDAlertManager(rfidTrouble)
        self.rfid = Rfid_Trigger(RFIDAlertManager, numDevice)
        self.myBle = Ble(BLEAlertManager)
        myrfidObj = self.rfid
        print("Testing RFID detection :")
        self.rfidIsReady = checkRFIDIsReady(myrfidObj, 25)
        if not self.rfidIsReady:
            print("RFID IS NOT READY")

    def lunch(self):
        if self.checkRFIDDetection():
            self.myBle.lunch()

    def checkRFIDDetection(self):
        return self.rfid.read()

    def checkResult(self):
        return True
        # return self.rfidIsReady


# MyManager = Rfid_BLE_manager()


# __________________________ #
# __________________________ #


# bleAlertManager = BLEAlertManager(bleTrouble)
# myBleObj = Ble(bleAlertManager)


# print("Testing BLE connection:")
# bleIsReady = checkBLEIsReady(myBleObj, 5)


# RFIDAlertManager = RFIDAlertManager(rfidTrouble)
# myrfidObj = Rfid_Trigger(RFIDAlertManager)


# print("Testing RFID detection :")
# rfidIsReady = checkRFIDIsReady(myrfidObj, 5)


# __________________________ #
# __________________________ #


# while True:
#     MyManager.lunch()
#
