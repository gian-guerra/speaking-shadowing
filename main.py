import os
from modules import index, audio, files, scripts, utils

FOLLOW_UP_OPTIONS = "[r] Repeat this topic\n[t] Choose another topic\n[s] Change section/dimension\n[q] Quit\n>>"
def main():
    print("Welcome to this pronunciation shadowing tool")

    while True:
        mode = input("\nSelect mode:\n[1] Line by line\n[2] Full chunk\n[3] Chunk (line-by-line IPA)\n[q] Quit: ").strip()
        if mode == "q":
            return
        mode = "lines" if mode == "1" else "chunk-paired" if mode == "3" else "chunk"
        
        dimension = input("Insert dimension: ")
        subDimension = input("Insert subdimension: ")
        section = input("Insert section: ")

        practicePath = f"{dimension}/section{section}"
        if subDimension != "":
            practicePath = f"{dimension}/{subDimension}/section{section}"
        paths = utils.getPaths(practicePath)

        while True:
            topic = files.select_topic(paths["script"])
            if not topic:
                print("No topic selected!")
                break

            script_file, audio_file, pronunciation_data = files.load_files_for_topic(topic, paths, mode)
            script_lines = scripts.load_script(script_file, mode=mode, ipa_path=os.path.join(paths["pronunciation"], f"{topic}.txt"))
            print(script_lines)
            audio_segments = audio.load_audio_segments_for_mode(audio_file, mode, len(script_lines) if mode == "lines" else None)

            if mode == "lines" and len(audio_segments) != len(script_lines):
                print(f"Audio length: {len(audio_segments)} and script length: {len(script_lines)} may not match perfectly")

            index.shadowing_session(script_lines, audio_segments, pronunciation_data, mode)

if __name__ == "__main__":
    main()

