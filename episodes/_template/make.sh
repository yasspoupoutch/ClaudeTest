#!/bin/bash
# make.sh <episode dir with ep.json> : renders <dir>/video.mp4 from this template
set -e; T=$(cd "$(dirname "$0")" && pwd); D=$(cd "$1" && pwd); W=$D/work
mkdir -p $W; cp -r $T/{appicon.png,base.css,lib.js,render.mjs,synth.py,fonts,composition.html,music.py} $W/
echo "const EP = $(cat $D/ep.json);" > $W/ep.js
N=$(python3 -c "import json;print(len(json.load(open('$D/ep.json'))['rounds']))"); DUR=$(python3 -c "print(2.4+4.6*$N+4.5)")
cd $W; rm -rf frames; node render.mjs frames $DUR; python3 music.py audio.wav $D/ep.json
ffmpeg -y -v error -framerate 30 -i frames/f%04d.jpg -i audio.wav -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k -af loudnorm=I=-14:TP=-1.5 -shortest -movflags +faststart $D/video.mp4
rm -rf frames; echo "$D/video.mp4 $DUR s"
