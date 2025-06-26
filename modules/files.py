import os
from modules import pronunciation

def list_files(directory, extension=None):
    files = [f for f in os.listdir(directory) if not extension or f.endswith(extension)]
    return files

def select_topic(directory, extension=".txt"):
    files = list_files(directory, extension)
    if not files:
        print(f"No {extension} files found in {directory}")
        return None

    topics = [os.path.splitext(f)[0] for f in files]
    print("\nAvailable topics:")
    for idx, topic in enumerate(topics, start=1):
        print(f"{idx}. {topic}")

    while True:
        try:
            choice = int(input("Select a topic by number: "))
            if 1 <= choice <= len(topics):
                return topics[choice - 1]
        except ValueError:
            pass
        print("Invalid selection. Please enter a valid number.")

def load_files_for_topic(topic, paths, mode):
    script_file = os.path.join(paths["script"], f"{topic}.txt")
    audio_file = os.path.join(paths["audio"], f"{topic}.mp3")

    if mode == "lines":
        pronunciation_file = os.path.join(paths["pronunciation"], f"{topic}.json")
        pronunciation_data = pronunciation.load_pronunciation_data(pronunciation_file)
    else:
        pronunciation_file = os.path.join(paths["pronunciation"], f"{topic}.txt")
        ipa_text = pronunciation.load_ipa_text(pronunciation_file)
        pronunciation_data = [{"ipa": ipa_text}]

    return script_file, audio_file, pronunciation_data