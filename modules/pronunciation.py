import json

def load_pronunciation_data(pronunciation_path):
    with open(pronunciation_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_ipa_text(ipa_txt_path):
    with open(ipa_txt_path, "r", encoding="utf-8") as f:
        return f.read().strip()