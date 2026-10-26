# Soundtrack for "ton cerveau sait lire sans voyelles": E minor, 120 BPM. Times follow composition.html.
import sys; from synth import *; from endcue import end_cues
DUR, T2, T3, END = 24.0, 6.9, 11.9, 18.7
M = Mix(DUR, seed=5)
chords = [[64, 67, 71], [60, 64, 67], [55, 59, 62, 67], [62, 66, 69]]  # Em C G D
roots = [40, 36, 43, 38]
def think(t0):   # 3 s on the clock: tick-tock and a heartbeat
    for s in range(3):
        tk = t0 + 0.4 + s; M.place(tone(2000 if s < 2 else 1500, 0.05, ((1, 1),), a=0.0005, tau=0.012), tk, 0.1, 0.2)
        M.place(kick(0.25, 40, 50, 0.08), tk + 0.05, 0.22); M.place(kick(0.25, 38, 45, 0.08), tk + 0.21, 0.15)
def found(t0, n, top=76):
    scale = [64, 67, 69, 71, 74, 76, 79, 81, 83, 86]
    for j in range(n): M.place(bell(scale[j % len(scale)] + 12, 0.7), t0 + j * 0.07, 0.05, (j % 3 - 1) * 0.3)
    for m in [52, 64, 67, 71]: M.place(tone(hz(m), 1.8, ((1, 1), (2, .2)), a=0.01, tau=0.8, det=0.002), t0 + 0.3, 0.04)
t = 0.0; step = 0
while t < END:
    ci = int(t // 2) % 4; k = step % 8
    if k == 0:
        for m in chords[ci]: M.place(pad(m, 2.3), t, 0.03)
    if t >= T2:
        if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.3, ((1, 1), (2, .25)), a=.004, tau=.14), 9), t, 0.14)
        if k in (0, 4): M.place(kick(), t, 0.24)
        if k in (2, 6) and not (T2 + 0.4 <= t < T2 + 3.4 or T3 + 0.4 <= t < T3 + 3.4): M.place(clap(M), t, 0.07)
        if k % 2: M.place(hat(M), t, 0.025, 0.25)
    else:
        notes = chords[ci] + [chords[ci][0] + 12]
        if k % 2 == 0: M.place(pluck(notes[(k // 2) % 4] + 12, 0.22), t, 0.035, 0.2)
    t += 0.25; step += 1
# level 1: a soft hit, the reading bar ticking, the vowels drop
M.place(kick(0.5, 42, 70, 0.25), 0.05, 0.25)
for i in range(5): M.place(tone(1600, 0.04, ((1, 1),), a=0.0005, tau=0.01), 0.45 + i * 0.5, 0.05)
found(2.75, 10); M.place(pluck(76), 4.1, 0.05); M.place(pluck(79), 4.7, 0.05)
# level 2 and 3
M.place(whoosh(M, 0.5), T2 - 0.25, 0.08); think(T2); found(T2 + 3.5, 7); M.place(blip(88, dur=0.1), T2 + 4.0, 0.05)
M.place(whoosh(M, 0.5), T3 - 0.25, 0.08); think(T3); found(T3 + 3.5, 3); M.place(blip(91, dur=0.1), T3 + 4.0, 0.06)
M.place(riser(M, 0.6), T3 + 2.8, 0.06)
# the app
M.place(whoosh(M, 0.7), 16.3, 0.08)
end_cues(M, END)
M.write(sys.argv[1], fade_out=1.2)
