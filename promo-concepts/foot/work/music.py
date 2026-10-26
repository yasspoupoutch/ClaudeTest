# Soundtrack for "seuls les vrais fans de foot": stomp-stomp-clap anthem in E minor, whistle, horn on each answer.
# No continuous crowd noise (it sounded like static): the stadium is carried by the beat, a low rumble only on answers.
import sys; import numpy as np; from synth import *; from endcue import end_cues
DUR, END = 24.0, 18.6
ROUNDS = [2.6, 7.1, 11.6]
M = Mix(DUR, seed=11)
def rumble(t0, d, g):   # a crowd going up: low, soft, no hiss
    k = int(d * SR); x = smooth(M.noise(k), 220) * 12
    e = np.minimum(1, np.arange(k) / (0.15 * SR)) * np.exp(-np.arange(k) / (0.9 * SR))
    M.place(x * e, t0, g, -0.25); M.place(smooth(M.noise(k), 220) * 12 * e, t0, g, 0.25)
def whistle(t0, d=0.35, g=0.04):
    k = int(d * SR); s = np.arange(k) / SR; f = 2600 + 80 * np.sin(2 * np.pi * 26 * s)
    M.place(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(k, 0.005, d) * np.minimum(1, (d - s) / 0.03), t0, g)
def horn(t0, g=0.05):
    M.place(tone(hz(57), 0.8, ((1, 1), (2, .45), (3, .25), (4, .1)), a=0.02, tau=0.45, det=0.003), t0, g)
chords = [[64, 67, 71], [60, 64, 67], [62, 66, 69], [59, 62, 66]]   # Em C D Bm
roots = [40, 36, 38, 35]
t = 0.0; step = 0
while t < END:
    thinking = any(r + 0.4 <= t < r + 3.45 for r in ROUNDS)
    g = 0.55 if thinking else 1.0; ci = int(t // 2) % 4; k = step % 4
    if k in (0, 1): M.place(kick(0.3, 45, 70, 0.1), t, 0.3 * g)          # stomp, stomp
    if k == 2: M.place(clap(M), t, 0.1 * g)                                # clap
    if k == 0:
        for m in chords[ci]: M.place(pad(m, 2.1), t, 0.022 * (0.6 if thinking else 1))
        M.place(smooth(tone(hz(roots[ci]), 0.5, ((1, 1), (2, .3)), a=.004, tau=.25), 9), t, 0.14 * g)
    t += 0.25 if k < 2 else 0.5; step += 1
# hook
M.place(kick(0.5, 42, 70, 0.25), 0.05, 0.3); M.place(whoosh(M, 0.5), 0.45, 0.05)
for i, m in enumerate([64, 67, 71, 76]): M.place(pluck(m + 12, 0.25), 0.5 + i * 0.15, 0.04)
for r in ROUNDS:
    whistle(r + 0.05)
    for s in range(3): M.place(tone(1700 if s < 2 else 1300, 0.05, ((1, 1),), a=0.0005, tau=0.012), r + 0.4 + s, 0.08, 0.2)
    for j in range(5): M.place(bell([76, 79, 83, 86, 88][j], 0.6), r + 3.45 + j * 0.09, 0.045)
    horn(r + 3.75); rumble(r + 3.45, 1.6, 0.06)
whistle(ROUNDS[0] + 3.5, 0.5, 0.04)                                         # referee on the yellow card
M.place(whoosh(M, 0.6), 15.9, 0.07); M.place(pluck(76), 16.1, 0.05); M.place(pluck(79), 16.7, 0.05)
end_cues(M, END)
M.write(sys.argv[1], fade_out=1.2)
