import pexpect
import sys
from datetime import datetime
from pygatt.backends import BGAPIBackend
from binascii import hexlify
from time import time, sleep
# address of your self.DEVICE

# -----------------------
# -----------------------


class BLEState:

    def updatestate():
        pass

    def description():
        pass


class BLEAckFaildeState:

    def updatestate():
        pass

    def description():
        return "Ack failed"


class BLEAckSuccessState:

    def updatestate():
        pass

    def description():
        return "Ack Success"


class BLEISReadyState:

    def updatestate():
        pass

    def description():
        return "Ble is ready"


class BLENotConnectedState:

    def updatestate():
        pass

    def description():
        return "Ble is not connected"


class BLEConnectedState:

    def updatestate():
        pass

    def description():
        return "Ble is connected"
# -----------------------
# -----------------------


# -----------------------
# -----------------------
class DistanceSensorState:

    def updatestate():
        pass

    def description():
        pass


class SensorIsReadyState:

    def updatestate():
        pass

    def description():
        return "Ack failed"


class UnpluggedSensorState:

    def updatestate():
        pass

    def description():
        return "Ack failed"

# -----------------------
# -----------------------


class AlertDelegate:

    def newAlertState(self, bleState):
        pass
        # curState = bleObj.currentState()


class BLEAlertManager(AlertDelegate):

    def __init__(self, functionToCall):
        self.localFunctionToCall = functionToCall

    def newAlertState(self, bleState):
        bleState.description
        self.localFunctionToCall(bleState)


def bleTrouble(bleState):
    print(type(bleState))
    print("Automatiser la correction BLE")


class Ble:

    stateEmitingAlert = [BLENotConnectedState,
                         BLEAckFaildeState, BLEAckSuccessState]

    def __init__(self, alertDelegate, address="0C:B8:15:F8:6E:02", UUID_DATA='6e400002-b5a3-f393-e0a9-e50e24dcca9e'):
        self.DEVICE = address
        self.UUID_DATA = UUID_DATA
        self.connected = False
        self.adapter = BGAPIBackend()
        if len(sys.argv) == 2:
            self.DEVICE = str(sys.argv[1])
        # Run gatttool interactively.
        self.child = pexpect.spawn("gatttool -I", timeout=5)
        self.dataRecievedTimer = time()
        self.value = ''
        self.alertDelegate = alertDelegate
        self.state = BLENotConnectedState()

        # Connect to the self.DEVICE.

    def updatestate(self, newState):
        self.state = newState
        # ALERT si besoin
        for state in Ble.stateEmitingAlert:
            if state == type(newState):
                self.alertDelegate.newAlertState(newState)

    def currentState(self):
        return self.state

    def check_connection(self):
        if not self.connected:
            NOF_REMAINING_RETRY = 3
            try:
                if not self.connected:
                    self.child.sendline("scan")
                    self.child.sendline("connect {0}".format(self.DEVICE))
                    self.child.expect("Connection successful")
            except pexpect.TIMEOUT:
                self.connected = False
                self.updatestate(BLENotConnectedState())
            else:
                self.connected = True
                self.updatestate(BLEConnectedState())

        return self.connected

    def check_acknowledge(self):
        if self.connected:
            try:
                self.child.sendline("char-write-req 0x0018 '20'")
                self.child.expect(
                    "Characteristic value was written successfully")
            except:
                print("ACK NOT OK")
                self.updatestate(BLEAckFaildeState())
                return False

            else:
                print("ACK OK")
                self.updatestate(BLEAckSuccessState())
                return True

    def lunch(self):
        if not self.connected:
            print("Connecting to:"),
            print(self.DEVICE)
            NOF_REMAINING_RETRY = 3
            try:
                if not self.connected:
                    self.child.sendline("scan")
                    self.child.sendline("connect {0}".format(self.DEVICE))
                    self.child.expect("Connection successful")
            except pexpect.TIMEOUT:
                NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
                if (NOF_REMAINING_RETRY > 0):
                    print("timeout, retry...")
                    self.connected = False
                else:
                    print("timeout, giving up.")
                    self.connected = False
            else:
                print("Connected!")
                self.connected = True
                self.dataRecievedTimer = time()
        else:
            try:
                line = self.child.readline().decode("utf-8")
                if line.split("value:"):
                    array = line.split("value:", 1)
                if len(array) > 1:
                    for i in array[1].split():
                        self.value += chr(int(i, 16))

            except:
                pass

            if self.value:
                print(self.value)
                Date = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                file = open('cache.txt', 'w')
                file.write(self.value)
                print("error for retrieve information")

            # pass


def checkBLEConnection(bleObj, nbTry=3):
    counter = 0
    while (True):
        if counter >= nbTry:
            print("Connection Failed")
            return False
        if bleObj.check_connection():
            print("Connected")
            return True
        counter += 1
        print("Failed, retry ({})".format(counter))
        sleep(1/10)


def checkBLEIsReady(bleObj, nbTry=3):
    connectionState = checkBLEConnection(bleObj, nbTry)
    if connectionState == True:
        ackState = bleObj.check_acknowledge()
        return ackState
    else:
        return False


bleAlertManager = BLEAlertManager(bleTrouble)
myBleObj = Ble(bleAlertManager)


print("Testing BLE connection:")
bleIsReady = checkBLEIsReady(myBleObj, 5)
