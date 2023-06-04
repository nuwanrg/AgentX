import os
import requests
import openai
from aiengine.config import Config
cfg = Config()

openai.api_key = cfg.openai_api_key


def convert_speech_to_text(file_name):
    print('convert_speech_to_text is called...')
    # Read the audio file as binary data
    audio_file_path = os.path.join("./", file_name)

    # Make a POST request to the Whisper ASR API
    audio_file = open(audio_file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print('transcript...', transcript['text'])
    return transcript['text']
