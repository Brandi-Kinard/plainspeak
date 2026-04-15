from datasets import load_dataset
import json, re

print("Loading Gutenberg sample (streaming)...")
dataset = load_dataset(
    "manu/project_gutenberg",
    split="en",
    streaming=True
)

def is_good_prose(text):
    """Filter out metadata, headers, and noise."""
    noise_signals = [
        "www.gutenberg.org",
        "Project Gutenberg",
        "Release Date:",
        "Character set encoding",
        "Proofreading Team",
        "CHAPTER",
        "CONTENTS",
        "[Illustration",
        "***START",
        "*** START",
        "Copyright,",
        "http://",
    ]
    for signal in noise_signals:
        if signal in text:
            return False
    # Must have sentence-like structure (periods, not just ALL CAPS titles)
    if len(re.findall(r'[.!?]', text)) < 3:
        return False
    # Reject if too many caps (title/header blocks)
    words = text.split()
    caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 2) / max(len(words), 1)
    if caps_ratio > 0.2:
        return False
    return True

passages = []
checked = 0
for item in dataset:
    checked += 1
    text = item.get("text", "")
    words = text.split()
    if len(words) > 300:
        # Try a few different windows to find prose, not preamble
        for start in [100, 200, 300]:
            chunk = " ".join(words[start:start+200])
            if is_good_prose(chunk):
                passages.append(chunk)
                break
    if len(passages) >= 1500:
        break
    if checked > 5000:  # safety limit
        break

print(f"Checked {checked} books, extracted {len(passages)} clean passages")

with open("data/raw/gutenberg_sample.jsonl", "w") as f:
    for p in passages:
        f.write(json.dumps({"text": p}) + "\n")

print("Done. Saved to data/raw/gutenberg_sample.jsonl")
print("\nSample passage:")
print(passages[0][:300] if passages else "None")