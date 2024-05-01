# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from time import time, sleep

from rpi_ws281x import Adafruit_NeoPixel

class LedMode:
    def __init__(self, colors):
        LED_COUNT = 9         # Number of LED pixels.
        LED_PIN = 20           # GPIO pin connected to the pixels (must support PWM!).
        LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10           # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 1
        self.strip_chill = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip_chill.begin()
        
        self.colors = colors
        self.nbrColor = 0

    def switcher(self, delay_ms=5):
        strip = self.strip_chill
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, self.colors[self.nbrColor])
        strip.show()

        self.nbrColor = (self.nbrColor + 1) % len(self.colors)
        sleep(delay_ms / 1000.0)

    def ledOff(self, delay_ms=5):
        strip = self.strip_chill
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, 0)
        strip.show()
        sleep(delay_ms / 1000.0)

    def static(self, delay_ms=5):
        strip = self.strip_chill
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, self.colors[self.nbrColor])
        strip.show()

        self.nbrColor = (self.nbrColor + 1) % len(self.colors)
        sleep(delay_ms / 1000.0)

    def fade(self, delay_ms=3):
        strip = self.strip_chill
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, self.colors[self.nbrColor])
        strip.show()

        self.nbrColor = (self.nbrColor + 1) % len(self.colors)
        sleep(delay_ms / 1000.0)

# Configuration des couleurs
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)

# Création de l'instance de LedMode avec les couleurs spécifiées
Ledmanager = LedMode([blue])

# Exécution des différents modes
while True:
    Ledmanager.fade()
