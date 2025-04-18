import os
import sounddevice as sd
from pydub import AudioSegment
from pydub.playback import play
from scipy.io.wavfile import write, read
import tempfile

def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return audio, sample_rate

def play_recorded_audio(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, sample_rate, audio_data)
        temp_audio = AudioSegment.from_wav(tmpfile.name)
        play(temp_audio)
        os.unlink(tmpfile.name)