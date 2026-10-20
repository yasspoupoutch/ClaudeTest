#!/bin/bash
# Edits the rendered shots into the final video: open, chat, type, mock, rewind (mock+type backwards),
# "Et si…", app, revenge, end card. Shots are rendered at 67% and scaled to 1080x1920 here.
set -e; cd "$(dirname "$0")"
rm -rf edit && mkdir -p edit
i=0
put() { i=$((i+1)); cp "$1" "edit/f$(printf %04d $i).png"; }
for s in open chat type mock; do for f in renders/${s}_[0-9]*.png; do put "$f"; done; done
# Rewind: mock then type played backwards fast (every 9th frame), 0.8 s
mapfile -t back < <(ls renders/type_[0-9]*.png renders/mock_[0-9]*.png | sort -r)
for ((k=0; k<${#back[@]} && k/9<24; k+=9)); do put "${back[$k]}"; done
rw_end=$i
# "Et si…": first frame of the typing shot held 0.9 s
for k in $(seq 27); do put renders/type_0001.png; done
etsi_end=$i
for s in app revenge; do for f in renders/${s}_[0-9]*.png; do put "$f"; done; done
shots_end=$i
for f in overlays/end/e*.png; do put "$f"; done
n_open=$(ls renders/open_[0-9]*.png | wc -l); n_chat=$(ls renders/chat_[0-9]*.png | wc -l)
n_type=$(ls renders/type_[0-9]*.png | wc -l); n_mock=$(ls renders/mock_[0-9]*.png | wc -l)
rw_start=$((n_open + n_chat + n_type + n_mock + 1))
# Rewind look (blur, desaturate) + icon during the rewind, darkened frame + "Et si…" after
ffmpeg -loglevel error -y -framerate 30 -i edit/f%04d.png -i overlays/rewind.png -i overlays/etsi.png -i audio.wav -filter_complex "
  [0]scale=1080:1920:flags=lanczos,setsar=1,split=2[v][w];
  [w]boxblur=4:1,eq=saturation=0.55:contrast=1.08[blur];
  [v][blur]overlay=enable='between(n,$((rw_start-1)),$((rw_end-1)))'[a];
  [a]eq=brightness=-0.18:enable='between(n,$rw_end,$((etsi_end-1)))'[b];
  [b][1]overlay=enable='between(n,$((rw_start-1)),$((rw_end-1)))'[c];
  [c][2]overlay=enable='between(n,$rw_end,$((etsi_end-1)))'[d];
  [d]noise=alls=4:allf=t,unsharp=5:5:0.5,format=yuv420p[out]" \
  -map "[out]" -map 3:a -c:v libx264 -preset slow -crf 17 -profile:v high -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 44100 -c:a aac -b:a 192k -movflags +faststart -shortest ../brag.mp4
echo "frames=$i duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ../brag.mp4)"
