from gtts import gTTS
import os

def generate_voice_msg(text, filename="voice_payload.mp3"):
    tts = gTTS(text=text, lang='es')
    path = os.path.abspath(filename)
    tts.save(path)
    return path