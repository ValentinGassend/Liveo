from rpi_ws281x import Color
from led import LedMode
import time

class LedStateMachine:
    def __init__(self, colors):
        self.led_mode = LedMode(colors)

    def handle_command(self, command):
        if command == "LED_fade":
            self.led_mode.handle_message("LED_fade")
        elif command == "LED_static":
            self.led_mode.handle_message("LED_static")
        elif command == "LED_off":
            self.led_mode.handle_message("LED_off")
        elif command == "LED_state":
            status = self.led_mode.led_status
            print("LED status:", status)
        else:
            print("Invalid command")

# Exemple d'utilisation
colors = [Color(244, 251, 255, 0), Color(244, 251, 255, 0), Color(244, 251, 255, 0)]  # Exemple de couleurs pour les LEDs
led_state_machine = LedStateMachine(colors)

# Utilisation des commandes
print("static")

led_state_machine.handle_command("LED_static")
time.sleep(2)
print("off")
led_state_machine.handle_command("LED_off") 
time.sleep(5)
print("static")

led_state_machine.handle_command("LED_static")
time.sleep(2)
# led_state_machine.handle_command("LED_static")
# while True:
#     led_state_machine.handle_command("LED_fade")  # Démarre le mode "fade"
#     led_state_machine.handle_command("LED_static")  # Démarre le mode "static"
#     led_state_machine.handle_command("LED_off")  # Éteint les LEDs
#     led_state_machine.handle_command("LED_state")
#     pass
