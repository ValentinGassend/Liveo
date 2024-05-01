# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from time import time

from rpi_ws281x import Color, PixelStrip, ws, Adafruit_NeoPixel


# # LED strip configuration:
# LED_COUNT = 25         # Number of LED pixels.
# LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
# LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
# LED_DMA = 10           # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
# LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL = 0
# LED_STRIP = ws.SK6812_STRIP_RGBW
# LED_STRIP = ws.SK6812W_STRIP


# Define functions which animate LEDs in various ways.
# def colorWipe(strip, color, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         sleep(wait_ms / 1000.0)


# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, color)
#             strip.show()
#             sleep(wait_ms / 1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, 0)


# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)


# def rainbow(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256 *iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, Color(0,(i +j),0))
#         strip.show()
#         sleep(wait_ms / 1000.0)


# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256 * iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel(((i * 256 // strip.numPixels()) + j) & 255))
#         strip.show()
#         sleep(wait_ms / 1000.0)


# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, wheel((i + j) % 255))
#             strip.show()
#             sleep(wait_ms / 1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i + q, 0)


# def newRainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256 * iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i + j) & 255))
#         strip.show()
#         sleep(wait_ms / 1000.0)


# def newRainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256 * iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel(((256 // strip.numPixels()) + j) & 255))
#         strip.show()
#         # sleep(wait_ms / 1000.0)


class LedMode:

    def __init__(self, colors):
        LED_COUNT = 50       # Number of LED pixels.
        # GPIO pin connected to the pixels (must support PWM!).
        LED_PIN = 19
        LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
        # DMA channel to use for generating signal (try 10)
        LED_DMA = 1
        LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
        # True to invert the signal (when using NPN transistor level shift)
        LED_INVERT = False
        LED_CHANNEL = 1
        LED_STRIP = ws.SK6812_STRIP_RGBW
        self.strip_chill = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,LED_CHANNEL )
        # Intialize the library (must be called once before other functions).
        self.strip_chill.begin()
        self.max = False

        self.startedTime = time()
        self.firstTime = True
        if not type(colors) == type(['']):
            colors = [colors]
        self.colors = colors

        self.nbrColor = 0

        pass

    def switcher(self, strip=None, delay_ms=5):
        # """Draw rainbow that uniformly distributes itself across all pixels."""
        if not strip:
            strip = self.strip_chill
        for i in range(0, strip.numPixels(), 1):
            if self.firstTime:
                self.startedTime = time()
                self.nbrColor = 0
                self.firstTime = False
            currentTime = time()

            if not self.nbrColor == len(self.colors):
                print(self.nbrColor)
                print(currentTime-self.startedTime)
                if currentTime-self.startedTime < delay_ms:
                    strip.setPixelColor(i, self.colors[self.nbrColor])
                else:
                    self.nbrColor = self.nbrColor+1
                    self.startedTime = time()
            else:
                self.nbrColor = 0
        strip.show()

    def ledOff(self, strip=None, delay_ms=5):
        # """Draw rainbow that uniformly distributes itself across all pixels."""
        if not strip:
            strip = self.strip_chill
        for i in range(0, strip.numPixels(), 1):
            if self.firstTime:
                self.startedTime = time()
                self.nbrColor = 0
                self.firstTime = False
            currentTime = time()

            if not self.nbrColor == len(self.colors):
                strip.setBrightness(
                    int(((((currentTime-self.startedTime)/delay_ms)*1)-255)*-1))
            else:
                self.nbrColor = 0
        strip.show()

    def static(self, strip=None, delay_ms=5):
        if not strip:
            strip = self.strip_chill
        for j in range(256):
            for i in range(0, strip.numPixels(), 1):
                if self.firstTime:
                    self.startedTime = time()
                    self.nbrColor = 0
                    self.firstTime = False
                currentTime = time()

                if not self.nbrColor == len(self.colors):
                    if currentTime-self.startedTime < delay_ms:
                        self.colors[self.nbrColor]
                        strip.setPixelColor(i, (self.colors[self.nbrColor]))
                        # fade in
                        # strip.setBrightness(int(((currentTime-self.startedTime)/delay_ms)*255))
                        # fade out
                        strip.setBrightness(
                            int(((((currentTime-self.startedTime)/delay_ms)*255)-255)*-1))
                    else:
                        self.nbrColor = self.nbrColor+1
                        self.startedTime = time()
                else:
                    self.nbrColor = 0
        strip.show()

    def fade(self, strip=None, delay_ms=5):
        if not strip:
            strip = self.strip_chill
        for j in range(256):
            for i in range(0, strip.numPixels(), 1):
                if self.firstTime:
                    self.startedTime = time()
                    self.nbrColor = 0
                    self.firstTime = False
                    self.max = False
                currentTime = time()

                if not self.nbrColor == len(self.colors):
                    if currentTime-self.startedTime < delay_ms:
                        self.colors[self.nbrColor]
                        strip.setPixelColor(i, (self.colors[self.nbrColor]))
                        if not self.max:
                            # fade out
                            strip.setBrightness(
                                int(((((currentTime-self.startedTime)/delay_ms)*255)-255)*-1))
                            # fade in
                            strip.setBrightness(
                                int(((currentTime-self.startedTime)/delay_ms)*255))
                            if int(((currentTime-self.startedTime)/delay_ms)*255) == 254:
                                self.max = True
                    else:
                        # fade in
                        strip.setBrightness(
                            int(((currentTime-self.startedTime - delay_ms)/delay_ms)*255))
                        # fade out
                        strip.setBrightness(
                            int(((((currentTime-self.startedTime - delay_ms)/delay_ms)*255)-255)*-1))

                        # strip.setBrightness(int((((delay_ms/(currentTime-self.startedTime))*255)-255)*-1))
                        if int(((((currentTime-self.startedTime - delay_ms)/delay_ms)*255)-255)*-1) == 1:
                            self.max = False
                            self.nbrColor = self.nbrColor+1
                            self.startedTime = time()

                    # else:
                    #     self.nbrColor=self.nbrColor+1
                    #     self.startedTime= time()
                else:
                    self.nbrColor = 0
        strip.show()

    # def switcher_chill(self, strip ,delay_ms=5 ):
    #     # """Draw rainbow that uniformly distributes itself across all pixels."""
    #     for j in range(256):
    #         for i in range(0, strip.numPixels(), 1):
    #             if self.firstTime:
    #                 self.startedTime= time()
    #                 self.nbrColor=0
    #                 self.firstTime=False
    #             currentTime = time()

    #             if not self.nbrColor == len(self.colors ):
    #                 if currentTime-self.startedTime < delay_ms:
    #                     strip.setPixelColor(i, (self.colors[self.nbrColor]))
    #                 else:
    #                     self.nbrColor=self.nbrColor+1
    #                     self.startedTime= time()
    #             else :
    #                 self.nbrColor=0
    #     strip.show()

    # sleep(wait_ms / 1000.0)
# Main program logic follows:
# strip_chill = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
# strip_chill.begin()
# strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
# strip.begin()
# Create NeoPixel object with appropriate configuration.
# strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# # Intialize the library (must be called once before other functions).
# # strip.begin()
firstTime = True
red = Color(255, 0, 0, 1)
blue = Color(164, 193, 255, 0)
green = Color(102, 255, 102, 255)
purple = Color(153, 51, 255, 100)
Ledmanager = LedMode([blue])
Ledmanager.ledOff()
# Ledmanager.static()
# Ledmanager.fade()
while True:
    Ledmanager.fade()
    pass
