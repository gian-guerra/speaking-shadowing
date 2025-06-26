from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

def getPaths(sectionToPractice):
    scripts_path = project_root / f"scripts/{sectionToPractice}"
    audios_path = project_root / f"audios/{sectionToPractice}"
    pronunciation_path = project_root / f"pronunciation/{sectionToPractice}"
    return {"script": scripts_path, "audio": audios_path, "pronunciation": pronunciation_path}

def printMultipleLines(lines):
    for _, line in enumerate(lines):
        print(line)