# Supertonic 3 voice (M1) for the Sprint edit, then the timeline the edit follows.
# The game (recording 5.3 → 81.5 s) plays at SPEED; each line is placed at a target time, pushed later if the previous one is still talking.
import json, numpy as np, soundfile as sf
from supertonic import TTS
tts = TTS(model='supertonic-3', auto_download=False); V = tts.get_voice_style('M1'); SR = 44100
SPEED, G0, G1, R1 = 2.8, 5.3, 81.5, 85.5        # game speed-up, game start/end and result end in the recording
def say(text, speed=1.22):
    wav, _ = tts.synthesize(text, voice_style=V, lang='fr', total_steps=16, speed=speed)
    a = np.asarray(wav, dtype=np.float32).reshape(-1); nz = np.nonzero(np.abs(a) > 0.01)[0]
    return a[max(0, nz[0] - 800):nz[-1] + 1600] if len(nz) else a
hook = say('Le record du Sprint ? Dix-huit mots… en quatre-vingt-dix secondes.')
TH = 0.25 + len(hook) / SR + 0.35                 # the game starts right after the hook
game = lambda src: TH + (src - G0) / SPEED          # recording time → edit time
TR = game(G1); TE = TR + (R1 - G1)
lines = [
    (0.25, hook, 'hook'),
    (TH + 0.3, say('Un mot sans voyelles. Tu retrouves, tu valides… et le suivant arrive direct.'), 'rule'),
    (game(40.0), say('Trois bonnes réponses d’affilée ? Combo fois trois !'), 'combo'),
    (game(58.0), say('Et le chrono, lui, ne s’arrête jamais.'), 'clock'),
    (game(74.0), say('Dernières secondes… vite !'), 'last'),
    (TR + 0.3, say('Sept mots. Pas mal… mais très loin du record.'), 'result'),
    (TE + 0.2, say('Et toi, tu en fais combien ? Le Sprint, c’est dans Consonne. Gratuit sur l’App Store.'), 'cta'),
]
tl, t_free, clips = {'TH': TH, 'TR': TR, 'TE': TE, 'speed': SPEED, 'g0': G0, 'g1': G1, 'r1': R1}, 0, []
for want, a, key in lines:
    s = max(want, t_free + 0.15); clips.append((s, a)); tl[key] = s; tl[key + '_d'] = len(a) / SR; t_free = s + len(a) / SR
tl['end'] = round(max(t_free + 2.4, TE + 4.5), 2)
out = np.zeros(int(tl['end'] * SR) + SR, np.float32)
for s, a in clips: i = int(s * SR); out[i:i + len(a)] += a[:len(out) - i]
sf.write('voice.wav', out[:int(tl['end'] * SR)], SR)
json.dump(tl, open('timeline.json', 'w')); open('tl.js', 'w').write('window.TL = ' + json.dumps(tl) + ';\n')
print(json.dumps(tl))
