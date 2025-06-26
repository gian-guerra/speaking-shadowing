
from modules import index, audio, files, scripts, utils

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
    paths = utils.getPaths(practicePath)

    topic = files.select_topic(paths["script"])
    if not topic:
        return
    script_file, audio_file, pronunciation_data = files.load_files_for_topic(topic, paths, mode)

    script_lines = scripts.load_script(script_file, mode=mode)
    audio_segments = audio.load_audio_segments_for_mode(audio_file, mode, len(script_lines) if mode == "lines" else None)

    if mode == "lines" and len(audio_segments) != len(script_lines):
        print(f"Audio length: {len(audio_segments)} and script length: {len(script_lines)} may not match perfectly")

    index.shadowing_session(script_lines, audio_segments, pronunciation_data, mode)

if __name__ == "__main__":
    main()

