#!/bin/bash
# Renders the given shots one after another into renders/.
V=/tmp/claude-0/-home-user/c49c6d0e-4e59-5018-ad5e-54a418c19ff6/scratchpad/b3d/venv_python3.11/bin/python
HDR=/tmp/claude-0/-home-user/c49c6d0e-4e59-5018-ad5e-54a418c19ff6/scratchpad/pmndrs/hdr/apartment.exr
cd "$(dirname "$0")"
for s in "$@"; do
  start=$(date +%s)
  $V shot.py -- $s screens/$s $HDR renders > renders/$s.log 2>&1
  echo "$s: $(ls renders/${s}_[0-9]*.png 2>/dev/null | wc -l) frames in $(( $(date +%s) - start ))s"
done
