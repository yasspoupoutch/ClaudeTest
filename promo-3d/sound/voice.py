# Cuts the ElevenLabs take into its lines, places each on the video's timeline and ducks the score under it.
# python3 voice.py take.mp3 intro.mp3 score.wav out.wav  (intro.mp3: second take of the opening, letters + "Hmmm ?" + question)
import subprocess, sys, wave
import numpy as np

SR = 48000

def load(path, ch):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).astype(np.float64)

# (take, [start, end] in it, seconds from the level meter) -> time in the video
LINES = [
    ('intro', (0.03, 3.40), 0.00, 'C. H. C. R. T.'),        # CHCRT on screen, slots, typing
    ('intro', (3.88, 4.92), 3.60, 'Hmmm ?'),
    ('intro', (5.63, 6.48), 4.90, 'Tu trouves les voyelles ?'),   # just as the neon starts round the card
    ('take', (6.69, 7.89), 5.95, 'Chaque jour, un mot.'),        # neon loop, the card lifts
    ('take', (8.31, 9.52), 7.40, 'Le même pour tout le monde.'),
    ('take', (10.08, 10.82), 8.85, 'Choucroute !'),          # just after the last vowel lands
    ('take', (11.34, 13.20), 9.85, 'Trente-huit secondes. Du premier coup.'),  # the card flips to its result
    ('take', (13.80, 14.38), 11.95, 'Sprint.'),              # camera on each mode card
    ('take', (15.39, 15.96), 12.95, 'Survie.'),
    ('take', (16.77, 17.65), 14.15, 'Double sens.'),
    ('take', (18.18, 19.16), 15.45, 'Et tes amis à battre.'),  # leaderboard
    ('take', (19.76, 22.37), 18.45, 'Consonne. Le mot du jour, sans ses voyelles.'),  # CONSONNE is complete, then the tagline
    ('take', (22.95, 24.53), 21.45, 'Gratuit, sur l\'App Store.'),
]

takes = {'take': load(sys.argv[1], 1)[:, 0], 'intro': load(sys.argv[2], 1)[:, 0]}
score = load(sys.argv[3], 2)
n = len(score)
voice = np.zeros(n)
env = np.zeros(n)   # where the voice speaks, for ducking

def clip(take, a, b, pre=0.05, post=0.15):
    i, j = int(max(0, a - pre) * SR), int(min(len(take) / SR, b + post) * SR)
    x = take[i:j].copy(); f = int(0.012 * SR)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x

prev = 0.0
for src, (a, b), at, txt in LINES:
    x = clip(takes[src], a, b)
    i = int(max(0, at - 0.05) * SR); j = min(n, i + len(x))
    assert i >= prev, txt + ' overlaps the line before'
    voice[i:j] += x[:j - i]; env[i:j] = 1; prev = j

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
with wave.open(sys.argv[4], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes())
for _, _, at, txt in LINES: print(f'{at:6.2f}s  {txt}')
