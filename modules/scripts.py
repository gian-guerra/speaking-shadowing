import re

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"

def format_line(line):
    return re.sub(r"\{(.*?)\}", f"{BOLD}{BLUE}\\1{RESET}", line)

def load_script(script_path, mode="lines", ipa_path=None):
    if mode == "chunk-paired":
        with open(script_path, "r", encoding="utf-8") as f1, open(ipa_path, "r", encoding="utf-8") as f2:
            script_lines = [line.strip() for line in f1 if line.strip()]
            ipa_lines = [line.strip() for line in f2 if line.strip()]
            combined_lines = [f"{format_line(s)}\n{GREEN}{ipa}{RESET}" for s, ipa in zip(script_lines, ipa_lines)]
            return ["\n".join(combined_lines)]
    else:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if mode == "chunk":
                return [format_line(content)]
            return [format_line(line.strip()) for line in content.splitlines() if line.strip()]