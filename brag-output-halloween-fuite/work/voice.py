# Cuts the ElevenLabs takes into their lines, places each on the video's timeline and ducks the score under it.
# python3 voice.py score.wav out.wav   (reads ../voice/take1.mp3 and ../voice/take2.mp3)
import subprocess, sys, wave
import numpy as np

SR = 48000

def load(path, ch):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)

# (take, [start, end] in it, from silencedetect at -42 dB) -> time in the video (matches CAPS in composition.html)
LINES = [
    ('take1', (0.00, 1.96), 0.80, 'Ahhh ! Les voyelles s’échappent !'),           # A, O, E, E jump out of HALLOWEEN
    ('take1', (3.57, 6.70), 3.30, 'Chaque jour, un nouveau mot… sans ses voyelles.'),  # they run off, the camera starts
    ('take1', (7.58, 9.00), 6.70, 'Viens nous aider à les retrouver !'),
    ('take1', (10.10, 11.98), 17.00, 'Regarde ! Elles retrouvent leur place !'),   # they dive towards the phone
    ('take1', (12.44, 13.43), 19.75, 'Halloween !'),                               # the word is complete
    ('take2', (14.40, 21.09), 22.40, 'Pour jouer, tape C. N. S. N. N. … Et c’est gratuit !'),  # second take: better CNSNN
]

takes = {k: load(f'../voice/{k}.mp3', 1)[:, 0] for k in ('take1', 'take2')}
score = load(sys.argv[1], 2)
n = len(score)
voice = np.zeros(n)
env = np.zeros(n)   # where the voice speaks, for ducking

def clip(take, a, b, pre=0.05, post=0.15):
    i, j = int(max(0, a - pre) * SR), int(min(len(take) / SR, b + post) * SR)
    x = take[i:j].copy(); f = int(0.012 * SR)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x

prev = 0
for src, (a, b), at, txt in LINES:
    x = clip(takes[src], a, b)
    i = int(max(0, at - 0.05) * SR); j = min(n, i + len(x))
    assert i >= prev, txt + ' overlaps the line before'
    assert j - i == len(x), txt + ' runs past the end of the video'
    voice[i:j] += x; env[i:j] = 1; prev = j

# Duck the score by 8 dB under the voice, 120 ms attack before each line, 400 ms release
k_att, k_rel = int(0.12 * SR), int(0.4 * SR)
duck = env.copy()
for i in np.flatnonzero(np.diff(np.concatenate([[0], env])) > 0):
    a = max(0, i - k_att); duck[a:i] = np.maximum(duck[a:i], np.linspace(0, 1, i - a))
for e in np.flatnonzero(np.diff(np.concatenate([env, [0]])) < 0):
    j = min(n, e + k_rel); duck[e:j] = np.maximum(duck[e:j], np.linspace(1, 0, j - e))
gain = 10 ** (-8 * duck / 20)

voice *= 0.5 / np.max(np.abs(voice))
mix = score * gain[:, None] * 0.55 + voice[:, None]
mix *= 0.95 / np.max(np.abs(mix))
with wave.open(sys.argv[2], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
for _, _, at, txt in LINES: print(f'{at:6.2f}s  {txt}')
