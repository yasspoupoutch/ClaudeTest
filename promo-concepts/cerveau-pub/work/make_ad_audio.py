# Builds the soundtrack of one ad cut: the body music cut like the picture (CUTS in composition.html),
# the ad end-card cues, then the voice lines of voice_<cut>.json. python3 make_ad_audio.py 6|15|25
import json, subprocess, sys, wave
import numpy as np
from synth import *

CUTS = {   # same as composition.html: body segments [out start, out end, source start], end-card start, cues, duration
    25: dict(segs=[[0, 18.1, 0]], end=18.1, cues=dict(search=0.75, consonne=4.1, free=5.6), dur=25.4),
    15: dict(segs=[[0, 6.9, 0], [6.9, 11.55, 12.0]], end=11.55, cues=dict(search=0.9, consonne=0.5, free=1.8), dur=15.0),
    6: dict(segs=[[0, 1.8, 0], [1.8, 3.3, 2.6]], end=3.3, cues=dict(search=0.7, consonne=0.35, free=1.3), dur=6.0),
}
cut = int(sys.argv[1]); C = CUTS[cut]
subprocess.run(['python3', 'music.py', 'score_body.wav', 'body'], check=True)
with wave.open('score_body.wav') as w: sr = w.getframerate(); body = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2) / 32768
M = Mix(C['dur'], seed=cut)
segs = C['segs'] + [[C['end'], C['dur'], C['segs'][-1][2] + C['end'] - C['segs'][-1][0]]]   # the music runs on under the end card
fade = int(0.015 * SR)
for a, b, src in segs:
    x = body[int(src * sr):int((src + b - a) * sr) + fade].copy()
    x[:fade] *= np.linspace(0, 1, fade)[:, None]; x[-fade:] *= np.linspace(1, 0, fade)[:, None]
    i = int(a * SR); j = min(M.n, i + len(x)); M.buf[i:j] += x[:j - i] * 1.6
# end card: a whoosh, a bell per vowel back into CONSONNE, a chime and a chord on "gratuit"
e, c = C['end'], C['cues']
M.place(whoosh(M, 0.5), e - 0.25, 0.08)
for i, m in enumerate([76, 79, 83]): M.place(bell(m, 0.9), e + c['consonne'] + 0.1 + i * 0.15, 0.06)
M.place(blip(84, dur=0.08), e + c['search'], 0.04)
M.place(blip(88, dur=0.08), e + c['free'], 0.06); M.place(blip(95, dur=0.1), e + c['free'] + 0.12, 0.05)
for m in [40, 52, 59, 64, 67, 71]: M.place(tone(hz(m), 2.5, ((1, 1), (2, .2), (3, .06)), a=0.01, tau=1.3, det=0.002), e + c['free'], 0.035)
M.write(f'score_{cut}.wav', fade_out=0.6)
subprocess.run(['python3', 'voicemix.py', '../../voice/take.mp3', f'score_{cut}.wav', f'audio_{cut}.wav', f'voice_{cut}.json'], check=True)
