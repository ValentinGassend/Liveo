# from whisper.whisper import Whisper
import subprocess
from whisper_and_controller.whisper_main import Whisper
from TTS.tts_main import Tts
from time import time, sleep

# with open('text_live.txt') as f:
#     lines = f.readlines()
#     print(lines)

class Manager_TTS_Whisper:

    def __init__(self):
        self.startTime  = time()
        self.transcription = Whisper()
        self.speaker = Tts()
        self.speaked = False
        self.priseRDV = False
        self.text = ""
        self.transcription.lunch()

# with open('./TTS_and_Whisper/text_live.txt') as f:
#                 lines = f.readlines()
#                 print(lines)
#                 for line in lines:
#                     text = text + line
#                 print(text)

    def start(self):
        self.actualTime = time()
        # if (actualTime-startTime > 15) and (actualTime-startTime < 20):
        #     if not priseRDV:
        #         subprocess.Popen("espeak -v mb-fr1 -a 75 \"Peux-tu me faire un résumé de mes évènement de la journée s'il te plait ?\"", shell=True)
        #         priseRDV=True
        if (self.actualTime-self.startTime > 30):
            if not self.speaked:
                self.transcription.stop()
                self.file = './TTS_and_Whisper/text_live.txt'
                self.speaker.lunch(self.file)
                self.speaked=True
        else:
            pass




Whisper  = Manager_TTS_Whisper()

while True:
    Whisper.start()
    