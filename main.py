from led.led import Led
from machine import Pin
from btn.btn import Button
import time

blue_pin = Pin(27, Pin.OUT)
green_pin = Pin(14, Pin.OUT)
red_pin = Pin(26, Pin.OUT)

my_led = Led(blue_pin, green_pin, red_pin)
my_button = Button(23)
button_status = False

start_time = 0
led_duration = 1  # Durée d'allumage de la LED en secondes

while True:
    if not button_status:
        button_status = my_button.check_status()
        if button_status:
            start_time = time.time()
    else:
        print("Appui long détecté")
        my_led.on_green()
        current_time = time.time()
        if current_time - start_time >= led_duration:
            my_led.turn_off()
            button_status = False
