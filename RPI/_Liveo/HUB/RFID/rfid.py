
import signal
import mfrc522
import RPi.GPIO as GPIO
import shlex
import subprocess
from time import time
import pexpect
import sys
from datetime import datetime
from pygatt.backends import BGAPIBackend
from binascii import hexlify

class RFIDState:
    def __init__(self):
        self.description = ""

    def update_state(self, rfid_trigger):
        pass

class RfidNotReadyState(RFIDState):
    def __init__(self):
        super().__init__()
        self.description = "RFID detection doesn't work"

    def update_state(self, rfid_trigger):
        rfid_trigger.update_state(self)

class RfidReadyState(RFIDState):
    def __init__(self):
        super().__init__()
        self.description = "RFID is working"

    def update_state(self, rfid_trigger):
        rfid_trigger.update_state(self)

import mfrc522
import RPi.GPIO as GPIO
from time import time


class RfidTrigger:
    def __init__(self, numDevice):
        self.MIFAREReader_first = mfrc522.MFRC522()
        self.numDevice = numDevice
        if self.numDevice == 2:
            self.MIFAREReader_second = mfrc522.MFRC522(device=1)
        else:
            self.MIFAREReader_second = None
        self.discoverable = False
        self.started = None
        self.state = False

    def read(self):
        (status_first, TagType) = self.MIFAREReader_first.Request(self.MIFAREReader_first.PICC_REQIDL)
        if self.MIFAREReader_second is not None:
            (status_second, TagType) = self.MIFAREReader_second.Request(self.MIFAREReader_first.PICC_REQIDL)

        if (status_first == self.MIFAREReader_first.MI_OK):
            (status_first, raw_uid) = self.MIFAREReader_first.Anticoll()
            self.started = time()
            if status_first == self.MIFAREReader_first.MI_OK:
                if self.discoverable == False:
                    print("###################### Card detected on 1 ######################")
                    self.discoverable = True
                    self.state = True
        else:
            if self.MIFAREReader_second is not None and (status_second == self.MIFAREReader_second.MI_OK):
                (status_second, raw_uid) = self.MIFAREReader_second.Anticoll()
                self.started = time()
                if status_second == self.MIFAREReader_second.MI_OK:
                    if self.discoverable == False:
                        print("###################### Card detected on 2 ######################")
                        self.discoverable = True
                        self.state = True
        if self.discoverable:
            if self.started is None:
                self.started = time()
            duration = time() - self.started
            if duration > 1:
                print("###################### Card removed ######################")
                self.discoverable = False
                self.started = time()
                self.state = False

    def get_state(self):
        return self.state

    def reset(self):
        print("Resetting RFID...")
        self.state = False