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
        return "Ack failed"


class BLEISReadyState:

    def updatestate():
        pass

    def description():
        return "Ack failed"


class BLENotConnectedState:

    def updatestate():
        pass

    def description():
        return "Ack failed"


class BLEConnectedState:

    def updatestate():
        pass

    def description():
        return "Ack failed"
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

    def newAlertState(self, bleObj):
        pass
        # curState = bleObj.currentState()


class BLEAlertManager(AlertDelegate):

    def __init__(self, functionToCall):
        self.localFunctionToCall = functionToCall

    def newAlertState(self, bleObj):
        print(bleObj.description)
        # self.localFunctionToCall(bleObj.state)


def bleTrouble(bleState):
    print("Automatiser la correction")


bleAlertManager = BLEAlertManager(bleTrouble)
myBleObj = Ble(bleAlertManager)


class Ble:

    stateEmitingAlert = [BLENotConnectedState, BLEAckFaildeState]

    def __init__(self, alertDelegate, address="0C:B8:15:F8:6E:02", UUID_DATA='6e400002-b5a3-f393-e0a9-e50e24dcca9e'):
        self.DEVICE = address
        self.UUID_DATA = UUID_DATA
        self.connected = False
        self.adapter = BGAPIBackend()
        if len(sys.argv) == 2:
            self.DEVICE = str(sys.argv[1])
        # Run gatttool interactively.
        self.child = pexpect.spawn("gatttool -I")
        self.dataRecievedTimer = time()
        self.value = ''
        self.alertDelegate = alertDelegate
        self.state = BLENotConnectedState()

        # Connect to the self.DEVICE.

    def updatestate(self, newState):
        self.state = newState
        # ALERT si besoin
        if Ble.stateEmitingAlert.contains(newState)
        self.alertDelegate.newAlertState(self)

    def currentState(self):
        return state

    def check_connection(self):
        if not self.connected:
            NOF_REMAINING_RETRY = 3
            try:
                if not self.connected:
                    self.child.sendline("scan")
                    self.child.sendline("connect {0}".format(self.DEVICE))
                    self.child.expect("Connection successful")
            except pexpect.TIMEOUT:
                NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
                if (NOF_REMAINING_RETRY > 0):
                    self.updatestate(BLENotConnectedState())
                    self.connected = False
                else:
                    self.updatestate(BLENotConnectedState())
                    self.connected = False
            else:
                self.connected = True
                self.updatestate(BLEConnectedState())

        return self.connected

    def check_acknowledge(self):
        if self.connected:
            self.child.sendline("ACK")
            sleep(1)
            line = self.child.readline().decode("utf-8")
            if line == "ACK":
                print("ACK OK")
                self.updatestate(BLEAckSuccessState())
                return True
            else:
                print("ACK NOT OK")
                self.updatestate(BLEAckFaildeState())
                return False

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


myble = Ble()


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
        sleep(1)


def checkBLEIsReady(bleObj, nbTry=3):
    connectionState = checkBLEConnection(bleObj, nbTry)
    if connectionState == True:
        ackState = bleObj.check_acknowledge()
        return ackState
    else:
        return False


print("Testing BLE connection:")
bleIsReady = checkBLEIsReady(myble)


print("Testing motor")
