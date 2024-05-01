import time
from rpi_ws281x import Adafruit_NeoPixel, Color

class BandeauLED:
    def __init__(self, data_pin, num_leds):
        self.data_pin = data_pin
        self.num_leds = num_leds

        # Configuration du bandeau LED NeoPixel
        LED_FREQ_HZ = 800000
        LED_DMA = 10
        LED_BRIGHTNESS = 255
        LED_INVERT = False
        self.strip = Adafruit_NeoPixel(self.num_leds, self.data_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()


    def set_pixel(self, index, color):
        # Vérification des limites de l'index
        if index < 0 or index >= self.num_leds:
            return

        # Mise à jour de la couleur du pixel
        self.strip.setPixelColor(index, color)

    def show(self):
        # Affichage des LED avec la nouvelle couleur
        self.strip.show()

    def clear(self):
        # Effacement de tous les pixels
        for i in range(self.num_leds):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def fade_in_fade_out(self, color, duration):
        # Réalise un fondu (fade) d'une couleur spécifique sur toutes les LED du bandeau
        start_time = time.time()
        elapsed_time = 0

        while elapsed_time < duration:
            brightness = int(255 * (elapsed_time / duration))

            # Mise à jour de la couleur de chaque LED avec la luminosité appropriée
            for i in range(self.num_leds):
                self.set_pixel(i, Color(color[0] * brightness // 255, color[1] * brightness // 255, color[2] * brightness // 255))

            # Affichage des LED avec la nouvelle couleur et luminosité
            self.show()

            # Attente de 10 millisecondes avant la prochaine itération
            time.sleep(0.01)

            # Mise à jour du temps écoulé
            elapsed_time = time.time() - start_time

        # Effacement du bandeau LED à la fin du fondu
        self.clear()

    def leds_off(self):
        # Met toutes les LED en mode "off" (éteintes)
        self.clear()

    def cleanup(self):
        # Nettoyage lors de la fermeture de la classe
        self.clear()


data_pin = 23  # Utilisez un autre pin GPIO disponible
num_leds = 10
bandeau = BandeauLED(data_pin, num_leds)

# Définition de la couleur pour le fondu (ici, rouge)
color = (255, 0, 0)

# Durée du fondu en secondes
duration = 5

# Réalisation du fondu
bandeau.fade_in_fade_out(color, duration)

# Nettoyage
bandeau.cleanup()
