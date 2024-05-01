from gtts import gTTS
from pygame import mixer
import subprocess
from pydub import AudioSegment


class TTS:
    def __init__(self):
        mixer.init()
        subprocess.run("sudo modprobe snd_bcm2835", shell=True)

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
        if not type(file) == type(""):
            file = str(file)
        subprocess.Popen("aplay '"+file+"'", shell=True)

    def kill(self):
        mixer.music.stop()


# mytts = TTS()

# mytts.talk("coucou les copains")
