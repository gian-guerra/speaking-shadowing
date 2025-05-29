import os
from pathlib import Path
import sys

# === Base Directories === 
SCRIPTS_DIR = Path("../scripts")
PRONUNCIATION_DIR = Path("../pronunciation")

def create_empty_json_files(section_name):
    section_input_dir = SCRIPTS_DIR / section_name
    section_output_dir = PRONUNCIATION_DIR / section_name

    if not section_input_dir.exists():
        print(f"❌ Section not found: {section_input_dir}")
        return

    os.makedirs(section_output_dir, exist_ok=True)

    txt_files = list(section_input_dir.glob("*.txt"))
    if not txt_files:
        print(f"⚠️ No .txt files found in {section_input_dir}")
        return

    print(f"📂 Creating .json files in: {section_output_dir}")

    for txt_file in txt_files:
        json_filename = txt_file.stem + ".json"
        json_path = section_output_dir / json_filename
        json_path.touch()  # Create an empty file
        print(f"✅ Created: {json_filename}")

    print("\n✅ Done!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_empty_jsons.py <section_name>")
        print("Example: python create_empty_jsons.py section1")
        sys.exit(1)

    section = sys.argv[1]
    create_empty_json_files(section)
