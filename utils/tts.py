
from gtts import gTTS
import tempfile

def text_to_speech(text):
    tts = gTTS(text, lang='fr')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tts.save(tmp.name)
        return tmp.name
