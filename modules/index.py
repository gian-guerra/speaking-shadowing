from pydub.playback import play
from pydub.silence import split_on_silence
from scipy.io.wavfile import write, read
from modules import record

INSTRUCTIONS = "Instructions: [r]epeat | [n]ext | [q]uit | [v]record and compare | [s]stress | [i]ipa | [l]linking | [a]all\n"

def printMultipleLines(lines):
    for _, line in enumerate(lines):
        print(line)
    
def shadowing_session(script_lines, audio_segments, pronunciation_data, mode):
    print("\n Shadowing Session Started ")

    for index, line in enumerate(script_lines):
        pronunciation = pronunciation_data[index]
        toPrint = [f"\n📢 {line}", f"IPA: {pronunciation.get('ipa', 'N/A')}"]
        while True:
            printMultipleLines(toPrint)
            nextPrintLines = [f"\n📢 {line}"]
            play(audio_segments[index])

            ipaDisplay = nextPrintLines.append(f"IPA: {pronunciation.get('ipa', 'N/A')}")
            stressDisplay = nextPrintLines.append(f"Stress: {pronunciation.get('stress', 'N/A')}")
            linkingDisplay = nextPrintLines.append(f"Linking:\n{pronunciation.get('linking', 'N/A')}")
            
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
                nextPrintLines.append(ipaDisplay)
            elif mode == "lines" and command in ("s", "i", "l", "a"):
                if command == "s":
                    nextPrintLines.append(stressDisplay)
                elif command == "l":
                    nextPrintLines.append(linkingDisplay)
                elif command == "a":
                    nextPrintLines.append(stressDisplay)
                    nextPrintLines.append(ipaDisplay)
                    nextPrintLines.append(linkingDisplay)
            else:
                print("Invalid input. Please try again.")
            toPrint = nextPrintLines
