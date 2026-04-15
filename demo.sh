#!/bin/bash

source /Users/brandiellenkinard/sovereign-geek/plainspeak/venv/bin/activate

clear

echo "
 ██████╗ ██╗      █████╗ ██╗███╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗  ██╗
 ██╔══██╗██║     ██╔══██╗██║████╗  ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
 ██████╔╝██║     ███████║██║██╔██╗ ██║███████╗██████╔╝█████╗  ███████║█████╔╝ 
 ██╔═══╝ ██║     ██╔══██║██║██║╚██╗██║╚════██║██╔═══╝ ██╔══╝  ██╔══██║██╔═██╗ 
 ██║     ███████╗██║  ██║██║██║ ╚████║███████║██║     ███████╗██║  ██║██║  ██╗
 ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

 Dense-to-Plain-English Translator · SmolLM2-1.7B · Runs 100% Local
"

sleep 3

echo "─────────────────────────────────────────────────────────"
echo " King James Bible · Genesis 1:1-2"
echo "─────────────────────────────────────────────────────────"
echo ""
echo " In the beginning God created the heaven and the earth."
echo " And the earth was without form, and void; and darkness"
echo " was upon the face of the deep."
echo ""
echo "─────────────────────────────────────────────────────────"
echo " Plain English"
echo "─────────────────────────────────────────────────────────"
echo ""

mlx_lm.generate \
  --model plainspeak-model \
  --prompt "### Original:
In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep.

### Plain English:" \
  --max-tokens 60

echo ""
echo " github.com/Brandi-Kinard/plainspeak"
echo ""