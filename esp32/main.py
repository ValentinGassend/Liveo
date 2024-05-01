from esp32_RFID_BLE_sendfile.RFID_and_BLE import RFID_BLE_manager
from led.led import Led
from led.single_led import SingleLed
from KeepMind.fileManager import keepMinder
from btn.btn import button



from machine import Pin
from time import time
import utime

MyRFID_BLE_manager = RFID_BLE_manager()
MyFileManager = keepMinder("hasard.txt")
myButton = button(23)
blue = Pin(27, Pin.OUT)
green = Pin(14, Pin.OUT)
red = Pin(26, Pin.OUT)
Myled = Led(blue,green,red)

single_green = Pin(13, Pin.OUT)
MySingleled = SingleLed(single_green)

delay_ms = 1000  # 1 second delay in milliseconds
start_time = utime.ticks_ms()

dataSended = False
dataSupossedSend = False
DataTimeStarted = False
ledTimerStarter=time()
Myled.off()
MySingleled.off()

while True:    
    is_pushed = myButton.isPushed()
    if not is_pushed:
        if MyRFID_BLE_manager.run():
            if not dataSended:
                    if MyRFID_BLE_manager.recieved("disconnect"):
                        MyRFID_BLE_manager.send("disconnect successfully")
                        dataSupossedSend=False
                        dataSended=True
                        MyRFID_BLE_manager.disconnected()
                    if MyRFID_BLE_manager.recieved("Hello"):
                        MyRFID_BLE_manager.send('Hi !')
                        MyFileManager.reset()
                        dataSended=True
                        ledTimerStarter = time()
                        MyRFID_BLE_manager.disconnected()
                    if MyRFID_BLE_manager.recieved("RPI-Liveo") and not dataSupossedSend:
                        content = MyFileManager.read()
    #                     Myled.on_green()
                    
                        start_time = utime.ticks_ms()
                        while utime.ticks_diff(utime.ticks_ms(), start_time) <delay_ms:
                            pass
                        MyRFID_BLE_manager.send("10")
#                         MyRFID_BLE_manager.send(content)
                        dataSupossedSend = True
                        
                    if dataSupossedSend:
                        if MyRFID_BLE_manager.recieved("Data-notOK"):
                            datasupossedSend = False
                        if MyRFID_BLE_manager.recieved("Data-ok"):
                            MyFileManager.reset()
                            dataSupossedSend=False
                            dataSended=True
                            MyRFID_BLE_manager.disconnected()
                        
                        
        else:           
            dataSended = False
            
    
    if myButton.status():
#         Myled.off()
        MySingleled.off()
        actualData = MyFileManager.read()
        print(actualData)
        if not actualData or actualData == "":
            newData = 1
        else:
            int(actualData)
            newData = int(actualData) + 1
        MyFileManager.write(newData)
#         Myled.on_green()
        MySingleled.on()
        ledTimerStarter = time()
    else :
#         temps de led active
        if (time()-ledTimerStarter)>1:
#             Myled.off()
            MySingleled.off()

 