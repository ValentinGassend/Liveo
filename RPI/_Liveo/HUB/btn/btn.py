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
                self.pressed = True
        if time.time() - self.startedTime > 1:
            self.pressed = False
