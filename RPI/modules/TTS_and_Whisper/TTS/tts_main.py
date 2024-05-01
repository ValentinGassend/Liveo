import subprocess


class Tts :
    def __init__(self) :
        self.process = None
        preprocess = subprocess.Popen("sudo modprobe snd_bcm2835", shell=True)
        preprocess.wait()

    def lunch(self,file):
        self.process = subprocess.Popen("espeak -v mb-fr4 -f "+file, shell=True)
        return True
    