#!/bin/bash
# Renders the promo at 2x in 60-frame chunks (out/chunks/c_<first>.mp4), skipping chunks already done,
# so a restart of the machine only loses the chunk in progress. Then: tools/finish.sh
cd "$(dirname "$0")/.." && mkdir -p out/chunks
TOTAL=699; STEP=60
for ((a = 0; a < TOTAL; a += STEP)); do
  b=$((a + STEP - 1)); ((b >= TOTAL)) && b=$((TOTAL - 1))
  f=$(printf 'out/chunks/c_%03d.mp4' $a)
  [ -s "$f" ] && continue
  ./node_modules/.bin/remotion render src/index.ts Promo "$f.tmp.mp4" --frames=$a-$b --log=error --crf=14 --scale=2 && mv "$f.tmp.mp4" "$f"
  echo "$(date +%T) frames $a-$b done"
done
echo "all chunks done"
