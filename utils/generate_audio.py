import boto3
import os
import sys
import re
from pathlib import Path

# === CONFIGURATION ===
SCRIPTS_DIR = Path("../scripts")
AUDIOS_DIR = Path("../audios")
VOICE_ID = "Stephen"
ENGINE = "generative"

def read_lines_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def clean_line(text):
    return text.replace("{", "").replace("}", "").strip()

def generate_ssml(lines):
    ssml_lines = ['<speak>']
    for line in lines:
        cleaned = clean_line(line)
        if cleaned:
            ssml_lines.append(f"{cleaned}<break time=\"1500ms\"/>")
    ssml_lines.append('</speak>')
    return '\n'.join(ssml_lines)

def synthesize_speech(ssml_text, output_path, voice_id, engine):
    polly = boto3.client("polly")

    response = polly.synthesize_speech(
        TextType="ssml",
        Text=ssml_text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine=engine
    )

    if "AudioStream" in response:
        with open(output_path, "wb") as f:
            f.write(response["AudioStream"].read())
        print(f"✅ Saved: {output_path.name}")
    else:
        raise RuntimeError(f"❌ Polly failed for: {output_path.name}")

def process_section(section_name):
    section_input_dir = SCRIPTS_DIR / section_name
    section_output_dir = AUDIOS_DIR / section_name

    if not section_input_dir.exists():
        print(f"❌ Section folder not found: {section_input_dir}")
        return

    os.makedirs(section_output_dir, exist_ok=True)

    txt_files = list(section_input_dir.glob("*.txt"))
    if not txt_files:
        print(f"⚠️ No .txt files found in {section_input_dir}")
        return

    print(f"🔄 Processing {len(txt_files)} files in section '{section_name}'...")

    for i, txt_file in enumerate(txt_files, 1):
        lines = read_lines_from_file(txt_file)
        ssml_text = generate_ssml(lines)
        output_filename = txt_file.stem + ".mp3"
        output_path = section_output_dir / output_filename

        print(f"🔊 [{i}/{len(txt_files)}] Converting: {txt_file.name}")
        try:
            synthesize_speech(ssml_text, output_path, VOICE_ID, ENGINE)
        except Exception as e:
            print(f"❌ Error with {txt_file.name}: {e}")

    print(f"\n✅ Done! All audios saved in: {section_output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_batch.py <section_folder>")
        print("Example: python generate_batch.py section1")
        sys.exit(1)

    section_name = sys.argv[1]
    process_section(section_name)
