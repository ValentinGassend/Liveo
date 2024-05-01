import RPi.GPIO as GPIO
#import the RPi.GPIO library
from time import sleep
from RPLCD.gpio import CharLCD
#import the CharLCD library from RPLCD.gpio

GPIO.setwarnings(False)
#to ignore the warnings

lcd = CharLCD(pin_rs = 37, pin_e=35, pins_data= [33, 31, 29, 23],
numbering_mode = GPIO.BOARD, cols=16, rows=2, dotsize=8)
#declare the LCD pins with GPIO pins of Raspberry Pi 4
while True:
    lcd.clear()
    #clear the screen of LCD


    lcd.write_string("It’s LinuxHint")
    sleep(1/10)
    #display the text on 16x2 LCD