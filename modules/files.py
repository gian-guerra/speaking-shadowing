import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

def list_files(directory, extension=None):
    print(project_root)
    files = [f for f in os.listdir(project_root / directory) if not extension or f.endswith(extension)]
    return files
    
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
                return os.path.join(project_root / directory, files[choice-1])
        except ValueError:
            pass
        print("Invalid selection. Please enter a valid number")