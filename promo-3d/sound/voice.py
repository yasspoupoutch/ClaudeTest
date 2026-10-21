# Cuts the ElevenLabs take into its lines, places each on the video's timeline and ducks the score under it.
# python3 voice.py take.mp3 score.wav out.wav
import subprocess, sys, wave
import numpy as np

SR = 48000

def load(path, ch):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)

# [start, end] in the take (seconds, from silencedetect at -40 dB) -> time in the video
LINES = [
    ((0.00, 3.61), 0.20, 'C… H… C… R… T.'),          # letters tightened below
    ((4.94, 5.72), 3.30, 'Tu trouves les voyelles ?'),
    ((6.69, 9.52), 4.85, 'Chaque jour, un mot. Le même pour tout le monde.'),   # over the neon loop and the card lift
    ((10.08, 10.82), 8.60, 'Choucroute !'),          # as the last vowel lands
    ((11.34, 13.20), 9.60, 'Trente-huit secondes. Du premier coup.'),            # the card flips to its result
    ((13.80, 14.38), 11.75, 'Sprint.'),              # camera on each mode card
    ((15.39, 15.96), 12.95, 'Survie.'),
    ((16.77, 17.65), 14.15, 'Double sens.'),
    ((18.18, 19.16), 15.45, 'Et tes amis à battre.'),  # leaderboard
    ((19.76, 22.37), 18.45, 'Consonne. Le mot du jour, sans ses voyelles.'),    # CONSONNE is complete, then the tagline
    ((22.95, 24.53), 21.45, 'Gratuit, sur l\'App Store.'),
]
# Letter line: gaps between letters in the take (start, end), each shortened to GAP seconds
LETTER_GAPS = [(0.50, 1.03), (1.50, 1.95), (2.24, 2.72), (3.03, 3.46)]
GAP = 0.28

take, score = load(sys.argv[1], 1)[:, 0], load(sys.argv[2], 2)
n = len(score)
voice = np.zeros(n)
env = np.zeros(n)   # where the voice speaks, for ducking

def clip(a, b, pre=0.05, post=0.15):
    i, j = int(max(0, a - pre) * SR), int(min(len(take) / SR, b + post) * SR)
    x = take[i:j].copy(); f = int(0.012 * SR)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x

for (a, b), at, _ in LINES:
    if a == 0.0:
        bounds = [a] + [v for g in LETTER_GAPS for v in g] + [b]
        parts = [clip(bounds[k], bounds[k + 1], 0.03, 0.08) for k in range(0, len(bounds), 2)]
        x = np.concatenate([np.concatenate([p, np.zeros(int(max(0, GAP - 0.11) * SR))]) for p in parts])
    else:
        x = clip(a, b)
    i = int(at * SR); j = min(n, i + len(x))
    voice[i:j] += x[:j - i]; env[i:j] = 1

# Duck the score by 8 dB under the voice, 120 ms attack before each line, 400 ms release
k_att, k_rel = int(0.12 * SR), int(0.4 * SR)
duck = env.copy()
idx = np.flatnonzero(np.diff(np.concatenate([[0], env])) > 0)
for i in idx: duck[max(0, i - k_att):i] = np.maximum(duck[max(0, i - k_att):i], np.linspace(0, 1, i - max(0, i - k_att)))
ends = np.flatnonzero(np.diff(np.concatenate([env, [0]])) < 0)
for e in ends: j = min(n, e + k_rel); duck[e:j] = np.maximum(duck[e:j], np.linspace(1, 0, j - e))
gain = 10 ** (-8 * duck / 20)

voice *= 0.5 / np.max(np.abs(voice))
mix = score * gain[:, None] * 0.55 + voice[:, None] * 1.0
mix *= 0.95 / np.max(np.abs(mix))
with wave.open(sys.argv[3], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
for (a, b), at, txt in LINES: print(f'{at:6.2f}s  {txt}')
