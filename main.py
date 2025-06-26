
from pydub.playback import play
from pydub.silence import split_on_silence
from scipy.io.wavfile import write, read
from modules import record, audio, files, pronunciation, scripts
from pathlib import Path

project_root = Path(__file__).resolve().parent

def getPaths(sectionToPractice):
    scripts_path = project_root / f"scripts/{sectionToPractice}"
    audios_path = project_root / f"audios/{sectionToPractice}"
    pronunciation_path = project_root / f"pronunciation/{sectionToPractice}"
    return {"script": scripts_path, "audio": audios_path, "pronunciation": pronunciation_path}

SECTION_TO_PRACTICE = "grammar/section1A"

INSTRUCTIONS = "Instructions: [r]epeat | [n]ext | [q]uit | [v]record and compare | [s]stress | [i]ipa | [l]linking | [a]all\n"

def printMultipleLines(lines):
    for _, line in enumerate(lines):
        print(line)
    print(INSTRUCTIONS)
    
def shadowing_session(script_lines, audio_segments, pronunciation_data, mode):
    print("\n Shadowing Session Started ")

    for index, line in enumerate(script_lines):
        pronunciation = pronunciation_data[index]
        toPrint = [f"\n📢 {line}", f"IPA: {pronunciation.get('ipa', 'N/A')}"]
        while True:
            printMultipleLines(toPrint)
            nextPrintLines = [f"\n📢 {line}"]

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
            elif command == "i":
                nextPrintLines.append(f"IPA: {pronunciation.get('ipa', 'N/A')}")
            elif mode == "lines" and command in ("s", "i", "l", "a"):
                if command == "s":
                    nextPrintLines.append(f"Stress: {pronunciation.get('stress', 'N/A')}")
                elif command == "l":
                    nextPrintLines.append(f"Linking:\n{pronunciation.get('linking', 'N/A')}")
                elif command == "a":
                    nextPrintLines.append(f"Stress: {pronunciation.get('stress', 'N/A')}")
                    nextPrintLines.append(f"IPA: {pronunciation.get('ipa', 'N/A')}")
                    nextPrintLines.append(f"Linking:\n{pronunciation.get('linking', 'N/A')}")
            else:
                print("Invalid input. Please try again.")
            toPrint = nextPrintLines

def main():
    print("Welcome to this pronunciation shadowing tool")

    mode = input("Select mode: [1] Line by line [2] Full chunk: ").strip()
    mode = "chunk" if mode == "2" else "lines"

    dimension = input("Insert dimension: ")
    subDimension = input("Insert subdimension: ")
    section = input("Insert section: ")

    practicePath = f"{dimension}/section{section}"
    if subDimension != "":
        practicePath = f"{dimension}/{subDimension}/section{section}"
    paths = getPaths(practicePath)

    script_file = files.select_file(paths["script"], ".txt")
    if not script_file:
        return

    audio_file = files.select_file(paths["audio"], ".mp3")
    if not audio_file:
        return

    if mode == "lines":
        pronunciation_file = files.select_file(paths["pronunciation"], ".json")
        if not pronunciation_file:
            return
        pronunciation_data = pronunciation.load_pronunciation_data(pronunciation_file)
    else:
        pronunciation_file = files.select_file(paths["pronunciation"], ".txt")
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

