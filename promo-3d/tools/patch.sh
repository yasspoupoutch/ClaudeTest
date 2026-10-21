#!/bin/bash
# Re-renders frame ranges and splices them into out/promo_silent.mp4: tools/patch.sh 189-330 450-614
set -e; cd "$(dirname "$0")/.."
args=()
for r in "$@"; do
  npx remotion render src/index.ts Promo out/part_$r.mp4 --frames=$r --crf=16 --log=error 2>&1 | grep -vE "memory|Memory|docker|CGroup|lower amount|^\s*$|THREE\." || true
done
# Build the splice: keep original frames outside the patched ranges
python3 - "$@" <<'PY'
import sys, subprocess
total = 615; ranges = sorted(tuple(map(int, r.split('-'))) for r in sys.argv[1:])
inputs = ['-i', 'out/promo_silent.mp4']; parts = []; cur = 0; n = 1
for a, b in ranges:
    if cur < a: parts.append(f"[0:v]trim=start_frame={cur}:end_frame={a},setpts=PTS-STARTPTS[s{len(parts)}]")
    inputs += ['-i', f'out/part_{a}-{b}.mp4']; parts.append(f"[{n}:v]setpts=PTS-STARTPTS[s{len(parts)}]"); n += 1; cur = b + 1
if cur < total: parts.append(f"[0:v]trim=start_frame={cur}:end_frame={total},setpts=PTS-STARTPTS[s{len(parts)}]")
fc = ';'.join(parts) + ';' + ''.join(f'[s{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=0[v]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', *inputs, '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', 'out/promo_silent_new.mp4'], check=True)
PY
mv out/promo_silent_new.mp4 out/promo_silent.mp4
ffmpeg -loglevel error -y -i out/promo_silent.mp4 -i sound/score.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 44100 -c:a aac -b:a 192k -movflags +faststart -shortest out/promo.mp4
echo "frames: $(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 out/promo.mp4)"
