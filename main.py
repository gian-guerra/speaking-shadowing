import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence

SCRIPTS_DIR = "scripts"
AUDIOS_DIR = "audios"

def list_files(directory, extension=None):
    files = [f for f in os.listdir(directory) if not extension or f.endswith(extension)]
    return files

def load_script(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_audio_segments(audio_path, number_of_segments):
    audio = AudioSegment.from_file(audio_path)
    segment_duration = len(audio) // number_of_segments
    segments = [audio[i*segment_duration:(i+1)*segment_duration] for i in range(number_of_segments)]
    return segments

def load_audio_segments_with_silence(audio_path, expected_segments):
    audio = AudioSegment.from_file(audio_path)

    chunks = split_on_silence(
        audio,
        min_silence_len=1000,
        silence_thresh=audio.dBFS - 16,
        keep_silence=200
    )

    if expected_segments and len(chunks) != expected_segments:
        print(f"Warning: Found {len(chunks)} segments, but script has {expected_segments} lines.")
    return chunks

def select_file(directory, extension):
    files = list_files(directory, extension)
    if not files:
        print(f"No files found in directory {directory}")
        return None

    print(f"\nAvailable files in directory {directory}")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    while True:
        try:
            choice = int(input("Select a file by number: "))
            if 1 <= choice <= len(files):
                return os.path.join(directory, files[choice-1])
        except ValueError:
            pass
        print("Invalid selection. Please enter a valid number")

def shadowing_session(script_lines, audio_segments):
    print("\n Shadowing Session Started ")
    print("Instructions: [r]epeat | [n]ext | [q]uit\n")

    for index, line in enumerate(script_lines):
        while True:
            print(f"\n📢 {line}")
            play(audio_segments[index])

            command = input(">> [r]epeat | [n]ext | [q]uit\n").strip().lower()
            if command == "n":
                break
            elif command == "q":
                print("Exiting...")
                return
            elif command == "r":
                continue
            else:
                print("Invalid input. Please try to use r/n/q")

def main():
    print("Welcome to this pronounciation shadowing tool")

    script_file = select_file(SCRIPTS_DIR, ".txt")
    if not script_file:
        return

    audio_file = select_file(AUDIOS_DIR, ".mp3")
    if not audio_file:
        return

    script_lines = load_script(script_file)
    audio_segments = load_audio_segments_with_silence(audio_file, len(script_lines))

    if len(audio_segments) != len(script_lines):
        print("Audio length and script length may not match perfectly")

    shadowing_session(script_lines, audio_segments)

if __name__ == "__main__":
    main()

