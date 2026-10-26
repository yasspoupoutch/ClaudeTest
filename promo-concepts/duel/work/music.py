# Soundtrack for "le duel": A minor, 128 BPM, tense; keystrokes of both players, a buzzer on the miss, fanfare on the win.
import sys; from synth import *; from endcue import end_cues
DUR, GO, END = 23.5, 2.3, 17.8
M = Mix(DUR, seed=21)
beat = 60 / 128
TRIES = {'pa': [(7.9, 'CASSOULET', 0.22, 10.3)], 'pb': [(2.6, 'CASSOLET', 0.22, 4.7), (11.3, 'CASSOULET', 0.2, 13.3)]}
chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 56, 59]]   # Am F G E: a chase
roots = [45, 41, 43, 40]
t = GO; step = 0
while t < 14.3:
    ci = int((t - GO) // (beat * 4)) % 4; k = step % 8
    if k in (0, 4): M.place(kick(), t, 0.25)
    if k in (2, 6): M.place(clap(M), t, 0.07)
    M.place(hat(M), t, 0.02 if k % 2 == 0 else 0.03, 0.25)
    if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.25, ((1, 1), (2, .25)), a=.004, tau=.12), 9), t, 0.15)
    if k == 0:
        for m in chords[ci]: M.place(pad(m, beat * 4 + 0.2), t, 0.025)
    t += beat / 2; step += 1
# hook: two hits and a riser
M.place(kick(0.5, 42, 80, 0.3), 0.05, 0.3); M.place(kick(0.5, 42, 80, 0.3), 0.55, 0.3); M.place(riser(M, 1.2), 1.0, 0.07)
M.place(whoosh(M, 0.6), 1.85, 0.08); M.place(bell(81, 0.5), 2.1, 0.05)
# keystrokes, left and right
for side, pan in (('pa', -0.5), ('pb', 0.5)):
    for t0, w, dt, tv in TRIES[side]:
        for i in range(len(w)): M.place(tone(1500 + (i % 3) * 150, 0.03, ((1, 1),), a=0.0005, tau=0.008), t0 + i * dt, 0.05, pan)
        M.place(tone(900, 0.05, ((1, 1),), a=0.0005, tau=0.015), tv, 0.07, pan)
# Malik's miss: a buzzer; Léa's win: bells and a fanfare; Malik second
n = int(0.4 * SR); M.place(tone(110, 0.4, ((1, 1), (2, .6), (3, .5), (4, .3)), a=0.005, tau=0.3) , 4.72, 0.08, 0.5)
for j in range(4): M.place(bell([76, 79, 83, 88][j], 0.7), 10.3 + j * 0.09, 0.06, -0.4)
for i, m in enumerate([69, 72, 76, 81]): M.place(tone(hz(m), 0.6, ((1, 1), (2, .4), (3, .2)), a=0.01, tau=0.35), 10.45 + i * 0.12, 0.05, -0.3)
for m in [57, 64, 69, 72, 76]: M.place(tone(hz(m), 1.8, ((1, 1), (2, .3)), a=0.01, tau=0.9, det=0.002), 10.95, 0.035)
for j in range(4): M.place(bell([72, 76, 79, 84][j], 0.6), 13.3 + j * 0.09, 0.045, 0.4)
# leaderboard and the challenge button
M.place(whoosh(M, 0.6), 14.2, 0.08); M.place(blip(84, dur=0.08), 14.5, 0.05)
for i in range(3): M.place(blip(88 + i * 3, dur=0.07), 15.6 + i * 0.6, 0.04)
end_cues(M, END)
M.write(sys.argv[1], fade_out=1.2)
