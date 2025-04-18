from pydub import AudioSegment
from pydub.playback import play

script = [
"Junior Dev: Hey! I’ve just pushed the refactored module. I tried to keep the functions small and clear, like you suggested.",
"You: Nice job! I’ve taken a quick look — it’s definitely cleaner. You’ve improved a lot since your first pull request.",
"Junior Dev: Thanks! I’ve been practicing every day. Honestly, I didn’t even know what “clean code” meant when I joined.",
"You: Totally get it. When I started out, I used to write 500-line functions without thinking twice. I would just try to make it work and ship it.",
"Junior Dev: Haha, I’ve done that too. I had written a class last month with almost 800 lines… It was a nightmare to debug.",
"You: Trust me, we’ve all been there. Before we adopted code reviews, people would push straight to main. Things used to break constantly.",
"Junior Dev: Yeah, I’ve heard about those days. So chaotic!",
"You: Yeah. But it’s been much better lately. The team has been focusing on writing more testable components. And since we moved to GitHub Actions, our pipelines have been running faster and more reliably.",
"Junior Dev: That explains why my builds have been so smooth. I had been struggling with the old CI configs before that switch.",
"You: Same here. I had spent hours debugging build failures last year. Now I barely think about it.",
"Junior Dev: I feel like my understanding of Git has improved too. I’ve finally understood how rebase works — kind of.",
"You: Oh man, rebasing. It used to terrify me. I would always prefer merging to avoid conflicts, even if it made the history messy.",
"Junior Dev: Exactly! That’s still me sometimes. But I’ve been practicing with dummy branches just to get comfortable.",
"You: That’s the way. And it shows — your last rebase was super clean. Keep doing what you’ve been doing."
]

audio_file = r"\path\file"
print(AudioSegment.ffmpeg)
audio = AudioSegment.from_file(audio_file)

segment_duration = len(audio) // len(script)
segments = [audio[i*segment_duration:(i+1)*segment_duration] for i in range(len(script))]

print("\n🎧 Shadowing Session Started")
print("Instructions: [r]epeat | [n]ext | [q]uit\n")

for i, line in enumerate(script):
    while True:
        print(f"\n📢 {line}")
        play(segments[i])

        cmd = input(">> [r]epeat | [n]ext | [q]uit: ").strip().lower()
        if cmd == 'n':
            break
        elif cmd == 'q':
            print("👋 Exiting. Keep practicing!")
            exit()
        elif cmd == 'r':
            continue
        else:
            print("❓ Invalid input. Please use r/n/q.")
