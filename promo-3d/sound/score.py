# Soundtrack of the 3D promo, timed on the script (src/Promo.tsx). A minor, 120 BPM.
import sys; from synth import *
DUR = 21.5
M = Mix(DUR, seed=21)
beat = 0.5; bar = 2.0
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55, 60], [55, 59, 62]]   # Am F C G
roots = [45, 41, 48, 43]
def hum(t0, d, f0=110, f1=220, g=0.05):
    n = int(d * SR); tt = np.arange(n) / SR; f = f0 + (f1 - f0) * (tt / d) ** 1.5
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + np.sin(2 * np.pi * np.cumsum(f * 2) / SR) * 0.5
    M.place(smooth(s, 30) * np.minimum(1, tt / 0.1) * np.minimum(1, (d - tt) / 0.2), t0, g)
def zip_(t, g=0.04):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    M.place(np.sin(2 * np.pi * np.cumsum(1800 + 2600 * tt / 0.09) / SR) * env(n, 0.002, 0.03), t, g, 0.2)
def click(t, g=0.13):
    n = int(0.03 * SR); M.place(smooth(M.noise(n), 4) * env(n, .0003, .006) + 0.3 * tone(2400, 0.03, a=.0005, tau=.006), t, g, 0.1)
def swoosh(t, d=0.5, g=0.06): M.place(whoosh(M, d), t - d / 2, g)
def low_hit(t, g=0.35): M.place(kick(0.7, 38, 90, 0.35), t, g)

# Pad under everything
for b in range(int(DUR / bar) + 1):
    t0 = b * bar; ci = b % 4
    if t0 >= 17.0: ci = 0
    for m in chords[ci]: M.place(pad(m, bar + 0.4), t0, 0.022 if t0 < 8.6 else 0.03)
# Rhythm sections
t = 0.0; step = 0
while t < 17.0:
    ci = int(t // bar) % 4; k = step % 8
    full = 8.65 <= t < 17.0
    pulse = t < 6.3
    if pulse and k % 2 == 0: M.place(smooth(tone(hz(roots[ci] - 12), 0.35, ((1, 1), (2, .2)), a=.01, tau=.18), 25), t, 0.18)
    if t >= 2.0 and (pulse or full) and k % 2: M.place(hat(M), t, 0.03, 0.25)
    if t >= 3.8 and pulse and k in (0, 4): M.place(kick(0.3, 48, 60, 0.1), t, 0.18)
    if full:
        if k in (0, 4): M.place(kick(), t, 0.3)
        if k in (2, 6): M.place(clap(M), t, 0.09)
        if k % 2 == 0: M.place(smooth(tone(hz(roots[ci] - 12), 0.3, ((1, 1), (2, .3)), a=.004, tau=.13), 9), t, 0.16)
        notes = chords[ci] + [chords[ci][0] + 12]
        M.place(pluck(notes[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12, 0.15), t, 0.035, 0.3 if k % 2 else -0.3)
    t += beat / 2; step += 1
# 0-2: the riddle — chrono ticks
for tt in (0.25, 1.25): click(tt, 0.08)
low_hit(0.0, 0.25)
# 1.35: the gold slots light up where the vowels are missing; 2.15-3.5 the neon links them and runs to the answer field
swoosh(1.2, 0.5, 0.05)
for i in range(5): M.place(bell(88 + [0, 2, 4, 7, 9][i], 0.25, 0.6), 1.38 + i * 0.07, 0.035, (i - 2) * 0.2)
hum(2.15, 1.4, 90, 260, 0.04)
for i in range(5): zip_(2.2 + i * 0.13)
swoosh(2.9, 0.5); M.place(bell(81, 0.5), 3.35, 0.05)
# 3.8-6.3: typing CHOUCROUTE, Valider
for i in range(10): click(4.0 + i * 0.2)
click(6.05, 0.2); M.place(tone(hz(69), 0.2, ((1, 1),), a=.002, tau=.05), 6.05, 0.06)
M.place(riser(M, 0.9), 5.4, 0.05)
# 6.3: the card leaves the screen, vowels fly in, flip, back down
low_hit(6.3, 0.3); swoosh(6.6, 0.8, 0.07)
for i, m in enumerate([81, 84, 86, 88, 91]): M.place(bell(m, 0.8), 7.3 + i * 0.26 + 0.3, 0.06, (i - 2) * 0.2)
for m in [57, 64, 69, 72, 76]: M.place(tone(hz(m), 2.0, ((1, 1), (2, .25), (3, .08)), a=.01, tau=1.0, det=.002), 8.65, 0.04)
low_hit(8.65, 0.3)
M.place(smooth(M.noise(int(0.12 * SR)), 3) * env(int(0.12 * SR), .001, .03), 9.0, 0.12)        # flip
M.place(bell(93, 0.5), 9.55, 0.05)                                                                 # 0:38
swoosh(10.4, 0.6, 0.06)
# 11-15: mode cards rise, small cues
for t0 in (11.0, 12.2, 13.4): swoosh(t0 + 0.3, 0.6, 0.06)
for i in range(4): M.place(blip(84 + [0, 3, 5, 7][i], dur=0.06), 11.5 + i * 0.12, 0.04)
M.place(kick(0.4, 45, 60, 0.15), 12.9, 0.2)
M.place(bell(88, 0.5), 13.9, 0.045); M.place(bell(83, 0.5), 14.15, 0.045)
# 15-17: leaderboard, neon loop around "Vous"
swoosh(15.2, 0.6, 0.06); hum(15.5, 0.9, 150, 300, 0.035); M.place(blip(91, dur=0.07), 16.2, 0.05)
# 17-20.5: phone stands, neon writes the name, vowels drop
low_hit(17.0, 0.3); hum(17.9, 0.65, 200, 420, 0.04)
for i, m in enumerate([81, 84, 88]): M.place(bell(m, 0.9), 18.75 + i * 0.16 + 0.15, 0.065)
for m in [45, 57, 64, 69, 72, 76]: M.place(tone(hz(m), 2.3, ((1, 1), (2, .2), (3, .06)), a=.01, tau=1.3, det=.002), 19.2, 0.045)
# End card: icon and App Store badge, then the TikTok account
M.place(blip(88, dur=0.08), 19.4, 0.05); M.place(blip(93, dur=0.08), 19.58, 0.045)
M.write(sys.argv[1], fade_out=1.0)
print('ok')
