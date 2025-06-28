from pydub import AudioSegment
from pydub.silence import split_on_silence

def load_audio_segments_for_mode(audio_path, mode, expected_segments=None):
    if mode == "lines":
        return load_audio_segments_with_silence(audio_path, expected_segments)
    else:
        return [AudioSegment.from_file(audio_path)]

def load_audio_segments(audio_path, number_of_segments):
    audio = AudioSegment.from_file(audio_path)
    segment_duration = len(audio) // number_of_segments
    segments = [audio[i*segment_duration:(i+1)*segment_duration] for i in range(number_of_segments)]
    return segments

def load_audio_segments_with_silence(audio_path, expected_segments):
    audio = AudioSegment.from_file(audio_path)

    chunks = split_on_silence(
        audio,
        min_silence_len=1500,
        silence_thresh=audio.dBFS - 16,
        keep_silence=200
    )

    if expected_segments and len(chunks) != expected_segments:
        print(f"Warning: Found {len(chunks)} segments, but script has {expected_segments} lines.")
    return chunks