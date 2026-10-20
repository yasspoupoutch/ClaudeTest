# Soundtrack for "défi v2": lo-fi night groove, chat sounds, tape rewind, typewriter end card.
import sys; from synth import *
DUR = 28.5
M = Mix(DUR)
bpm = 88; beat = 60 / bpm; bar = 4 * beat
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]   # Fmaj7 Em7 Dm7 Cmaj7
roots = [41, 40, 38, 36]
def epiano(m, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*hz(m)*tt) + 0.3*np.sin(2*np.pi*hz(m)*2*tt)*np.exp(-tt/0.3) + 0.08*np.sin(2*np.pi*hz(m)*3*tt)*np.exp(-tt/0.1)
    return s * env(n, 0.004, 1.2) * (1 + 0.15 * np.sin(2*np.pi*4.5*tt))
def music(t0, t1, busy):
    t = t0; step = 0
    while t < t1:
        ci = int((t - t0) // bar) % 4; k = step % 8
        if k == 0:
            for m in chords[ci]: M.place(epiano(m, min(bar, t1 - t) + 0.05), t, 0.03, (m % 4 - 1.5) * 0.2)
        if k in (0, 5): M.place(smooth(kick(0.3, 48, 60, 0.11), 15), t + (0.02 if k == 5 else 0), 0.3)
        if k in (2, 6): M.place(smooth(clap(M), 9), t, 0.1)
        if k % 2 or busy: M.place(smooth(hat(M, 0.05, 0.01), 3), t + (0.03 if k % 2 else 0), 0.035 if k % 2 else 0.018, 0.3)
        if k in (0, 3, 4): M.place(smooth(tone(hz(roots[ci]), 0.4, ((1, 1), (2, .2)), a=.01, tau=.25), 15), t, 0.14)
        t += beat / 2; step += 1
# Room tone + vinyl crackle under everything except the end card
n = int(23.3 * SR)
crack = np.zeros(n); idx = M.rng.integers(0, n, 400); crack[idx] = M.rng.uniform(-1, 1, 400)
M.place(smooth(crack, 3) + 0.02 * smooth(M.noise(n), 200), 0, 0.25)
# Notification + unlock
M.place(bell(84, 0.25, 0.6), 0.15, 0.06); M.place(bell(88, 0.3, 0.8), 0.27, 0.06)
M.place(blip(96, dur=0.03), 1.3, 0.05)
music(1.4, 13.5, False)
# Chat sounds
for t in (2.5, 3.3, 4.2, 11.2, 12.0, 20.3, 21.0): M.place(blip(79, up=True, dur=0.09), t, 0.08, -0.15); M.place(blip(84, up=True, dur=0.07), t + 0.05, 0.05, -0.15)
for t in (9.72, 18.5, 19.1, 21.7): M.place(whoosh(M, 0.22), t - 0.05, 0.05, 0.2); M.place(blip(88, up=True, dur=0.08), t, 0.06, 0.2)
for t in (10.5, 12.6, 19.7): M.place(blip(91, dur=0.06), t, 0.05); M.place(blip(95, dur=0.06), t + 0.06, 0.04)
for i in range(8):  # phone keyboard clicks
    t = 7.25 + i * 0.27; m = int(0.025 * SR); M.place(smooth(M.noise(m), 4) * env(m, .0003, .005), t, 0.18, 0.1)
# Tape rewind: falling-then-rising chirps with noise
n = int(0.8 * SR); tt = np.arange(n) / SR
f = 300 + 1800 * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt)) * (tt / 0.8)
M.place((np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + 0.5 * smooth(M.noise(n), 6)) * np.minimum(1, tt / 0.05) * np.minimum(1, (0.8 - tt) / 0.1), 13.5, 0.08)
M.place(tone(hz(29), 1.0, ((1, 1), (2, .3)), a=0.05, tau=0.6), 14.3, 0.18)     # "Et si…" low swell
for m in [53, 60, 64, 69]: M.place(pad(m, 0.9), 14.35, 0.03)
# CNSNN app + timeline B
music(15.2, 23.3, True)
for i in range(6): M.place(blip(96, dur=0.025), 15.45 + i * 0.13, 0.04)
for j, m in enumerate([81, 84]): M.place(bell(m, 0.5), 16.35 + j * 0.08, 0.06)
for i in range(7): M.place(blip(96, dur=0.025), 16.95 + i * 0.13, 0.04)
# End card: typewriter, CONSONNE, final chord
line = 'Zéro voyelle, zéro pitié.'
for i in range(len(line)): M.place(smooth(M.noise(int(.02 * SR)), 3) * env(int(.02 * SR), .0003, .004), 23.45 + i / len(line), 0.12)
for i in range(10): M.place(smooth(M.noise(int(.02 * SR)), 3) * env(int(.02 * SR), .0003, .004), 25.3 + i * 0.03, 0.08)
M.place(kick(0.6, 42, 80, 0.3), 25.75, 0.35)
for i, m in enumerate([81, 84, 88]): M.place(bell(m), 26.3 + i * 0.16, 0.07)
for m in [53, 60, 64, 69, 72, 76]: M.place(tone(hz(m), 2.0, ((1, 1), (2, .2), (3, .06)), a=.01, tau=1.2, det=.002), 26.8, 0.045)
M.write(sys.argv[1], fade_out=0.8)
print('ok')
