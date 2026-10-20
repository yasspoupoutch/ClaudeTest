# Sound for the 3D test shot: quiet bedroom tone, soft pad, message arrivals (screen time 1.7 -> shot time 0).
import sys; from synth import *
M = Mix(4.8, seed=11)
off = 1.7
n = M.n
M.place(0.03 * smooth(M.noise(n), 300) + 0.004 * smooth(M.noise(n), 8), 0, 1.0)          # room tone
for m in [53, 57, 60, 64]: M.place(pad(m, 4.8), 0, 0.012)                                  # very soft pad (Fmaj7)
for at in (2.75, 4.0, 5.35):                                                               # incoming message
    M.place(blip(79, dur=0.09), at - off, 0.07, -0.1); M.place(blip(84, dur=0.07), at - off + 0.05, 0.045, -0.1)
M.write(sys.argv[1], fade_out=0.4)
print('ok')
