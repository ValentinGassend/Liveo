import signal
import mfrc522
import RPi.GPIO as GPIO
import shlex
import subprocess
from time import sleep, time
import pexpect
import sys
from datetime import datetime
from pygatt.backends import BGAPIBackend
from binascii import hexlify
from time import time, sleep
# address of your self.DEVICE

# -----------------------
# -----------------------


class RFIDState:

    def updatestate():
        pass

    def description():
        pass


class RfidNotReadyState:

    def updatestate():
        pass

    def description():
        return "RFID detection doesn't work"


class RfidReadyState:

    def updatestate():
        pass

    def description():
        return "RFID is working"
# -----------------------
# -----------------------


class AlertDelegate:

    def newAlertState(self, rfidState):
        pass
        # curState = rfidObj.currentState()


class RFIDAlertManager(AlertDelegate):

    def __init__(self, functionToCall):
        self.localFunctionToCall = functionToCall

    def newAlertState(self, rfidState):
        rfidState.description
        self.localFunctionToCall(rfidState)


def rfidTrouble(rfidState):
    print("Automatiser la correction RFID")

################################################
# BRANCHEMENT DU LECTEUR RFID-RC522 sur le RPi #
################################################
    # SDA   xxxxxxxxxxxxxxxxxxxxx  24
    # SCK   xxxxxxxxxxxxxxxxxxxxx  23
    # MOSI  xxxxxxxxxxxxxxxxxxxxx  19
    # MISO  xxxxxxxxxxxxxxxxxxxxx  21
    # GND   xxxxxxxxxxxxxxxxxxxxx  6
    # RST   xxxxxxxxxxxxxxxxxxxxx  22
    # 3.3v  xxxxxxxxxxxxxxxxxxxxx  1


class Rfid_Trigger:

    stateEmitingAlert = [RfidNotReadyState]

    def __init__(self, alertDelegate, numDevice):
        self.MIFAREReader_first = mfrc522.MFRC522()
        self.numDevice = numDevice
        if self.numDevice==2:
            self.MIFAREReader_second = mfrc522.MFRC522(device=1)
        self.continue_reading = True
        self.discoverable = False
        self.started = None
        print("Welcome to the MFRC522 data read example")
        print("Press Ctrl-C to stop.")

        #----- here is my checker -----#
        signal.signal(signal.SIGINT, self.end_read)
        self.alertDelegate = alertDelegate
        self.state = RfidNotReadyState()

    def reset(self):
        self.continue_reading = True
        self.MIFAREReader_first = mfrc522.MFRC522()
        if self.numDevice==2:
            self.MIFAREReader_second = mfrc522.MFRC522(device=1)
        self.discoverable = False
        self.started = None

    def updatestate(self, newState):
        self.state = newState
        # ALERT si besoin
        for state in Rfid_Trigger.stateEmitingAlert:
            if state == type(newState):
                self.alertDelegate.newAlertState(newState)

    def currentState(self):
        return self.state

    def check_detection(self):

        while self.continue_reading:
            (status, TagType) = self.MIFAREReader_first.Request(
                self.MIFAREReader_first.PICC_REQIDL)

            if status == self.MIFAREReader_first.MI_OK:
                (status, raw_uid) = self.MIFAREReader_first.Anticoll()
                if status == self.MIFAREReader_first.MI_OK:
                    print(
                        "###################### Card detected ######################")
                    self.updatestate(RfidReadyState())
                    self.disconnected()
                    self.end_read()
                    self.reset()
                    card = True
            else:
                card = self.disconnected()
            return card
    def disconnected(self):
        self.updatestate(RfidNotReadyState())
        card = False

        return card
        
    def read(self):
        while self.continue_reading:
            (status_first, TagType) = self.MIFAREReader_first.Request(
                self.MIFAREReader_first.PICC_REQIDL)
            (status_second, TagType) = self.MIFAREReader_second.Request(
                self.MIFAREReader_first.PICC_REQIDL)
            if (status_first == self.MIFAREReader_first.MI_OK):
                (status_first, raw_uid) = self.MIFAREReader_first.Anticoll()
                self.started = time()
                if status_first == self.MIFAREReader_first.MI_OK:
                    if self.discoverable == False:
                        print(
                            "###################### Card detected on 1 ######################")
                        self.discoverable = True
            else:
                if (status_second == self.MIFAREReader_second.MI_OK):
                    (status_second, raw_uid) = self.MIFAREReader_second.Anticoll()
                    self.started = time()
                    if status_second == self.MIFAREReader_second.MI_OK:
                        if self.discoverable == False:
                            print(
                                "###################### Card detected on 2 ######################")
                            self.discoverable = True
                if self.discoverable:
                    if self.started == None:
                        self.started = time()
                    duration = time() - self.started
                    if duration > 25:
                        print(
                            "###################### Card removed ######################")
                        self.discoverable = False
                        self.started = time()
                        self.end_read()
            return self.discoverable

    def end_read(self, signal=None, frame=None):
        if self.continue_reading:
            print("\nCtrl+C captured, ending read.")
            self.continue_reading = False
            GPIO.cleanup()
            self.reset()
        else:
            print("\nAlready Stopped, shutting down terminal")
            sys.exit()


def checkRFIDIsReady(rfidObj, nbTry=3, delay = 5):
    counter = 0
    while (True):
        if counter >= nbTry:
            print("Connection Failed")
            return False
        if rfidObj.check_detection():
            print("Connected")
            rfidObj.disconnected()
            ("disconnected of validated connexion")
            return True
        counter += 1
        print("Failed, retry ({})".format(counter))
        sleep(delay)


# RFIDAlertManager = RFIDAlertManager(rfidTrouble)
# myrfidObj = Rfid_Trigger(RFIDAlertManager)


# print("Testing RFID detection :")
# rfidIsReady = checkRFIDIsReady(myrfidObj, 5)
