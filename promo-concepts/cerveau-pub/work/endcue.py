"""Sound cues of the shared App Store end card (kit.js renderEnd), relative to its start t0; same cue names as END_CUES."""
from synth import *
def end_cues(M, t0, search=1.0, type=1.5, result=2.8, consonne=3.3, free=4.0):
    M.place(whoosh(M, 0.5), t0 - 0.25, 0.08)
    for i in range(5): M.place(tone(1800, 0.04, ((1, 1),), a=0.0005, tau=0.01), t0 + type + i * 0.26, 0.07)   # keys of the search
    M.place(blip(84, dur=0.08), t0 + result, 0.05)                                                            # the app shows up
    for i, m in enumerate([76, 79, 83]): M.place(bell(m, 0.9), t0 + consonne + 0.1 + i * 0.18, 0.06)        # vowels into CONSONNE
    M.place(blip(88, dur=0.08), t0 + free, 0.06); M.place(blip(95, dur=0.1), t0 + free + 0.12, 0.05)        # "Obtenir", free
    for m in [40, 52, 59, 64, 67, 71]: M.place(tone(hz(m), 2.5, ((1, 1), (2, .2), (3, .06)), a=0.01, tau=1.3, det=0.002), t0 + free, 0.035)
