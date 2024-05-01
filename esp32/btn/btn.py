from machine import Pin
from time import time


class button:
    def __init__(self, buttonPin):
        self.currentState=False
        self.button = Pin(buttonPin,Pin.IN)
        self.lastState = False
        self.pushType=None
        self.long=False
        self.startedTime=None
        self.lunched=False
        self.enable = True
    def status(self):
        if self.button.value() == 1:
            self.pressedType()
            if self.pressedType() and self.enable:
                self.enable = False 
                return self.pressedType()
        else:
            self.startedTime=None
            self.long=False
            self.lunched=False
            self.enable = True 


    def pressedType(self):
        if self.startedTime==None:
            self.startedTime=time()
        else:
            pressedTime = time()-self.startedTime
#         temps de pression du bouton
            if not pressedTime < 2:
                if not self.lunched:
                    self.long = True
                    self.lunched = True
            return self.long
        
        
    def isPushed(self):
        if self.button.value() == 1:
            return True
        else:
            return False
#         
# myButton = button(23)
# 
# while True:
#     print(Pin(23,Pin.IN).value())