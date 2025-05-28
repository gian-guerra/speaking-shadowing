data = [
"Ethan: If we had caught that memory leak earlier, the app wouldn’t have crashed during the launch.",
"Carla: Exactly. And if QA had run a proper load test, we might have spotted it before Friday.",
"Ethan: Yeah… I should have double-checked the metrics dashboard after the last commit.",
"Carla: Honestly, we all missed it. But if we had communicated better with DevOps, they could have helped us flag it sooner.",
"Ethan: True. If I hadn’t skipped the daily stand-up, I would have known we were merging early.",
"Carla: And I could have reminded you too — that’s on me. If only we had slowed down a bit, the release would have gone smoothly.",
"Ethan: We learned the hard way. But at least we created an incident doc now — that should have happened a long time ago.",
]

def convert_to_ssml(data, output_file="conversation.ssml"):
    ssml_lines = ['<speak>']
    for line in data:
        ssml_lines.append(f"{line}<break time=\"1500ms\"/>")
    ssml_lines.append('</speak>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ssml_lines))

    print(f"✅ SSML file written to {output_file}")

if __name__ == "__main__":
    convert_to_ssml(data)

