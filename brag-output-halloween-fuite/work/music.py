# Soundtrack for "la nuit où les voyelles ont disparu": D minor, 120 BPM. Pass times come from times.json
# (when the camera crosses each floating line, ring and carved pumpkin), written by window.passTimes().
import sys, json; import numpy as np; from synth import *
DUR = 26.0
M = Mix(DUR, seed=1031)
T = json.load(open('times.json'))
def thunder(t, g=0.5, d=2.6):
    n = int(d * SR); x = smooth(M.noise(n), 160) * 9; x *= env(n, 0.01, 0.7)
    M.place(x, t, g, -0.2); M.place(kick(0.9, 30, 70, 0.4), t, g * 0.8)
def flutter(t, d=0.8, g=0.04, pan=0.4):
    n = int(d * SR); tt = np.arange(n) / SR; x = smooth(M.noise(n), 8) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 13 * tt))) * np.sin(np.pi * tt / d)
    M.place(x, t, g, pan)
def box(m, t, g=0.05, pan=0.0): M.place(tone(hz(m), 1.6, ((1, 1), (3.0, 0.25), (5.4, 0.08)), a=0.002, tau=0.5), t, g, pan)
def toll(m, t, g=0.06): M.place(tone(hz(m), 4.0, ((1, 1), (2.4, .5), (3.0, .3), (4.2, .2), (5.4, .1)), a=0.003, tau=1.4, det=0.003), t, g)
def buzz(t, d, g=0.03):
    n = int(d * SR); tt = np.arange(n) / SR; x = np.sign(np.sin(2 * np.pi * 100 * tt)) * (np.sin(2 * np.pi * 21 * tt) > 0.2) * env(n, 0.005, d)
    M.place(smooth(x, 6), t, g)
n = M.n; tt = np.arange(n) / SR
# bed: drone and wind, all along
drone = (np.sin(2 * np.pi * hz(26) * tt) + 0.6 * np.sin(2 * np.pi * hz(33) * tt + 1) + 0.25 * np.sin(2 * np.pi * hz(38) * 1.003 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / 7))
M.place(drone * np.minimum(1, tt / 1.5), 0, 0.05)
M.place(smooth(M.noise(n), 40) * 3 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 5.3)), 0, 0.03, -0.3)
# 0–1.4: the six vowels wait in a row, music-box theme with its tritone
theme = [62, 65, 69, 68, 65, 62, 61, 62]
for i, m_ in enumerate(theme[:4]): box(m_ + 12, 0.1 + i * 0.28, 0.05, (i % 2 - 0.5) * 0.4)
for i in range(6): M.place(bell([74, 77, 81, 84, 86, 89][i], 0.5), 0.12 + i * 0.08, 0.025, (i - 2.5) * 0.15)
# 1.4–2.0: they tremble (a fast chatter), then each hops and dashes off with a giggle and a whoosh
for i in range(14): M.place(blip(96 + (i % 3) * 2, dur=0.03), 1.42 + i * 0.042, 0.02, ((i % 3) - 1) * 0.5)
for i in range(6):
    t0 = 2.0 + i * 0.12
    M.place(blip(86 + i * 2, dur=0.07), t0, 0.05, (i - 2.5) * 0.18)
    M.place(whoosh(M, 0.4), t0, 0.05, (i - 2.5) * 0.18)
# 2.8: the chase starts
M.place(riser(M, 0.9), 2.2, 0.08); M.place(whoosh(M, 0.8), 2.9, 0.1)
# 3.1–16.3: the chase, 120 BPM
t = 3.1; step = 0; roots = [38, 34, 36, 33]; chords = ([62, 65, 69], [58, 62, 65], [60, 64, 67], [57, 61, 64])
while t < 16.2:
    k = step % 8; ci = int((t - 3.1) // 2) % 4
    if k in (0, 4): M.place(kick(), t, 0.26)
    if k in (2, 6): M.place(clap(M), t, 0.07)
    M.place(hat(M), t, 0.02 if k % 2 == 0 else 0.03, 0.25)
    if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.28, ((1, 1), (2, .25)), a=.004, tau=.14), 9), t, 0.15)
    if k == 0:
        for m in chords[ci]: M.place(pad(m, 2.3), t, 0.022)
        box(theme[(step // 8) % 8] + 12, t, 0.035)
    t += 0.25; step += 1
for w in T['words']: M.place(whoosh(M, 0.5), w - 0.25, 0.07, 0.3 if w % 2 > 1 else -0.3)
for r in T['rings']: M.place(whoosh(M, 0.7), r - 0.35, 0.1); M.place(kick(0.6, 40, 100, 0.25), r, 0.25); M.place(bell(81, 0.6), r, 0.04)
for c in T['carved']: M.place(whoosh(M, 0.4), c - 0.2, 0.05); box(74, c, 0.03)
for i in range(6): flutter(6.2 + i * 0.12, 0.9, 0.03, (i % 2 - 0.5)); flutter(10.8 + i * 0.12, 0.9, 0.03, (0.5 - i % 2))
# 15.6–18.6: the vowels reach the phone, one bell each, then the found word
M.place(pad(50, 4.0), 16.2, 0.035); M.place(pad(57, 4.0), 16.2, 0.03)
for i in range(6): M.place(bell([74, 77, 81, 86, 89, 93][i], 0.8), 17.5 + i * 0.22, 0.07, (i - 2.5) * 0.15)
for m in [50, 62, 65, 69, 74]: M.place(tone(hz(m), 2.0, ((1, 1), (2, .2)), a=0.01, tau=0.9, det=0.002), 18.35, 0.04)
# 19–20.25: dive into the screen, impact
M.place(riser(M, 1.2), 19.05, 0.1); thunder(20.25, 0.5)
# end card
for i, m in enumerate([74, 77, 81]): M.place(bell(m, 1.0), 21.0 + i * 0.18 + 0.1, 0.07)
for m in [38, 50, 57, 62, 65, 69, 74]: M.place(tone(hz(m), 3.5, ((1, 1), (2, .2), (3, .06)), a=0.01, tau=1.6, det=0.002), 21.5, 0.04)
M.place(pluck(74), 22.0, 0.06); M.place(pluck(77), 22.35, 0.06)
M.place(blip(86, dur=0.08), 23.0, 0.05); M.place(blip(93, dur=0.08), 23.3, 0.045)
for i, m in enumerate(theme[:5]): box(m + 12, 23.8 + i * 0.25, 0.035)
M.write(sys.argv[1], fade_out=1.5)
