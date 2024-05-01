#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#
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





from time import sleep, time
import subprocess
import shlex
import RPi.GPIO as GPIO
import mfrc522
import signal
import sys


class Rfid_Trigger :
    def __init__(self):    
        self.continue_reading = True
        self.MIFAREReader = mfrc522.MFRC522()
        self.discoverable = False
        self.started=None
        print ("Welcome to the MFRC522 data read example")
        print ("Press Ctrl-C to stop.")
        signal.signal(signal.SIGINT, self.end_read)
    
    def read(self):
        while self.continue_reading:
            (status,TagType) = self.MIFAREReader.Request(self.MIFAREReader.PICC_REQIDL)
            if status == self.MIFAREReader.MI_OK:
                (status, raw_uid) = self.MIFAREReader.Anticoll()
                self.started=time()
                if status == self.MIFAREReader.MI_OK:
                    if self.discoverable==False:
                        print ("###################### Card detected ######################")
                        self.discoverable=True
            else :
                
                if self.discoverable :
                    if self.started==None:
                        self.started=time()
                    duration = time() - self.started
                    if duration>25:
                        print ("###################### Card removed ######################")
                        self.discoverable=False
                        self.started=time()
            return self.discoverable

    def end_read(self,signal=None,frame=None):

        if self.continue_reading :
            print ("\nCtrl+C captured, ending read.")
            self.continue_reading = False
            GPIO.cleanup()
        else:
            print("\nAlready Stopped, shutting down terminal")
            sys.exit()
