import subprocess

class TTS:
    def __init__(self):
        subprocess.Popen("sudo modprobe snd_bcm2835", shell=True)
        self.talkSubprocess = None
        pass

    def talk(self, content):
        if not type(content)==type(""):
            content = str(content)
        self.talkSubprocess = subprocess.Popen("espeak -v mb-fr4 '"+content+"'", shell=True)

    def sound(self, file):
        if not type(file)==type(""):
            file = str(file)
        subprocess.Popen("aplay '"+file+"'", shell=True)
    
    def kill(self):
        if self.talkSubprocess:
            self.talkSubprocess.terminate()

myTTS = TTS()

myTTS.talk("blablabla")