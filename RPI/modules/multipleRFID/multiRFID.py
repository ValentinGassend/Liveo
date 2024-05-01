import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev

class NFC():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.close()
        self.bus = bus
        self.boards = {}
        
        self.device = device
        self.spd = spd

    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        # self.reader.READER.SimpleMFRC522()

    def close(self):
        self.reader.READER.spi.close()

    def addBoard(self, rid, pin):
        self.boards[rid] = pin

    def selectBoard(self, rid):
        if not rid in self.boards:
            print("readerid " + rid + " not found")
            return False

        for loop_id in self.boards:
            print(rid)
            print(self.boards[loop_id])
            if self.boards[loop_id]==6:
                value = 31
            if self.boards[loop_id]==5:
                value = 29
            GPIO.setup(value, GPIO.OUT)
            GPIO.setwarnings(False)
            GPIO.output(value, GPIO.HIGH)
        return True

    def read(self, rid):
        if not self.selectBoard(rid):
            return None

        self.reinit()
        cid, val = self.reader.read_no_block()
        self.close()

        return val

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True


if __name__ == "__main__":
    nfc = NFC()
    nfc.addBoard("reader1",5)
    nfc.addBoard("reader2",6)

    data = nfc.read("reader1")
    print("data = " + str(data))
    nfc.write("reader2",data)