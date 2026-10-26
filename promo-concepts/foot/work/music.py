# Soundtrack for "seuls les vrais fans de foot": stadium crowd, whistle, stomp-clap beat, a roar on each answer.
import sys; import numpy as np; from synth import *; from endcue import end_cues
DUR, END = 24.0, 18.6
ROUNDS = [2.6, 7.1, 11.6]
M = Mix(DUR, seed=11)
n = M.n; tt = np.arange(n) / SR
def crowd(t0, d, g):   # band-passed noise swelling like a stand
    k = int(d * SR); x = smooth(M.noise(k), 6) - smooth(M.noise(k), 60); e = np.sin(np.pi * np.arange(k) / k) ** 0.6
    M.place(x * e * 2.5, t0, g, -0.2); M.place((smooth(M.noise(k), 6) - smooth(M.noise(k), 60)) * e * 2.5, t0, g, 0.2)
def whistle(t0, d=0.35, g=0.05):
    k = int(d * SR); s = np.arange(k) / SR; f = 2900 + 120 * np.sign(np.sin(2 * np.pi * 28 * s))
    M.place(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(k, 0.005, d), t0, g)
crowd(0, DUR, 0.025)                      # the stadium murmur all along
# stomp-stomp-clap (We Will Rock You feel) under the hook and between rounds, lighter while thinking
t = 0.0; step = 0
while t < END:
    k = step % 4; thinking = any(r + 0.4 <= t < r + 3.45 for r in ROUNDS)
    g = 0.5 if thinking else 1.0
    if k in (0, 1): M.place(kick(0.3, 45, 70, 0.1), t, 0.28 * g)
    if k == 2: M.place(clap(M), t, 0.12 * g)
    if k % 2 == 0 and not thinking: M.place(pad([52, 55, 59, 50][int(t // 2) % 4], 0.6), t, 0.02)
    t += 0.25 if k < 2 else 0.5; step += 1
M.place(kick(0.5, 42, 70, 0.25), 0.05, 0.3); M.place(whoosh(M, 0.5), 0.45, 0.06)
for r in ROUNDS:
    whistle(r + 0.05)
    for s in range(3): M.place(tone(2000 if s < 2 else 1500, 0.05, ((1, 1),), a=0.0005, tau=0.012), r + 0.4 + s, 0.1, 0.2)
    crowd(r + 3.4, 2.0, 0.09)                                                     # the roar on the answer
    for j in range(5): M.place(bell([76, 79, 83, 86, 88][j], 0.6), r + 3.45 + j * 0.09, 0.045)
    M.place(tone(hz(57), 0.9, ((1, 1), (2, .5), (3, .3)), a=0.02, tau=0.5), r + 3.75, 0.05)          # air horn
whistle(ROUNDS[0] + 3.5, 0.6, 0.05)                                            # referee on the yellow card
M.place(whoosh(M, 0.6), 15.9, 0.08); M.place(pluck(76), 16.1, 0.05); M.place(pluck(79), 16.7, 0.05)
end_cues(M, END)
M.write(sys.argv[1], fade_out=1.2)
