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

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = mfrc522.MFRC522()

# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")
discoverable = False
started=None
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    sleep(1/10)
    # Scan for cards    
    # (status,TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    # if status == MIFAREReader.MI_OK:
    #     if discoverable==False:
    #         print ("Card detected")
    #         subprocess.Popen(["sudo","bluetoothctl","discoverable","on"])
    #         subprocess.Popen(["sudo","bluetoothctl","connect","0C:B8:15:F8:6E:02"])
    #         discoverable=True
    # else :
    #     if discoverable :
    #         subprocess.Popen(["sudo","bluetoothctl","discoverable","off"])
    #         subprocess.Popen(["sudo","bluetoothctl","disconnect","0C:B8:15:F8:6E:02"])
    #         discoverable=False
    # Get the UID of the card
    # If we have the UID, continue
    # if status == MIFAREReader.MI_OK:

    #     # Print UID
    #     print ("Card read UID:"+ str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]))
    
    #     # This is the default key for authentication
    #     key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    #     myCard = [220,118,215,56,69]
    #     if uid == myCard:
    #         print("this is the good card")

        
    #     # Select the scanned tag
    #     MIFAREReader.SelectTag(uid)

    #     # Authenticate
    #     status = MIFAREReader.Authenticate(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

    #     # Check if authenticated
    #     if status == MIFAREReader.MI_OK:
    #         MIFAREReader.ReadTag(8)
    #         MIFAREReader.StopCrypto1()
    #     else:
    #         print ("Authentication error")
    (status,TagType) = MIFAREReader.Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        (status, raw_uid) = MIFAREReader.Anticoll()
        started=time()
        if status == MIFAREReader.MI_OK:
            if discoverable==False:
                print ("###################### Card detected ######################")
                discoverable=True
                
    else :
        
        if discoverable :
            if started==None:
                started=time()
            duration = time() - started
            if duration>2:
                print ("###################### Card removed ######################")
                discoverable=False
                started=time()
