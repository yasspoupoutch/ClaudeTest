#!/bin/bash
# Joins the 2x chunks, scales them down to 1080x1920 (Lanczos) and adds the voice + score mix.
set -e; cd "$(dirname "$0")/.."
ls out/chunks/c_*.mp4 | grep -v tmp | sed "s/^out\/chunks\//file '/; s/$/'/" > out/chunks/list.txt
ffmpeg -v error -y -f concat -safe 0 -i out/chunks/list.txt -i sound/mix_norm.wav -map 0:v -map 1:a \
  -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart -shortest cnsnn-promo-3d.mp4
ffmpeg -v error -y -ss 20.8 -i cnsnn-promo-3d.mp4 -frames:v 1 -q:v 2 cnsnn-promo-3d.jpg
ffprobe -v error -show_entries format=duration -of csv=p=0 cnsnn-promo-3d.mp4
