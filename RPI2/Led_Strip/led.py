# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
from time import time, sleep
from rpi_ws281x import Color, PixelStrip, ws, Adafruit_NeoPixel
import threading


class LedMode:

    def __init__(self, colors=[Color(244, 251, 255, 0)]):
        LED_COUNT = 25       # Number of LED pixels.
        # GPIO pin connected to the pixels (must support PWM!).
        LED_PIN = 18
        LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
        # DMA channel to use for generating signal (try 10)
        LED_DMA = 10
        LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
        # True to invert the signal (when using NPN transistor level shift)
        LED_INVERT = False
        LED_CHANNEL = 0
        LED_STRIP = ws.SK6812_STRIP_RGBW
        self.strip_chill = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip_chill.begin()
        self.max = False

        self.fade_thread = threading.Thread(target=self.fade_loop)
        self.fade_thread_stop = threading.Event()
        self.static_thread = threading.Thread(target=self.static_loop)
        self.static_thread_stop = threading.Event()
        self.off_thread = threading.Thread(target=self.off_loop)
        self.off_thread_stop = threading.Event()
        self.startedTime = time()
        self.firstTime = True
        if not isinstance(colors, list):
            
            colors = [colors]
        self.colors = colors

        self.nbrColor = 0

        self.led_status = "Off_mode"
        self.ledOff()  # Variable pour stocker l'état des LEDs

    def handle_message(self, message,delay=1):
        self.firstTime=True

        if message == "LED_fade":
            self.fade_thread_stop.set()  # Définit l'Event pour arrêter le thread de "static"
            if not self.fade_thread.is_alive():
                self.fade_thread = threading.Thread(target=self.fade_loop)
                self.static_thread_stop.set()
                self.off_thread_stop.set()
                self.fade_thread_stop.clear()
                self.fade_thread.start()
        elif message == "LED_STATE":
            
            pass
        elif message == "LED_static" or message =="LED_static_2":
            # self.static_thread_stop.set()  # Définit l'Event pour arrêter le thread de "static"
            if self.off_thread.is_alive():
                print("Alive")
            if not self.static_thread.is_alive():
                print("not Alive")
                
                self.static_thread = threading.Thread(target=self.static_loop,args=(delay,))
                self.static_thread_stop.set()
                self.off_thread_stop.set()
                self.static_thread_stop.clear()
                self.static_thread.start()
        elif message == "LED_off":
            # self.static_thread_stop.set()
            if not self.off_thread.is_alive():
                self.off_thread = threading.Thread(target=self.off_loop, args=(delay,))
                self.off_thread_stop.clear()
                self.static_thread_stop.set()
                self.fade_thread_stop.set()
                self.off_thread.start()
        # else:
        #     if not self.off_thread.is_alive():
        #         self.off_thread = threading.Thread(target=self.off_loop(delay))
        #         self.off_thread_stop.clear()
        #         self.static_thread_stop.set()
        #         self.fade_thread_stop.set()
        #         self.off_thread.start()

    def off_loop(self, delay):
        while not self.off_thread_stop.is_set():  # Vérifie si l'Event a été défini pour arrêter le thread
            self.ledOff(delay_ms=delay)

    def ledOff(self, strip=None, delay_ms=5):
        # """Draw rainbow that uniformly distributes itself across all pixels."""
        if not strip:
            strip = self.strip_chill
        for i in range(0, strip.numPixels(), 1):
            if self.firstTime:
                self.startedTime = time()
                self.nbrColor = 0
                self.firstTime = False

            if not self.nbrColor == len(self.colors):
                strip.setBrightness(0)
            else:
                self.nbrColor = 0
        strip.show()
        self.led_status = "Off_mode"  # Met à jour l'état des LEDs

    def static_loop(self, delay):
        while not self.static_thread_stop.is_set():  # Vérifie si l'Event a été défini pour arrêter le thread
            self.static(delay_ms=delay)

    def static(self, strip=None, delay_ms=1):
        if not strip:
            strip = self.strip_chill
        for j in range(256):
            for i in range(0, strip.numPixels(), 1):
                if self.firstTime:
                    self.startedTime = time()
                    self.nbrColor = 0
                    self.firstTime = False
                currentTime = time()
                print(currentTime-self.startedTime>delay_ms )
                print(currentTime-self.startedTime )


                if not self.nbrColor == len(self.colors):
                    if currentTime-self.startedTime<delay_ms:
                        self.colors[self.nbrColor]
                        strip.setPixelColor(i, self.colors[self.nbrColor])
                        strip.setBrightness(255)

                    else:
                        self.nbrColor = self.nbrColor + 1
                        strip.setBrightness(0)
                        # self.handle_message("LED_off")
                        # self.led_status = "Off_mode"
                else:
                    self.nbrColor = 0

            strip.show()  # Afficher les pixels après chaque itération de la boucle j
              # Sortir de la boucle j si le délai spécifié est atteint

        self.led_status = "Static_mode"  # Met à jour l'état des LEDs

    def fade_loop(self):
        while not self.fade_thread_stop.is_set():  # Vérifie si l'Event a été défini pour arrêter le thread
            self.fade()

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
                    if currentTime - self.startedTime < delay_ms:
                        self.colors[self.nbrColor]
                        strip.setPixelColor(i, self.colors[self.nbrColor])
                        if not self.max:
                            # fade out
                            fade_out_brightness = int(((((currentTime - self.startedTime) / delay_ms) * 255) - 255) * -1)
                            strip.setBrightness(max(0, min(255, fade_out_brightness)))
                            # fade in
                            fade_in_brightness = int(((currentTime - self.startedTime) / delay_ms) * 255)
                            strip.setBrightness(max(0, min(255, fade_in_brightness)))
                            if fade_in_brightness == 254:
                                self.max = True
                    else:
                        # fade in
                        fade_in_brightness = int(((currentTime - self.startedTime - delay_ms) / delay_ms) * 255)
                        strip.setBrightness(max(0, min(255, fade_in_brightness)))
                        # fade out
                        fade_out_brightness = int(((((currentTime - self.startedTime - delay_ms) / delay_ms) * 255) - 255) * -1)
                        strip.setBrightness(max(0, min(255, fade_out_brightness)))

                        if fade_out_brightness == 1:
                            self.max = False
                            self.nbrColor = self.nbrColor + 1
                            self.startedTime = time()

                else:
                    self.nbrColor = 0
        strip.show()
        self.led_status = "Fade_mode"  # Met à jour l'état des LEDs

    def get_led_status(self):
        return self.led_status
