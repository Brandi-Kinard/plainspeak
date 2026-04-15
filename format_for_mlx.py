"""
Convert training pairs to MLX LoRA format.
MLX expects: {"text": "### Original:\n...\n\n### Plain English:\n..."}
Also creates an 80/10/10 train/valid/test split.
"""

import json, random
from pathlib import Path

input_path = Path("data/processed/training_pairs.jsonl")

pairs = []
with open(input_path) as f:
    for line in f:
        item = json.loads(line)
        formatted = {
            "text": f"### Original:\n{item['original']}\n\n### Plain English:\n{item['plain']}"
        }
        pairs.append(formatted)

random.seed(42)
random.shuffle(pairs)

n = len(pairs)
train_end = int(n * 0.8)
valid_end = int(n * 0.9)

splits = {
    "data/train/train.jsonl": pairs[:train_end],
    "data/valid/valid.jsonl": pairs[train_end:valid_end],
    "data/test/test.jsonl": pairs[valid_end:],
}

Path("data/test").mkdir(exist_ok=True)

for path, split in splits.items():
    with open(path, "w") as f:
        for item in split:
            f.write(json.dumps(item) + "\n")
    print(f"Wrote {len(split)} examples → {path}")

print("\nSample training record:")
print(pairs[0]["text"][:400])