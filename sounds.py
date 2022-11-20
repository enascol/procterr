from ursina import Audio
from settings import AUDIO_PATH

import os.path
import os


files = [song_file.split(".")[0] for song_file in os.listdir(AUDIO_PATH) if song_file.split(".")[-1] == "wav"]
files_path = [os.path.join(song_file) for song_file in files] 
ost = {name: path for name, path in zip(files, files_path)}

def play(name, **config):
    try:
        audio = Audio(ost[name], **config)
        audio.play()
        print(f"[*] Playing now: {name}")
        return audio

    except KeyError:
        print(F"could not find {name} song in current path")
