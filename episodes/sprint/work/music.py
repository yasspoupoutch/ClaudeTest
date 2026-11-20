# Fast bed for the Sprint edit: 128 BPM, a tick that speeds up with the game, hits on the combo, the last seconds and the result.
import sys, json; from synth import *
T = json.load(open(sys.argv[2])); M = Mix(T['end'])
chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]   # Am F G Em
b = 60 / 128; t, step = 0.0, 0
while t < T['end'] - 1.0:
    bar = int(t // (4 * b)) % 4; k = step % 8
    if k == 0:
        for m in chords[bar]: M.place(pad(m, 4 * b + 0.2), t, 0.025)
    if T['TH'] <= t < T['TE']:
        if k % 2 == 0: M.place(kick(), t, 0.2)
        if k % 2: M.place(hat(M), t, 0.02, 0.25)
        if k in (2, 6): M.place(clap(M), t, 0.05)
        M.place(pluck(chords[bar][k % 3] + 12), t, 0.02, 0.3 if k % 2 else -0.3)
    t += b / 2; step += 1
M.place(riser(M, 1.2), T['TH'] - 1.2, 0.05); M.place(kick(0.5, 45, 90, 0.2), T['TH'], 0.3)
for k in ('combo', 'last'):
    for j, m in enumerate([76, 79, 83, 88]): M.place(bell(m, 0.6), T[k] + j * 0.07, 0.05)
M.place(kick(0.6, 42, 80, 0.3), T['TR'], 0.35)
for j, m in enumerate([72, 76, 79, 84]): M.place(bell(m), T['TE'] + 0.1 + j * 0.12, 0.06)
M.write(sys.argv[1]); print('ok')
