import subprocess
subprocess.Popen(
    "whisper-ctranslate2 --live_transcribe True --language en", shell=True)
