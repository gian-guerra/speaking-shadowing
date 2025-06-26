import re

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"

def format_line(line):
    return re.sub(r"\{(.*?)\}", f"{BOLD}{BLUE}\\1{RESET}", line)

def load_script(script_path, mode="lines"):
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if mode == "chunk":
            return [format_line(content)]
        return [format_line(line.strip()) for line in content.splitlines() if line.strip()]