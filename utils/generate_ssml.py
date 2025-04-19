import html

data = [
    "Teammate: Hey, did you get a chance to review my PR for the payment validation bug?",
    "You: Yeah, I’ve just finished going through it. Honestly, I think you nailed it. The fix was clean. How long had the bug been affecting users?",
    "Teammate: Since last week, I believe. I had been debugging it for three days straight before I figured out it wasn’t our code — it was a third-party API returning bad data.",
    "You: Damn. That’s rough. I’ve been in that situation. I remember a time when we had a similar issue — we had used a third-party service that silently failed, and we didn't realize for weeks.",
    "Teammate: Right! We used to log errors but didn’t really monitor them. We would check logs only if something broke completely.",
    "You: Yeah, those were the early days. We would deploy without automated tests too. I can’t believe how far we’ve come.",
    "Teammate: Absolutely. I’ve actually been working on improving our logging system since last sprint. I’ve added trace IDs to help track issues across services — it’s been really useful.",
    "You: That’s smart. And it shows — I’ve noticed we’ve been solving bugs faster lately. I’ve been more productive too since I switched to using the new feature flags library.",
    "Teammate: I heard about that! You’ve been experimenting with it for a while, haven’t you?",
    "You: Yeah, I had started testing it before our last release. By the time the sprint started, I had already written some wrappers to integrate it smoothly.",
    "Teammate: That’s cool. So overall, how’s your week been?",
    "You: Pretty good. I’ve been focusing on documentation. I’ve written more internal docs this week than in the last three months combined.",
    "Teammate: Haha, I used to hate writing docs, but now I kind of enjoy it. It’s satisfying to make things clear for others.",
    "You: Same. Honestly, I would write more if I had time. But you know how it is — meetings, sprint planning, code reviews...",
]

def convert_to_ssml(data, output_file="conversation.ssml"):
    ssml_lines = ['<speak>']
    for line in data:
        safe_line = html.escape(line)
        ssml_lines.append(f"{safe_line}<break time=\"1000ms\"/>")
    ssml_lines.append('</speak>')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ssml_lines))

    print(f"✅ SSML file written to {output_file}")

if __name__ == "__main__":
    convert_to_ssml(data)

