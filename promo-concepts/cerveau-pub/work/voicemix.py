# Places the lines of the shared ElevenLabs take on a video's timeline and ducks the score under them.
# python3 voicemix.py take.mp3 score.wav out.wav lines.json   (lines.json: [[start, end, at, "text"], ...], seconds)
import json, subprocess, sys, wave
import numpy as np

SR = 48000

def load(path, ch):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)

take, score = load(sys.argv[1], 1)[:, 0], load(sys.argv[2], 2)
LINES = json.load(open(sys.argv[4]))
n = len(score); voice = np.zeros(n); env = np.zeros(n)
prev = 0
for a, b, at, txt in LINES:
    i0, j0 = int(max(0, a - 0.05) * SR), int(min(len(take) / SR, b + 0.15) * SR)
    x = take[i0:j0].copy(); f = int(0.012 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    i = int(max(0, at - 0.05) * SR); j = i + len(x)
    assert i >= prev, txt + ' overlaps the line before'
    assert j <= n, txt + ' runs past the end of the video'
    voice[i:j] += x; env[i:j] = 1; prev = j
# duck the score by 8 dB under the voice: 120 ms attack before each line, 400 ms release
k_att, k_rel = int(0.12 * SR), int(0.4 * SR)
duck = env.copy()
for i in np.flatnonzero(np.diff(np.concatenate([[0], env])) > 0):
    a = max(0, i - k_att); duck[a:i] = np.maximum(duck[a:i], np.linspace(0, 1, i - a))
for e in np.flatnonzero(np.diff(np.concatenate([env, [0]])) < 0):
    j = min(n, e + k_rel); duck[e:j] = np.maximum(duck[e:j], np.linspace(1, 0, j - e))
voice *= 0.5 / np.max(np.abs(voice))
mix = score * (10 ** (-8 * duck / 20))[:, None] * 0.55 + voice[:, None]
mix *= 0.95 / np.max(np.abs(mix))
with wave.open(sys.argv[3], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
for a, b, at, txt in LINES: print(f'{at:6.2f}–{at + b - a:5.2f}s  {txt}')
