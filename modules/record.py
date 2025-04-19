import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
from pydub import AudioSegment
from pydub.playback import play
import os
import time

def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return audio, sample_rate

def record_audio_until_keypress(sample_rate=44100):
    input("🎙️ Press [Enter] to start recording...")
    print("🎙️ Recording... Press [Enter] again to stop.")
    
    start_time = time.time()

    max_duration = 300
    recording = sd.rec(int(max_duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')

    input()
    sd.stop()
    
    end_time = time.time()
    trimmed = recording[:int((end_time - start_time) * sample_rate)]
    return trimmed, sample_rate

def play_recorded_audio(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, sample_rate, audio_data)
        temp_audio = AudioSegment.from_wav(tmpfile.name)
        play(temp_audio)
        os.unlink(tmpfile.name)

def save_and_play_recording(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, sample_rate, audio_data)
        tmpfile_path = tmpfile.name

    audio = AudioSegment.from_wav(tmpfile_path)
    play(audio)

    time.sleep(0.5)

    try:
        os.remove(tmpfile_path)
    except PermissionError:
        print("⚠️ Could not delete temp file. It may still be in use.")