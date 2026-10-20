# Full soundtrack of the 3D video, timed on the edit (see assemble.sh):
# quiet bedroom until the rewind, lo-fi groove from the app on, typewriter on the end card.
import sys; from synth import *
EDIT = dict(open=0.0, chat=1.3, type=6.1, mock=10.0, rewind=13.2, etsi=14.0, app=14.9, revenge=20.4, end=26.4)
SCREEN0 = dict(open=0.4, chat=1.7, type=6.4, mock=10.3, app=15.0, revenge=20.5)   # screen time at each shot's first frame
def at(shot, screen_t): return EDIT[shot] + screen_t - SCREEN0[shot]
DUR = 31.6
M = Mix(DUR, seed=5)
bpm = 88; beat = 60 / bpm; bar = 4 * beat
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]   # Fmaj7 Em7 Dm7 Cmaj7
roots = [41, 40, 38, 36]
def epiano(m, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*hz(m)*tt) + 0.3*np.sin(2*np.pi*hz(m)*2*tt)*np.exp(-tt/0.3) + 0.08*np.sin(2*np.pi*hz(m)*3*tt)*np.exp(-tt/0.1)
    return s * env(n, 0.004, 1.2) * (1 + 0.15 * np.sin(2*np.pi*4.5*tt))
def soft_click(t, g):
    n = int(0.025 * SR); M.place(smooth(M.noise(n), 4) * env(n, .0003, .005), t, g, 0.1)
def incoming(t):
    M.place(blip(79, dur=0.09), t, 0.07, -0.1); M.place(blip(84, dur=0.07), t + 0.05, 0.045, -0.1)
def sent(t):
    M.place(whoosh(M, 0.22), t - 0.05, 0.045, 0.2); M.place(blip(88, dur=0.08), t, 0.055, 0.2)
def tapback(t):
    M.place(blip(91, dur=0.06), t, 0.045); M.place(blip(95, dur=0.06), t + 0.06, 0.035)

# Bedroom tone under everything before the end card, a soft Fmaj7 pad until the rewind
n = int(EDIT['end'] * SR)
M.place(0.012 * smooth(smooth(M.noise(n), 400), 400), 0, 1.0)
for m in [53, 57, 60, 64]: M.place(pad(m, EDIT['rewind']), 0, 0.012)
# Timeline A
M.place(bell(84, 0.25, 0.6), 0.05, 0.05); M.place(bell(88, 0.3, 0.8), 0.17, 0.05)   # notification (already shown when the shot starts)
M.place(blip(96, dur=0.03), at('open', 1.3), 0.04)                                                            # tap
for s in (2.75, 4.0, 5.35): incoming(at('chat', s))
for i in range(8): soft_click(at('type', 7.25 + i * 0.27), 0.16)
sent(at('type', 9.7))
tapback(at('mock', 10.5)); incoming(at('mock', 11.2)); incoming(at('mock', 12.0)); tapback(at('mock', 12.6))
# Rewind: tape chirps, then a low swell under "Et si…"
d = EDIT['etsi'] - EDIT['rewind']; n = int(d * SR); tt = np.arange(n) / SR
f = 300 + 1800 * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt)) * (tt / d)
M.place((np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + 0.5 * smooth(M.noise(n), 6)) * np.minimum(1, tt / 0.05) * np.minimum(1, (d - tt) / 0.1), EDIT['rewind'], 0.08)
M.place(tone(hz(29), 1.0, ((1, 1), (2, .3)), a=0.05, tau=0.6), EDIT['etsi'], 0.18)
for m in [53, 60, 64, 69]: M.place(pad(m, 0.95), EDIT['etsi'], 0.03)
# Lo-fi groove from the app to the end card
t = EDIT['app']; step = 0
while t < EDIT['end']:
    ci = int((t - EDIT['app']) // bar) % 4; k = step % 8
    if k == 0:
        for m in chords[ci]: M.place(epiano(m, min(bar, EDIT['end'] - t) + 0.05), t, 0.03, (m % 4 - 1.5) * 0.2)
    if k in (0, 5): M.place(smooth(kick(0.3, 48, 60, 0.11), 15), t + (0.02 if k == 5 else 0), 0.3)
    if k in (2, 6): M.place(smooth(clap(M), 9), t, 0.1)
    M.place(smooth(hat(M, 0.05, 0.01), 3), t + (0.03 if k % 2 else 0), 0.03 if k % 2 else 0.015, 0.3)
    if k in (0, 3, 4): M.place(smooth(tone(hz(roots[ci]), 0.4, ((1, 1), (2, .2)), a=.01, tau=.25), 15), t, 0.14)
    t += beat / 2; step += 1
# App: keys, Valider, sheet, vowels, share
for i in range(10): M.place(blip(96, dur=0.025), at('app', 15.5 + i * 0.17), 0.035)
M.place(blip(84, dur=0.05), at('app', 17.35), 0.05)
M.place(whoosh(M, 0.35), at('app', 17.65), 0.05)
for i, m in enumerate([81, 84, 86, 88, 93]): M.place(bell(m, 0.6), at('app', 18.4 + i * 0.16), 0.055, (i - 2) * 0.15)
for m in [53, 60, 64, 69, 72]: M.place(tone(hz(m), 1.4, ((1, 1), (2, .2)), a=.02, tau=.6), at('app', 19.3), 0.03)
M.place(blip(91, dur=0.04), at('app', 20.05), 0.04)
# Timeline B
sent(at('revenge', 21.0)); sent(at('revenge', 21.6)); tapback(at('revenge', 22.1))
for s in (22.6, 23.4): incoming(at('revenge', s))
sent(at('revenge', 24.2)); incoming(at('revenge', 25.35))
# End card: typewriter, erase, CONSONNE, final chord (end card timeline from endcard.html, offset 23.3)
E = lambda x: EDIT['end'] + x - 23.3
line = 'Zéro voyelle, zéro pitié.'
for i in range(len(line)): soft_click(E(23.45 + i / len(line)), 0.12)
for i in range(10): soft_click(E(25.3 + i * 0.03), 0.08)
M.place(kick(0.6, 42, 80, 0.3), E(25.75), 0.35)
for i, m in enumerate([81, 84, 88]): M.place(bell(m), E(26.3 + i * 0.16), 0.07)
for m in [53, 60, 64, 69, 72, 76]: M.place(tone(hz(m), 2.0, ((1, 1), (2, .2), (3, .06)), a=.01, tau=1.2, det=.002), E(26.8), 0.045)
M.write(sys.argv[1], fade_out=0.8)
print('ok')
