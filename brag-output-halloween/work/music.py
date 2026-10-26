# Soundtrack for the CNSNN Halloween video: D minor, 120 BPM, music box, heartbeat and thunder. Timed on composition.html.
import sys; import numpy as np; from synth import *
DUR = 25.5
M = Mix(DUR, seed=31)
beat = 0.5
def thunder(t, g=0.5, d=2.6):
    n = int(d * SR); x = smooth(M.noise(n), 160) * 9; x *= env(n, 0.01, 0.7)
    M.place(x, t, g, -0.2); M.place(kick(0.9, 30, 70, 0.4), t, g * 0.8)
def hit(t, g=0.4): M.place(kick(0.7, 38, 110, 0.32), t, g); M.place(whoosh(M, 0.5), t - 0.25, 0.08)
def flutter(t, d=0.8, g=0.04):
    n = int(d * SR); tt = np.arange(n) / SR; x = smooth(M.noise(n), 8) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 13 * tt))) * np.sin(np.pi * tt / d)
    M.place(x, t, g, 0.4)
def heart(t, g=0.32): M.place(kick(0.25, 40, 50, 0.08), t, g); M.place(kick(0.25, 38, 45, 0.08), t + 0.16, g * 0.7)
def box(m, t, g=0.05, pan=0.0): M.place(tone(hz(m), 1.6, ((1, 1), (3.0, 0.25), (5.4, 0.08)), a=0.002, tau=0.5), t, g, pan)
# drone + wind throughout
n = M.n; tt = np.arange(n) / SR
drone = (np.sin(2 * np.pi * hz(26) * tt) + 0.6 * np.sin(2 * np.pi * hz(33) * tt + 1) + 0.25 * np.sin(2 * np.pi * hz(38) * 1.003 * tt)) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / 7))
M.place(drone * np.minimum(1, tt / 1.5), 0, 0.05)
M.place(smooth(M.noise(n), 40) * 3 * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 5.3)), 0, 0.03, -0.3)
# 0–2.6 title: neon whooshes, music box theme, thunder on the logo
M.place(whoosh(M, 0.8), 0.0, 0.1); M.place(whoosh(M, 0.9), 0.6, 0.08)
theme = [62, 65, 69, 68, 65, 62, 61, 62]          # D F A G# F D C# D — the tritone does the creeping
for i, m in enumerate(theme): box(m + 12, 0.15 + i * 0.3, 0.05, (i % 2 - 0.5) * 0.4)
thunder(0.95, 0.45); flutter(0.3); flutter(1.1, 0.9)
# 2.6–5.2 kinetic words: an impact per word, riser into the game
for t0 in (2.7, 3.35): hit(t0, 0.3)
hit(4.0, 0.5); M.place(tone(hz(50), 1.4, ((1, 1), (2, .4), (3, .2)), a=0.005, tau=0.6, det=0.004), 4.0, 0.08)
M.place(riser(M, 1.0), 4.2, 0.07)
# rounds: heartbeat + clock ticks while thinking, then bells for the vowels and a chord
ROUNDS = [(5.2, 4), (8.6, 4), (12.0, 4)]
for k, (r, nv) in enumerate(ROUNDS):
    hit(r, 0.3); M.place(pad(50, 3.2), r, 0.03); M.place(pad(57, 3.2), r, 0.025)
    for s in range(3):
        tk = r + 0.5 + s * 1.9 / 3; M.place(tone(2200, 0.05, ((1, 1),), a=0.0005, tau=0.012), tk, 0.12, 0.2); heart(tk + 0.05, 0.25 + 0.05 * s)
    rv = r + 2.4
    for j in range(nv): M.place(bell([74, 77, 81, 86, 89][j % 5], 0.8), rv + j * 0.09 + 0.05, 0.07, (j - nv / 2) * 0.15)
    for m in [50, 62, 65, 69]: M.place(tone(hz(m), 1.6, ((1, 1), (2, .2)), a=0.01, tau=0.7, det=0.002), rv + 0.35, 0.04)
    M.place(whoosh(M, 0.45), r + 3.2, 0.06)
flutter(5.6, 1.0, 0.03)                                   # spider drop
M.place(smooth(M.noise(int(2.4 * SR)), 30) * 2 * np.sin(np.linspace(0, np.pi, int(2.4 * SR))), 8.6, 0.05)   # fog
for i in range(6): flutter(14.45 + i * 0.07, 0.9, 0.035)  # bat swarm
# 15.4–18.6 phone: a beat comes in
t = 15.4; step = 0; roots = [38, 34, 36, 33]
while t < 18.6:
    k = step % 8; ci = int((t - 15.4) // 2) % 4
    if k in (0, 4): M.place(kick(), t, 0.26)
    if k in (2, 6): M.place(clap(M), t, 0.07)
    if k % 2: M.place(hat(M), t, 0.025, 0.25)
    if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.3, ((1, 1), (2, .25)), a=.004, tau=.14), 9), t, 0.15)
    if k == 0:
        for m in ([62, 65, 69], [58, 62, 65], [60, 64, 67], [57, 61, 64])[ci]: M.place(pad(m, 2.3), t, 0.025)
    t += beat / 2; step += 1
M.place(whoosh(M, 0.8), 15.2, 0.09)
# 18.6–21: lock screen, the reminder chimes
M.place(whoosh(M, 0.6), 18.4, 0.07)
M.place(blip(86, dur=0.09), 19.3, 0.06); M.place(blip(91, dur=0.12), 19.45, 0.055)
for i, m in enumerate([62, 65, 69, 74]): box(m + 12, 19.9 + i * 0.22, 0.035)
# 21–25.5 end: thunder, vowels drop, the store
thunder(21.0, 0.5); M.place(riser(M, 0.6), 20.4, 0.06)
for i, m in enumerate([74, 77, 81]): M.place(bell(m, 1.0), 21.7 + i * 0.15 + 0.1, 0.07)
for m in [38, 50, 57, 62, 65, 69, 74]: M.place(tone(hz(m), 3.5, ((1, 1), (2, .2), (3, .06)), a=0.01, tau=1.6, det=0.002), 22.1, 0.04)
for i, t0 in enumerate([22.5, 22.85, 23.2]): M.place(pluck(74 + [0, 3, 7][i]), t0, 0.06)
M.place(blip(86, dur=0.08), 23.6, 0.05); M.place(blip(93, dur=0.08), 23.85, 0.045)
for i, m in enumerate(theme[:5]): box(m + 12, 24.0 + i * 0.25, 0.035)
M.write(sys.argv[1], fade_out=1.4)
