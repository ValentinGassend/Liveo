from gtts import gTTS
from pygame import mixer
import subprocess

class TTS:
    def __init__(self):
        mixer.init()

    def talk(self, content):
        if not isinstance(content, str):
            content = str(content)

        tts = gTTS(content, lang='fr')
        audio_file = "output.mp3"
        tts.save(audio_file)

        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            pass

    def sound(self, file):
        if not type(file)==type(""):
            file = str(file)
        subprocess.Popen("aplay '"+file+"'", shell=True)

    def kill(self):
        mixer.music.stop()
