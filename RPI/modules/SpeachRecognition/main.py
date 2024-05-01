import io

# from faster_whisper import WhisperModel

from pydub import AudioSegment

import speech_recognition as sr

from pywhispercpp.model import Model

import tempfile

import os

import sys

import _thread

import time

import rel

import threading

from pathlib import Path

import numpy as np

from collections import Counter


sys.path.append('/opt/homebrew/bin/ffmpeg')

AudioSegment.converter = '/opt/homebrew/bin/ffmpeg'


temp_dir = tempfile.mkdtemp()

save_path = os.path.join(temp_dir, "temp.wav")


def check_stop_word(predicted_text: str) -> bool:

    import re

    pattern = re.compile('[\W_]+', re.UNICODE)

    return pattern.sub('', predicted_text).lower() == 'stop'


def transcribe():

    model = "tiny"

    audio_model = Model(model, n_threads=4,
                        print_progress=False, print_realtime=False, language="fr", translate=False)

    # load the speech recognizer with CLI settings

    r = sr.Recognizer()

    r.energy_threshold = 700

    r.pause_threshold = 0.8

    r.dynamic_energy_threshold = False

    with sr.Microphone(sample_rate=16000) as source:

        print("Let's get the talking going!")

        while True:

            # record audio stream into wav

            audio = r.listen(source)

            data = io.BytesIO(audio.get_wav_data())

            audio_clip = AudioSegment.from_file(data)

            audio_clip.export(save_path, format="wav")

            print("before transcribe")
            result = audio_model.transcribe(
                save_path)

            for segment in result:
                print(segment.text)
            # if check_stop_word(predicted_text):

            #     break


th = threading.Thread(target=transcribe)

th.start()
