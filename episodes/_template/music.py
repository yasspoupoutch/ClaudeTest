# Soundtrack for the "3 secondes" quiz: E minor, 120 BPM, a ticking clock under each round.
import sys, json; from synth import *
EP = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'ep.json'))
N = len(EP['rounds']); OT = 2.4 + 4.6 * N
M = Mix(OT + 4.5)
beat = 0.5; bar = 2.0
chords = [[64, 67, 71], [60, 64, 67], [55, 59, 62, 67], [62, 66, 69]]  # Em C G D
roots = [40, 36, 43, 38]
ROUNDS = [(2.4 + 4.6 * i, [76, 79, 83, 88][:3 + (i == N - 1 and N > 1)]) for i in range(N)]
def thinking(t): return any(r + 0.45 <= t < r + 3.45 for r, _ in ROUNDS)
t = 0.0; step = 0
while t < OT:
    ci = int(t // bar) % 4; k = step % 8
    if k == 0:
        for m in chords[ci]: M.place(pad(m, bar + 0.3), t, 0.03)
    if t >= 2.4 and t < OT:
        if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.3, ((1, 1), (2, .25)), a=.004, tau=.14), 9), t, 0.14)
        if k in (0, 4): M.place(kick(), t, 0.24)
        if not thinking(t) and k in (2, 6): M.place(clap(M), t, 0.07)
        if k % 2: M.place(hat(M), t, 0.025, 0.25)
    if t < 2.4 or t >= OT:
        notes = chords[ci] + [chords[ci][0] + 12]
        M.place(pluck(notes[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 12), t, 0.04, 0.3 if k % 2 else -0.3)
    t += beat / 2; step += 1
# Hook accents
M.place(kick(0.5, 45, 90, 0.2), 0.0, 0.3); M.place(bell(83, 0.5), 0.45, 0.04); M.place(bell(88, 0.5), 1.2, 0.035)
M.place(riser(M, 0.7), 1.7, 0.05)
for r0, vowels in ROUNDS:
    M.place(whoosh(M, 0.3), r0 - 0.05, 0.05)
    for s in range(3):  # clock ticks, tock on the last
        n = int(0.05 * SR)
        M.place(tone(2000 if s < 2 else 1500, 0.05, a=.0005, tau=.012) + 0.4 * hat(M, 0.05, 0.006)[:n], r0 + 0.45 + s, 0.08)
    rv = r0 + 3.45
    for i, m in enumerate(vowels): M.place(bell(m, 0.7), rv + i * 0.12, 0.055, (i - 2) * 0.15)
    for m in [52, 64, 71, 76]: M.place(tone(hz(m), 1.2, ((1, 1), (2, .2)), a=.02, tau=.5), rv + 0.1, 0.035)
# Outro
M.place(kick(0.6, 42, 80, 0.3), OT + 0.00, 0.38)
for i, m in enumerate([76, 79, 83]): M.place(bell(m), OT + 0.70 + i * 0.16, 0.07)
for m in [52, 64, 71, 76, 78, 79]: M.place(tone(hz(m), 2.6, ((1, 1), (2, .2), (3, .06)), a=.01, tau=1.4, det=.002), OT + 1.20, 0.045)
M.place(bell(88, 0.6), OT + 2.00, 0.035)
# App Store badge
M.place(blip(88, dur=0.08), OT + 2.50, 0.05); M.place(blip(93, dur=0.08), OT + 2.66, 0.045)
for m in [52, 64, 71, 76, 79]: M.place(tone(hz(m), 2.4, ((1, 1), (2, .2)), a=.05, tau=1.6, det=.002), OT + 2.50, 0.03)
M.write(sys.argv[1])
print('ok')
