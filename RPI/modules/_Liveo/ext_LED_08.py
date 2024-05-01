from LED_Strip.led import LedMode
from rpi_ws281x import Color
red = Color(255, 0, 0, 1)
blue = Color(164, 193, 255, 0)
green = Color(102, 255, 102, 255)
purple = Color(153, 51, 255, 100)
Ledmanager = LedMode([blue])
print(Ledmanager.strip_chill.numPixels())

Ledmanager.ledOff()
while True:
    Ledmanager.fade()
    pass
