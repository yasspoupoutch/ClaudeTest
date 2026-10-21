import React from 'react';
import { Img, continueRender, delayRender, staticFile, useCurrentFrame } from 'remotion';
import { FPS, clamp, ease, prog, spring } from './kit';

// Brand marks as vector paths (Simple Icons, CC0): Apple and TikTok.
const APPLE = 'M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701';
const TIKTOK = 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z';

/** The app fonts, loaded before any frame that uses them is captured. */
let fontsReady = false;
const FontFaces: React.FC = () => {
  if (!fontsReady && typeof document !== 'undefined') {
    fontsReady = true;
    const h = delayRender('end card fonts');
    const faces = [
      new FontFace('Fraunces', `url(${staticFile('fonts/Fraunces-Black.ttf')})`, { weight: '900' }),
      new FontFace('Instrument Serif', `url(${staticFile('fonts/InstrumentSerif-Italic.ttf')})`, { style: 'italic' }),
    ];
    Promise.all(faces.map((f) => f.load())).then((fs) => { fs.forEach((f) => (document.fonts as any).add(f)); continueRender(h); }, () => continueRender(h));
  }
  return null;
};

const IN = 19.35;   // seconds: the end card rises after CONSONNE and its tagline
const END = 17.0;   // the phone stands up; CNSNN is drawn from END + 0.9

/** Bottom of the last shot: app icon + App Store badge, and the TikTok account. */
/** Top of the last shot, drawn in HTML so it stays sharp: a gold light line writes CNSNN, the vowels drop into CONSONNE. */
const Wordmark: React.FC<{ t: number }> = ({ t }) => {
  if (t < END + 0.85) return null;
  const sweep = clamp((t - (END + 0.9)) / 0.65);
  const letters = 'CONSONNE'.split('');
  let vi = 0;
  const tag = ease(prog(t, END + 2.3, END + 2.7));   // with the voice: "Le mot du jour…"
  const lineFade = 1 - 0.75 * prog(t, END + 1.6, END + 2.3);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, top: 118, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ display: 'flex', fontFamily: 'Fraunces', fontWeight: 900, fontSize: 108, letterSpacing: 2, lineHeight: 1, height: 116, whiteSpace: 'nowrap' }}>
        {letters.map((c, i) => {
          const vowel = 'AEIOU'.includes(c);
          if (vowel) {
            const p = spring(t - (END + 1.75 + vi++ * 0.16), 0.42, 0.62);
            return <span key={i} style={{ color: '#ffc65a', display: 'inline-block', maxWidth: `${Math.max(0, p)}em`, textAlign: 'center',
              opacity: clamp(p), transform: `translateY(${(1 - clamp(p)) * -60}px) scale(${0.6 + 0.4 * clamp(p)})` }}>{c}</span>;
          }
          const x = i / (letters.length - 1);
          return <span key={i} style={{ color: '#f4f5f8', opacity: clamp((sweep - x * 0.85) * 5) }}>{c}</span>;
        })}
      </div>
      <div style={{ width: 760, height: 4, marginTop: 14, borderRadius: 2, background: '#ffd36e', transformOrigin: 'left', transform: `scaleX(${sweep})`,
        opacity: lineFade, boxShadow: '0 0 18px 4px rgba(255,198,90,.75)' }} />
      <div style={{ marginTop: 26, fontFamily: 'Instrument Serif', fontStyle: 'italic', fontSize: 56, color: '#f4f5f8', opacity: tag, transform: `translateY(${(1 - tag) * 20}px)` }}>
        Le mot du jour. Sans ses voyelles.
      </div>
    </div>
  );
};

export const EndCard: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  if (t < END + 0.85) return null;
  if (t < IN - 0.1) return <div style={{ position: 'absolute', inset: 0 }}><FontFaces /><Wordmark t={t} /></div>;
  const a = spring(t - IN, 0.5, 0.75), b = spring(t - IN - 0.18, 0.5, 0.75), c = ease(prog(t, IN + 0.4, IN + 0.8));
  const scrim = ease(prog(t, IN - 0.1, IN + 0.4));
  const up = (p: number) => ({ opacity: clamp(p * 1.4), transform: `translateY(${(1 - p) * 40}px)` });
  return (
    <div style={{ position: 'absolute', inset: 0, fontFamily: 'Inter, sans-serif', color: '#f4f5f8' }}>
      <FontFaces /><Wordmark t={t} />
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 760, opacity: scrim,
        background: 'linear-gradient(rgba(8,5,3,0), rgba(8,5,3,.82) 42%, rgba(8,5,3,.92))' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1290, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 34, ...up(a) }}>
        <Img src={staticFile('brand/appicon.png')} style={{ width: 190, height: 190, borderRadius: 43, boxShadow: '0 18px 40px rgba(0,0,0,.55), 0 0 0 2px rgba(255,255,255,.12)' }} />
        <div style={{ height: 158, padding: '0 46px 0 34px', borderRadius: 34, background: '#000', border: '3px solid #a6a6a6', display: 'flex', alignItems: 'center', gap: 20 }}>
          <svg width="78" height="78" viewBox="0 0 24 24"><path d={APPLE} fill="#fff" /></svg>
          <div style={{ lineHeight: 1.05 }}>
            <div style={{ fontSize: 34, fontWeight: 500, letterSpacing: 0.3 }}>Télécharger dans</div>
            <div style={{ fontSize: 66, fontWeight: 600, letterSpacing: -1 }}>l’App Store</div>
          </div>
        </div>
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1520, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 22, ...up(b) }}>
        <svg width="62" height="62" viewBox="0 0 24 24">
          <path d={TIKTOK} fill="#25F4EE" transform="translate(-0.7,-0.5)" />
          <path d={TIKTOK} fill="#FE2C55" transform="translate(0.7,0.5)" />
          <path d={TIKTOK} fill="#fff" />
        </svg>
        <div style={{ fontSize: 54, fontWeight: 700, letterSpacing: 0.5 }}>@jeuCNSNN</div>
      </div>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1625, textAlign: 'center', fontSize: 30, fontWeight: 600, letterSpacing: 6, color: '#ffc65a', opacity: c }}>
        GRATUIT · SANS PUBLICITÉ
      </div>
    </div>
  );
};
