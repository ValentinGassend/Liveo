import pexpect
import sys
from datetime import datetime
from pygatt.backends import BGAPIBackend
from binascii import hexlify
from time import time, sleep
# address of your self.DEVICE


class Ble:
    def __init__(self, address="0C:B8:15:F8:6E:02", UUID_DATA='6e400002-b5a3-f393-e0a9-e50e24dcca9e'):
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
                try:
                    self.child.sendline(b'Hello')
                    line = self.child.readline().decode("utf-8")
                    if line.split("value:"):
                        array = line.split("value:", 1)
                    if len(array) > 1:
                        for i in array[1].split():
                            self.value += chr(int(i, 16))
                            print()

                except:
                    pass

                if self.value:
                    print(self.value)
                    Date = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
                    file = open('Hub/cache.txt', 'w')
                    file.write(self.value)
                    print("error for retrieve information")
        else:
            pass
            

#             # pass
# Myble = Ble()

# print(Myble.check_connection())
# sleep(3)
# print(Myble.check_knowledge())
