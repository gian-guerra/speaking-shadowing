
from pydub.playback import play
from pydub.silence import split_on_silence
from scipy.io.wavfile import write, read
from modules import record, audio, files, pronunciation, scripts
from pathlib import Path

project_root = Path(__file__).resolve().parent

SECTION_TO_PRACTICE = "grammar/section1A"
SCRIPTS_DIR = project_root / f"scripts/{SECTION_TO_PRACTICE}"
AUDIOS_DIR = project_root / f"audios/{SECTION_TO_PRACTICE}"
PRONUNCIATION_DIR = project_root / f"pronunciation/{SECTION_TO_PRACTICE}"
INSTRUCTIONS = "Instructions: [r]epeat | [n]ext | [q]uit | [v]record and compare | [s]stress | [i]ipa | [l]linking | [a]all\n"

def shadowing_session(script_lines, audio_segments, pronunciation_data, mode):
    print("\n Shadowing Session Started ")
    print(INSTRUCTIONS)

    for index, line in enumerate(script_lines):
        while True:
            print(f"\n📢 {line}")
            print(f"IPA: {pronunciation_data[index].get('ipa', 'N/A')}")
            if mode == "lines":
                print(f"Linking: {pronunciation_data[index].get('linking', 'N/A')}")
            play(audio_segments[index])

            command = input(INSTRUCTIONS).strip().lower()
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

    script_file = files.select_file(SCRIPTS_DIR, ".txt")
    if not script_file:
        return

    audio_file = files.select_file(AUDIOS_DIR, ".mp3")
    if not audio_file:
        return

    if mode == "lines":
        pronunciation_file = files.select_file(PRONUNCIATION_DIR, ".json")
        if not pronunciation_file:
            return
        pronunciation_data = pronunciation.load_pronunciation_data(pronunciation_file)
    else:
        pronunciation_file = files.select_file(PRONUNCIATION_DIR, ".txt")
        if not pronunciation_file:
            return
        ipa_text = pronunciation.load_ipa_text(pronunciation_file)
        pronunciation_data = [{"ipa": ipa_text}]

    script_lines = scripts.load_script(script_file, mode=mode)
    audio_segments = audio.load_audio_segments_for_mode(audio_file, mode, len(script_lines) if mode == "lines" else None)

    if mode == "lines" and len(audio_segments) != len(script_lines):
        print(f"Audio length: {len(audio_segments)} and script length: {len(script_lines)} may not match perfectly")

    shadowing_session(script_lines, audio_segments, pronunciation_data, mode)

if __name__ == "__main__":
    main()

