import os
import re
import json
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
from scipy.io.wavfile import write, read
from modules import record

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"


SECTION_TO_PRACTICE = "vocabulary/intermediate/section1"
SCRIPTS_DIR = f"scripts/{SECTION_TO_PRACTICE}"
AUDIOS_DIR = f"audios/{SECTION_TO_PRACTICE}"
PRONUNCIATION_DIR = f"pronunciation/{SECTION_TO_PRACTICE}"

def list_files(directory, extension=None):
    files = [f for f in os.listdir(directory) if not extension or f.endswith(extension)]
    return files

def format_line(line):
    return re.sub(r"\{(.*?)\}", f"{BOLD}{BLUE}\\1{RESET}", line)

def load_script(script_path, mode="lines"):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if mode == "chunk":
            return [format_line(content)]  # return as a single-element list
        return [format_line(line.strip()) for line in content.splitlines() if line.strip()]

def load_audio_segments_for_mode(audio_path, mode, expected_segments=None):
    if mode == "chunk":
        return [AudioSegment.from_file(audio_path)]  # Single chunk
    else:
        return load_audio_segments_with_silence(audio_path, expected_segments)

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

def load_pronunciation_data(pronunciation_path):
    with open(pronunciation_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
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

def load_ipa_text(ipa_txt_path):
    with open(ipa_txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def shadowing_session(script_lines, audio_segments, pronunciation_data, mode):
    print("\n Shadowing Session Started ")
    print("Instructions: [r]epeat | [n]ext | [q]uit | [v]record and compare | [s]stress | [i]ipa | [l]linking | [a]all\n")

    for index, line in enumerate(script_lines):
        while True:
            print(f"\n📢 {line}")
            print(f"IPA: {pronunciation_data[index].get('ipa', 'N/A')}")
            if mode == "lines":
                print(f"Linking: {pronunciation_data[index].get('linking', 'N/A')}")
            play(audio_segments[index])

            command = input(">> [r]epeat | [n]ext | [q]uit | [v]record and compare" +
                            (" | [s]stress | [i]ipa | [l]linking | [a]all" if mode == "lines" else "") + "\n").strip().lower()
            
            if command == "n":
                break
            elif command == "q":
                print("Exiting...")
                return
            elif command == "r":
                continue
            elif command == "v":
                audio_data, sr = record.record_audio_until_keypress()
                print("🔁 Playing your recording...")
                record.save_and_play_recording(audio_data, sr)
                break
            elif mode == "lines" and command in ("s", "i", "l", "a"):
                data = pronunciation_data[index]
                if command == "s":
                    print(f"Stress: {data.get('stress', 'N/A')}")
                elif command == "i":
                    print(f"IPA: {data.get('ipa', 'N/A')}")
                elif command == "l":
                    print(f"Linking:\n{data.get('linking', 'N/A')}")
                elif command == "a":
                    print(f"Stress: {data.get('stress', 'N/A')}")
                    print(f"IPA: {data.get('ipa', 'N/A')}")
                    print(f"Linking:\n{data.get('linking', 'N/A')}")
            else:
                print("Invalid input. Please try again.")

def main():
    print("Welcome to this pronunciation shadowing tool")

    mode = input("Select mode: [1] Line by line (dialogue) or [2] Full chunk (paragraph): ").strip()
    mode = "chunk" if mode == "2" else "lines"

    script_file = select_file(SCRIPTS_DIR, ".txt")
    if not script_file:
        return

    audio_file = select_file(AUDIOS_DIR, ".mp3")
    if not audio_file:
        return

    if mode == "lines":
        pronunciation_file = select_file(PRONUNCIATION_DIR, ".json")
        if not pronunciation_file:
            return
        pronunciation_data = load_pronunciation_data(pronunciation_file, mode)
    else:
        pronunciation_file = select_file(PRONUNCIATION_DIR, ".txt")
        if not pronunciation_file:
            return
        ipa_text = load_ipa_text(pronunciation_file)
        pronunciation_data = [{"ipa": ipa_text}]

    script_lines = load_script(script_file, mode=mode)
    audio_segments = load_audio_segments_for_mode(audio_file, mode, len(script_lines) if mode == "lines" else None)

    if mode == "lines" and len(audio_segments) != len(script_lines):
        print(f"Audio length: {len(audio_segments)} and script length: {len(script_lines)} may not match perfectly")

    shadowing_session(script_lines, audio_segments, pronunciation_data, mode)

if __name__ == "__main__":
    main()

