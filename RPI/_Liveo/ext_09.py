from TTS.tts import TTS
from time import sleep
# import subprocess
myTTS = TTS()
# from LED_Strip.led import LedMode
# from rpi_ws281x import Color
# red = Color(255,0,0,1)
# blue = Color(164,193,255,0)
# green = Color(102,255,102,255)
# purple = Color(153,51,255,100)
# Ledmanager = LedMode([blue])

# Ledmanager.ledOff()
myTTS.talk("Vous avez un rendez-vous chez votre médecin traitant le mercredi 17 juin à 10:30, soit dans 30 minutes, vous ne devez pas oublié votre carte vitale. Souhaitez-vous que je répètes les informations liées au rendez-vous ?")
# while True:
#     # Ledmanager.fade()
#     pass
# myTTS.talk("Je récapitule, vous avez un rendez-vous chez votre médecin traitant le mardi 16 juin à 10:30 et vous ne devez pas oublié votre carte vitale. Je veillerais à vous le rappeler 30 minutes avant, soit à 10 heure.")
# myTTS.talk("Je veillerais à vous le rappeler 30 minutes avant, soit à 10 heure. Est-ce que ces informations sont correctes ?")
