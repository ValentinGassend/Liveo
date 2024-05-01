import RPi.GPIO as GPIO
import time
class Btn:
    def __init__(self, buttonPin):
        self.buttonPin = buttonPin
        self.pressed = False
        self.startedTime = None
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def checking_state(self):
        if self.pressed == False:
            self.startedTime = time.time()
            input_state = GPIO.input(self.buttonPin)
            if input_state == 0:
                print('Button Pressed')
                self.pressed=True
        if time.time()-self.startedTime > 5:
            self.pressed=False

Mybtn = Btn(10)
while True:
    Mybtn.checking_state()




# while True:
#     input_state = GPIO.input(18)
#     if input_state == False:
#         print('Button Pressed')
#         time.sleep(0.2)
# class button:
#     def __init__(self, buttonPin):
#         self.currentState=False
#         self.button = Pin(buttonPin,Pin.IN)
#         self.lastState = False
#         self.pushType=None
#         self.long=False
#         self.startedTime=None
#         self.lunched=False
#         self.enable = True
#     def status(self):
#         if self.button.value() == 0:
#             self.pressedType()
#             if self.pressedType() and self.enable:
#                 self.enable = False 
#                 return self.pressedType()
#         else:
#             self.startedTime=None
#             self.long=False
#             self.lunched=False
#             self.enable = True 


#     def pressedType(self):
#         if self.startedTime==None:
#             self.startedTime=time()
#         else:
#             pressedTime = time()-self.startedTime
# #         temps de pression du bouton
#             if not pressedTime < 3:
#                 if not self.lunched:
#                     self.long = True
#                     self.lunched = True
#             return self.long
        
        
#     def isPushed(self):
#         if self.button.value() == 0:
#             return True
#         else:
#             return False