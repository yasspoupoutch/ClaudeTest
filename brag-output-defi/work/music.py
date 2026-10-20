# Soundtrack for the "défi" video: D minor, 128 BPM, bouncy then loud.
import sys; from synth import *
M = Mix(21.5)
beat = 60 / 128; bar = 4 * beat
chords = [[62, 65, 69], [58, 62, 65], [60, 64, 67], [57, 61, 64]]   # Dm Bb C A
roots = [38, 34, 36, 33]
def section(t):
    if t < 7.6: return 'chat'
    if t < 8.5: return 'flash'
    if t < 11.6: return 'run'
    if t < 14.3: return 'chat'
    if t < 17.6: return 'punch'
    return 'outro'
t = 0.0; step = 0
while t < 17.6:
    ci = int(t // bar) % 4; sec = section(t); k = step % 8
    if sec in ('chat', 'run'):
        notes = chords[ci] + [chords[ci][0] + 12]
        M.place(pluck(notes[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12, 0.14), t, 0.045, 0.3 if k % 2 else -0.3)
        if k % 2 == 0: M.place(smooth(tone(hz(roots[ci]), 0.25, ((1, 1), (2, .3)), a=.003, tau=.1), 9), t, 0.15)
        if k in (0, 4): M.place(kick(), t, 0.3 if sec == 'run' else 0.22)
        if k in (2, 6): M.place(clap(M), t, 0.08 if sec == 'chat' else 0.11)
        M.place(hat(M), t, 0.03 if (k % 2 or sec == 'run') else 0.0, 0.25)
        if sec == 'run': M.place(hat(M, 0.04, 0.008), t + beat / 4, 0.022, -0.25)
    if k == 0 and sec in ('chat', 'run'):
        for m in chords[ci]: M.place(pad(m, bar), t, 0.022)
    t += beat / 2; step += 1
# Chat pops (in key)
pops = [(0.0, 74), (1.0, 77), (2.0, 69), (2.65, 72), (3.3, 65), (4.0, 77), (5.35, 81), (6.0, 86), (11.6, 86), (12.45, 69), (13.0, 72), (13.55, 65)]
for tm, m in pops: M.place(blip(m, up=m >= 81), tm, 0.09, 0.15)
M.place(riser(M, 0.9), 6.7, 0.07)
# Flash hit
M.place(kick(0.6, 40, 120, 0.3), 7.6, 0.45); M.place(smooth(M.noise(int(SR * 1.2)), 3) * env(int(SR * 1.2), .001, .35), 7.6, 0.08)
for m in [50, 62, 65, 69]: M.place(tone(hz(m), 0.9, ((1, 1), (2, .5), (3, .25)), a=.003, tau=.25), 7.6, 0.06)
# Speed run: thump + rising ding per word
for i in range(5):
    t0 = 8.5 + i * 0.6
    M.place(whoosh(M, 0.2), t0 - 0.08, 0.05)
    M.place(bell([74, 77, 81, 84, 86][i], 0.3, 0.8), t0 + 0.34, 0.06)
# Punch lines: big stabs
for i, t0 in enumerate([14.3, 15.4, 16.5]):
    M.place(kick(0.6, 42, 110, 0.25), t0, 0.42); M.place(clap(M), t0, 0.12)
    for m in [[50, 62, 65, 69], [46, 58, 62, 65], [45, 57, 61, 64]][i]:
        M.place(tone(hz(m), 1.0, ((1, 1), (2, .45), (3, .2)), a=.003, tau=.35), t0, 0.06)
    M.place(smooth(M.noise(int(SR * .5)), 3) * env(int(SR * .5), .001, .12), t0, 0.04)
# Outro
M.place(kick(0.6, 42, 80, 0.3), 17.6, 0.38)
for m in [62, 69, 74, 77]: M.place(pad(m, 3.9), 17.6, 0.03)
for i, m in enumerate([74, 77, 81]): M.place(bell(m), 18.3 + i * 0.16, 0.07)
for m in [50, 62, 69, 74, 76, 77]: M.place(tone(hz(m), 2.6, ((1, 1), (2, .2), (3, .06)), a=.01, tau=1.4, det=.002), 18.9, 0.045)
M.place(blip(79), 19.7, 0.09); M.place(bell(86, 0.6), 19.85, 0.03)
M.write(sys.argv[1])
print('ok')
