#!/bin/bash
# Cuts source.mov into g/%05d.jpg following timeline.json: frozen start under the hook, the game sped up, the result, frozen end card.
set -e
eval $(python3 -c "import json;d=json.load(open('timeline.json'));print(f\"TH={d['TH']:.3f} END={d['end']:.3f} E={d['end']-d['TE']:.3f} S={d['speed']} G0={d['g0']} G1={d['g1']} R1={d['r1']}\")")
mkdir -p g && rm -f g/*
ffmpeg -v error -y -i source.mov -filter_complex "\
[0:v]fps=30,delogo=x=290:y=795:w=185:h=56,scale=540:960,split=4[a][b][c][d];\
[a]trim=start=5.6:duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=$TH[s1];\
[b]trim=start=$G0:end=$G1,setpts=(PTS-STARTPTS)/$S,fps=30[s2];\
[c]trim=start=$G1:end=$R1,setpts=PTS-STARTPTS[s3];\
[d]trim=start=$(python3 -c "print($R1-0.05)"):duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=$E[s4];\
[s1][s2][s3][s4]concat=n=4:v=1:a=0,trim=duration=$END[v]" -map "[v]" -q:v 3 g/%05d.jpg
ls g | wc -l
