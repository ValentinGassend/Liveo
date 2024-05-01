import subprocess
# from time import sleep
class Whisper :
    def __init__(self) :
        self.process = None

    def lunch(self):
        self.process = subprocess.Popen("./stream -m models/ggml-tiny.bin --step 10000 --keep 0 --length 15360 -c 0 -t 3 -ac 1024 -l fr -f ../../text_live.txt", shell=True, cwd=r'/home/valentin/Desktop/MemoRoom/modules/TTS_and_Whisper/whisper_and_controller/whisper.cpp')
        
    
    def stop(self):
        self.process.terminate()
        self.process.kill()
