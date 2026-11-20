"""Tiny numpy synth shared by the CNSNN brag soundtracks."""
import numpy as np, wave
SR = 44100
class Mix:
    def __init__(self, dur, seed=7):
        self.dur = dur; self.n = int(SR * dur); self.buf = np.zeros((self.n, 2)); self.rng = np.random.default_rng(seed)
    def place(self, sig, t, gain=1.0, pan=0.0):
        i = int(t * SR); j = min(self.n, i + len(sig))
        if i >= self.n or j <= i: return
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.buf[i:j, 0] += sig[:j - i] * gain * l * 1.414
        self.buf[i:j, 1] += sig[:j - i] * gain * r * 1.414
    def noise(self, n): return self.rng.standard_normal(n)
    def write(self, path, fade_out=1.2):
        t = np.arange(self.n) / SR; m = self.buf
        m *= np.minimum(1, t / 0.03)[:, None] * np.clip((self.dur - t) / fade_out, 0, 1)[:, None] ** 1.5
        m = np.tanh(m * 1.3) / np.tanh(1.3); m *= 0.89 / np.max(np.abs(m))
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype('<i2').tobytes())
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def env(n, a, tau):
    t = np.arange(n) / SR; e = np.exp(-t / tau); ai = int(a * SR)
    if ai > 0: e[:ai] *= np.linspace(0, 1, ai)
    return e
def smooth(x, k):
    w = np.hanning(k); return np.convolve(x, w / w.sum(), mode='same')
def tone(f, dur, harm=((1, 1),), a=0.005, tau=0.4, det=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for h, g in harm:
        s += g * np.sin(2 * np.pi * f * h * t)
        if det: s += g * 0.6 * np.sin(2 * np.pi * f * h * (1 + det) * t + 1.3)
    return s * env(n, a, tau)
def pad(m, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = np.sin(2*np.pi*hz(m)*tt) + 0.5*np.sin(2*np.pi*hz(m)*1.003*tt + 1) + 0.18*np.sin(2*np.pi*hz(m)*2*tt)
    return s * np.minimum(1, tt / 0.4) * np.minimum(1, (dur - tt) / 0.5)
def kick(dur=0.35, lo=50, hi=90, tau=0.12):
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(lo + hi * np.exp(-tt / 0.03)) / SR) * env(n, 0.001, tau)
def hat(mix, dur=0.06, tau=0.012):
    n = int(dur * SR); return np.diff(mix.noise(n + 1)) * env(n, 0.0005, tau)
def clap(mix):
    n = int(0.18 * SR); s = smooth(mix.noise(n), 5) - smooth(mix.noise(n), 40); return s * env(n, 0.002, 0.05)
def bell(m, tau=0.9, dur=2.5):
    return tone(hz(m), dur, ((1, 1), (2.0, 0.3), (3.01, 0.12), (4.2, 0.05)), a=0.002, tau=tau)
def pluck(m, tau=0.18):
    return tone(hz(m), 0.6, ((1, 1), (2, 0.35), (3, 0.12)), a=0.002, tau=tau)
def blip(m, up=True, dur=0.12):
    n = int(dur * SR); tt = np.arange(n) / SR; f0 = hz(m)
    f = f0 * (1 + (0.25 if up else -0.2) * tt / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04)
def whoosh(mix, d=0.35):
    n = int(d * SR); tt = np.arange(n) / SR
    return smooth(mix.noise(n), 12) * np.sin(np.pi * tt / d) ** 2
def riser(mix, d):
    n = int(d * SR); tt = np.arange(n) / SR
    return smooth(mix.noise(n), 6) * (tt / d) ** 2
