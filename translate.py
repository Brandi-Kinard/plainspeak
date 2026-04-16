#!/usr/bin/env python3
"""
PlainSpeak CLI — Dense-to-Plain-English Translator
Usage: python translate.py "Your dense text here"
       echo "Your text" | python translate.py
"""

import sys
from mlx_lm import load, generate

MODEL_PATH = "plainspeak-model"

def translate(text: str) -> str:
    model, tokenizer = load(MODEL_PATH)
    prompt = f"### Original:\n{text.strip()}\n\n### Plain English:"
    result = generate(model, tokenizer, prompt=prompt, max_tokens=200, verbose=False)
    output = result.strip()
    if "### " in output:
        output = output.split("### ")[0].strip()
    return output

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("PlainSpeak — Dense-to-Plain-English Translator")
        print("Usage: python translate.py \"Your text here\"")
        print("       echo \"Your text\" | python translate.py")
        sys.exit(0)

    print("\nTranslating...\n")
    result = translate(text)
    print(f"Plain English:\n{result}\n")

if __name__ == "__main__":
    main()