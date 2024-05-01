from time import sleep
import random
import struct
import time
from wireless_manager import *

    

class WebsocketCallback(CommunicationCallback):

    def __init__(self):
        pass
    
    def connectionCallback(self):
        print("Connected")
    
    def disconnectionCallback(self):
        print("Disconected")
    
    def didReceiveCallback(self,value):
        print(f"Received {value}")
        
    
wirelessManager = WirelessManager(WebsocketCallback())

try:
    while True:
        wirelessManager.process()
        sleep(0.1)
        wirelessManager.sendDataToWS("Hoho WS")
            
except KeyboardInterrupt:
    pass
#server.stop()