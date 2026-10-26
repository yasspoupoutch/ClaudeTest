# Soundtrack for "la nuit où les voyelles ont disparu": D minor, 120 BPM. Pass times come from times.json
# (when the camera crosses each floating line, ring and carved pumpkin), written by window.passTimes().
# The voice-over (voix.txt) sits on 1.7–6.5 s: the bed stays light there.
import sys, json; import numpy as np; from synth import *
DUR = 27.6
M = Mix(DUR, seed=1031)
T = json.load(open('times.json'))
theme = [62, 65, 69, 68, 65, 62, 61, 62]
def thunder(t, g=0.5, d=2.6):
    n = int(d * SR); x = smooth(M.noise(n), 160) * 9; x *= env(n, 0.01, 0.7)
    M.place(x, t, g, -0.2); M.place(kick(0.9, 30, 70, 0.4), t, g * 0.8)
def flutter(t, d=0.8, g=0.04, pan=0.4):
    n = int(d * SR); tt = np.arange(n) / SR; x = smooth(M.noise(n), 8) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 13 * tt))) * np.sin(np.pi * tt / d)
    M.place(x, t, g, pan)
def box(m, t, g=0.05, pan=0.0): M.place(tone(hz(m), 1.6, ((1, 1), (3.0, 0.25), (5.4, 0.08)), a=0.002, tau=0.5), t, g, pan)
def buzz(t, d, g=0.03):
    n = int(d * SR); tt = np.arange(n) / SR; x = np.sign(np.sin(2 * np.pi * 100 * tt)) * (np.sin(2 * np.pi * 21 * tt) > 0.2) * env(n, 0.005, d)
    M.place(smooth(x, 6), t, g)
def pop(t, m=84, g=0.07, pan=0.0): M.place(kick(0.12, 180, 400, 0.03), t, g * 0.6, pan); M.place(blip(m, dur=0.09), t, g, pan)
def boing(t, m=72, g=0.05, pan=0.0):
    n = int(0.35 * SR); tt = np.arange(n) / SR; f = hz(m) * (1 + 0.5 * np.exp(-tt * 9) * np.sin(2 * np.pi * 9 * tt))
    M.place(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, 0.12), t, g, pan)
n = M.n; tt = np.arange(n) / SR
drone = (np.sin(2 * np.pi * hz(26) * tt) + 0.6 * np.sin(2 * np.pi * hz(33) * tt + 1) + 0.25 * np.sin(2 * np.pi * hz(38) * 1.003 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / 7))
M.place(drone * np.minimum(1, tt / 0.3), 0, 0.05)
M.place(smooth(M.noise(n), 40) * 3 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 5.3)), 0, 0.03, -0.3)
# 0–1.2: the CONSONNE sign buzzes on; A, I, U, Y swoop in
buzz(0.0, 0.3, 0.05); buzz(0.3, 2.6, 0.012)
for k, (t0, pan) in enumerate([(0.45, -0.7), (0.65, 0.0), (0.85, 0.7), (1.05, 0.6)]):
    M.place(whoosh(M, 0.45), t0 - 0.2, 0.06, pan); M.place(bell([74, 81, 86, 89][k], 0.5), t0 + 0.3, 0.04, pan)
for i, m in enumerate(theme[:4]): box(m + 12, 0.1 + i * 0.3, 0.04, (i % 2 - 0.5) * 0.4)
# 1.8–2.9: O, O and E pop out of the sign, which crackles; the two O merge
pop(1.8, 84, pan=-0.3); pop(1.95, 86, pan=0.1); pop(2.1, 89, pan=0.5)
buzz(1.9, 1.0, 0.04); M.place(bell(93, 0.5), 2.68, 0.05)
# 3.0–3.6: they tremble, then each hops and dashes off with a giggle and a whoosh
for i in range(14): M.place(blip(96 + (i % 3) * 2, dur=0.03), 3.02 + i * 0.042, 0.02, ((i % 3) - 1) * 0.5)
for i in range(6):
    t0 = 3.6 + i * 0.12; M.place(blip(86 + i * 2, dur=0.07), t0, 0.05, (i - 2.5) * 0.18); M.place(whoosh(M, 0.4), t0, 0.05, (i - 2.5) * 0.18)
M.place(riser(M, 0.9), 3.9, 0.07)
# 4.6–17.8: the chase, 120 BPM (kept a little lower while the voice speaks, until 6.5)
t = 4.6; step = 0; roots = [38, 34, 36, 33]; chords = ([62, 65, 69], [58, 62, 65], [60, 64, 67], [57, 61, 64])
while t < 17.8:
    k = step % 8; ci = int((t - 4.6) // 2) % 4; g = 0.7 if t < 6.5 else 1.0
    if k in (0, 4): M.place(kick(), t, 0.26 * g)
    if k in (2, 6): M.place(clap(M), t, 0.07 * g)
    M.place(hat(M), t, (0.02 if k % 2 == 0 else 0.03) * g, 0.25)
    if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.28, ((1, 1), (2, .25)), a=.004, tau=.14), 9), t, 0.15 * g)
    if k == 0:
        for m in chords[ci]: M.place(pad(m, 2.3), t, 0.022)
        if t >= 6.5: box(theme[(step // 8) % 8] + 12, t, 0.035)
    t += 0.25; step += 1
for w in T['words']: M.place(whoosh(M, 0.5), w - 0.25, 0.07, 0.3 if w % 2 > 1 else -0.3)
for r in T['rings']: M.place(whoosh(M, 0.7), r - 0.35, 0.1); M.place(kick(0.6, 40, 100, 0.25), r, 0.25); M.place(bell(81, 0.6), r, 0.04)
for c in T['carved']: M.place(whoosh(M, 0.4), c - 0.2, 0.05); box(74, c, 0.03)
for i in range(6): flutter(7.0 + i * 0.12, 0.9, 0.03, (i % 2 - 0.5)); flutter(12.0 + i * 0.12, 0.9, 0.03, (0.5 - i % 2))
# 17–20: at the phone. A, O, E land in their slots (E splits for the second E); I, U, Y bounce off; HALLOWEEN
M.place(pad(50, 4.5), 17.6, 0.035); M.place(pad(57, 4.5), 17.6, 0.03)
for t0, m in [(18.6, 74), (18.9, 77), (19.2, 81), (19.45, 86)]: M.place(bell(m, 0.8), t0, 0.075); pop(t0, 96, 0.03)
for t0, pan in [(18.4, -0.5), (18.5, 0.5), (18.6, -0.4)]: boing(t0, 70, 0.04, pan)
for m in [50, 62, 65, 69, 74, 77]: M.place(tone(hz(m), 2.2, ((1, 1), (2, .2)), a=0.01, tau=1.0, det=0.002), 19.75, 0.04)
# 20.6–21.85: dive into the screen, impact
M.place(riser(M, 1.2), 20.65, 0.1); thunder(21.85, 0.5)
# end card
for i, m in enumerate([74, 77, 81]): M.place(bell(m, 1.0), 22.6 + i * 0.18 + 0.1, 0.07)
for m in [38, 50, 57, 62, 65, 69, 74]: M.place(tone(hz(m), 3.5, ((1, 1), (2, .2), (3, .06)), a=0.01, tau=1.6, det=0.002), 23.1, 0.04)
M.place(pluck(74), 23.6, 0.06); M.place(pluck(77), 23.95, 0.06)
M.place(blip(86, dur=0.08), 24.6, 0.05); M.place(blip(93, dur=0.08), 24.9, 0.045)
for i, m in enumerate(theme[:5]): box(m + 12, 25.3 + i * 0.25, 0.035)
M.write(sys.argv[1], fade_out=1.5)
