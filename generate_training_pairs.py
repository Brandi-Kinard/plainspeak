"""
PlainSpeak — Training Pair Generator
Sends each Gutenberg passage to Claude, gets plain English version back.
Output: JSONL ready for MLX fine-tuning.
"""

import anthropic
import json
import time
from pathlib import Path

client = anthropic.Anthropic()

PROMPT_TEMPLATE = """Rewrite the following passage in plain, modern English that a 16-year-old would understand. Keep the meaning exactly the same. Do not add or remove information. Use short sentences. Avoid fancy words. Do not add any introduction or explanation — just give the rewritten passage directly.

Original:
{passage}

Plain English version:"""

def generate_plain_english(passage: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",  # cheapest, fast enough
        max_tokens=512,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(passage=passage)}]
    )
    return message.content[0].text.strip()

def main():
    input_path = Path("data/raw/gutenberg_sample.jsonl")
    output_path = Path("data/processed/training_pairs.jsonl")
    output_path.parent.mkdir(exist_ok=True)

    passages = []
    with open(input_path) as f:
        for line in f:
            passages.append(json.loads(line)["text"])

    print(f"Loaded {len(passages)} passages")
    print("Generating plain English versions...\n")

    pairs = []
    for i, passage in enumerate(passages):
        try:
            plain = generate_plain_english(passage)
            pair = {"original": passage, "plain": plain}
            pairs.append(pair)

            # Print progress
            print(f"[{i+1}/{len(passages)}] Done")
            if i == 0:
                print(f"\nSample output:\nORIGINAL: {passage[:150]}...\nPLAIN: {plain[:150]}...\n")

            # Save incrementally — don't lose progress if it crashes
            with open(output_path, "w") as f:
                for p in pairs:
                    f.write(json.dumps(p) + "\n")

            # Rate limit buffer
            time.sleep(0.5)

        except Exception as e:
            print(f"[{i+1}] ERROR: {e}")
            time.sleep(2)
            continue

    print(f"\nDone. {len(pairs)} pairs saved to {output_path}")

if __name__ == "__main__":
    main()