import numpy as np, wave, sys
SR = 44100; DUR = 21.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
mix = np.zeros((N, 2))
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i >= N or j <= i: return
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:j, 0] += sig[:j - i] * gain * l * 1.414
    mix[i:j, 1] += sig[:j - i] * gain * r * 1.414
def env(n, a, d_tau):
    t = np.arange(n) / SR; e = np.exp(-t / d_tau); ai = int(a * SR)
    if ai > 0: e[:ai] *= np.linspace(0, 1, ai)
    return e
def smooth(x, k):
    w = np.hanning(k); return np.convolve(x, w / w.sum(), mode='same')
def tone(f, dur, harm=((1, 1),), a=0.005, tau=0.4, det=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for h, g in harm:
        s += g * np.sin(2 * np.pi * f * h * t)
        if det: s += g * 0.6 * np.sin(2 * np.pi * f * h * (1 + det) * t + 1.3)
    return s * env(n, a, tau)

BPM = 120; beat = 60 / BPM; bar = 4 * beat
# A minor: Am F C G
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60, 64], [55, 59, 62]]
roots = [45, 41, 48, 43]
nbars = int(np.ceil(DUR / bar))
for b in range(nbars):
    t0 = b * bar; ci = b % 4
    last = t0 >= 18.0
    if last: ci = 0
    # Pad: soft detuned partials, slow attack
    for m in chords[ci] + [chords[ci][0] + 12]:
        n = int((bar + 0.6) * SR); tt = np.arange(n) / SR
        s = (np.sin(2*np.pi*hz(m)*tt) + 0.5*np.sin(2*np.pi*hz(m)*1.003*tt + 1) + 0.18*np.sin(2*np.pi*hz(m)*2*tt))
        e = np.minimum(1, tt / 0.5) * np.minimum(1, (bar + 0.6 - tt) / 0.6)
        g = 0.045 if t0 < 2.8 else 0.035
        place(s * e, t0, g, pan=(m % 5 - 2) * 0.15)
    if t0 >= 17.0: continue
    for k in range(8):  # 8th notes
        t = t0 + k * beat / 2
        if t >= 17.0: break
        # Pluck arpeggio
        notes = chords[ci] + [chords[ci][1] + 12]
        m = notes[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 12
        pl = tone(hz(m), 0.6, ((1, 1), (2, 0.35), (3, 0.12)), a=0.002, tau=0.18)
        place(pl, t, 0.05 if t < 2.8 else 0.04, pan=0.35 if k % 2 else -0.35)
        if t >= 2.8:
            # Bass 8ths (root, octave on offbeat)
            bm = roots[ci] - 12 + (12 if k % 2 else 0)
            bs = tone(hz(bm), 0.3, ((1, 1), (2, 0.25)), a=0.004, tau=0.12)
            place(smooth(bs, 9), t, 0.16)
            # Hats on offbeats
            if k % 2:
                nz = np.diff(rng.standard_normal(int(0.06 * SR) + 1)) * env(int(0.06 * SR), 0.0005, 0.012)
                place(nz, t, 0.03, pan=0.25)
            if k % 2 == 0:
                # Kick
                n = int(0.35 * SR); tt = np.arange(n) / SR
                f = 50 + 90 * np.exp(-tt / 0.03); ph = 2 * np.pi * np.cumsum(f) / SR
                place(np.sin(ph) * env(n, 0.001, 0.12), t, 0.32)
                # Clap on 2 and 4 in the middle section
                if 9.6 <= t < 17.0 and k in (2, 6):
                    nz = smooth(rng.standard_normal(int(0.18 * SR)), 5) - smooth(rng.standard_normal(int(0.18 * SR)), 40)
                    place(nz * env(len(nz), 0.002, 0.05), t, 0.09)

# Riser into the game (2.0 -> 2.8)
n = int(0.8 * SR); tt = np.arange(n) / SR
nz = smooth(rng.standard_normal(n), 6) * (tt / 0.8) ** 2
place(nz, 2.0, 0.05)

def whoosh(t, d=0.35, g=0.05):
    n = int(d * SR); tt = np.arange(n) / SR
    nz = smooth(rng.standard_normal(n), 12) * np.sin(np.pi * tt / d) ** 2
    place(nz, t - d * 0.5, g)
for t in (2.85, 6.85, 9.7, 12.8, 14.2, 15.6, 17.0): whoosh(t)

def click(t, g=0.05, f=2200):
    n = int(0.03 * SR); nz = np.diff(rng.standard_normal(n + 1)) * env(n, 0.0003, 0.004)
    place(nz + tone(f, 0.03, a=0.0005, tau=0.006), t, g, pan=0.1)
for i in range(7): click(4.55 + i * 0.26)
click(3.8, 0.06, 1760); click(6.45, 0.07, 1320)

def bell(t, m, g=0.06, tau=0.9):
    s = tone(hz(m), 2.5, ((1, 1), (2.0, 0.3), (3.01, 0.12), (4.2, 0.05)), a=0.002, tau=tau)
    place(s, t, g, pan=((m % 7) - 3) * 0.08)
# Vowels slide in: A5 C6 D6 E6 (A minor pentatonic)
for i, m in enumerate([81, 84, 86, 88]): bell(7.55 + i * 0.16, m)
bell(8.32, 93, 0.035, 1.4); bell(8.32, 88, 0.03, 1.4)
for i in range(4): bell(13.35 + i * 0.2, 76 + [0, 3, 5, 7][i], 0.03, 0.25)   # combo
n = int(0.4 * SR); tt = np.arange(n) / SR                                      # heart lost
place(np.sin(2 * np.pi * np.cumsum(140 * np.exp(-tt / 0.1) + 60) / SR) * env(n, 0.002, 0.1), 14.95, 0.12)
for i, m in enumerate([76, 81, 84]): bell(16.0 + i * 0.12, m, 0.04, 0.5)
for i, m in enumerate([79, 84]): bell(16.35 + i * 0.12, m, 0.04, 0.5)
# Outro: wordmark lands, vowels drop, final chord
n = int(0.5 * SR); tt = np.arange(n) / SR
place(np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-tt / 0.05)) / SR) * env(n, 0.001, 0.25), 17.05, 0.35)
for i, m in enumerate([81, 84, 88]): bell(17.9 + i * 0.16, m, 0.07)
for m in [57, 64, 69, 71, 72, 76]:
    place(tone(hz(m), 3.4, ((1, 1), (2, 0.2), (3, 0.06)), a=0.01, tau=1.6, det=0.002), 18.4, 0.05)
bell(18.4, 93, 0.04, 1.8)
bell(19.3, 88, 0.035, 0.6)

# Master: gentle fade-in/out, soft clip, normalize to -1 dBFS
t = np.arange(N) / SR
mix *= np.minimum(1, t / 0.05)[:, None] * np.clip((DUR - t) / 1.2, 0, 1)[:, None] ** 1.5
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= 0.89 / np.max(np.abs(mix))
pcm = (mix * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', N / SR)
