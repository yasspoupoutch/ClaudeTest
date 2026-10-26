// Shared helpers for the CNSNN brag compositions: easing, springs, vowel reveal, ambient background.
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const prog = (t, a, b) => clamp((t - a) / (b - a));
function bezier(x1, y1, x2, y2) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = u => ((ax * u + bx) * u + cx) * u, sy = u => ((ay * u + by) * u + cy) * u;
  return x => { if (x <= 0) return 0; if (x >= 1) return 1; let u = x;
    for (let i = 0; i < 8; i++) { const d = (3 * ax * u + 2 * bx) * u + cx; if (Math.abs(d) < 1e-6) break; u -= (sx(u) - x) / d; }
    return sy(clamp(u)); };
}
const ease = bezier(0.2, 0.9, 0.25, 1);   // CNSNNTheme.ease
const io = bezier(0.65, 0, 0.35, 1);
function spring(t, response = 0.42, damping = 0.62) {
  if (t <= 0) return 0;
  const w = 2 * Math.PI / response, wd = w * Math.sqrt(1 - damping * damping);
  return 1 - Math.exp(-damping * w * t) * (Math.cos(wd * t) + (damping * w / wd) * Math.sin(wd * t));
}
const set = (el, op, tf = '') => { el.style.opacity = op; el.style.transform = tf; el.style.visibility = op <= 0.001 ? 'hidden' : 'visible'; };
const isVowel = c => 'AEIOUYÀÂÉÈÊËÎÏÔÛÙ'.includes(c);
// VowelReveal: consonants stay, vowels grow into the gaps
function buildWord(el, word) {
  el.innerHTML = '';
  return [...word].map(c => { const s = document.createElement('span'); s.textContent = c; s.style.display = 'inline-block';
    if (isVowel(c)) { s.className = 'v'; s.style.display = 'inline-flex'; s.style.justifyContent = 'center'; }
    el.appendChild(s); return { el: s, v: isVowel(c), w: 0 }; });
}
function measure(letters) { letters.forEach(l => { l.el.style.width = ''; l.w = l.el.getBoundingClientRect().width; }); }
function reveal(letters, pFor) {
  let i = 0; letters.forEach(l => { if (!l.v) return; const p = pFor(i++);
    l.el.style.width = Math.max(0, l.w * p) + 'px'; l.el.style.opacity = Math.pow(clamp(p), 1.6);
    l.el.style.transform = `translateY(${-0.35 * (1 - clamp(p))}em) scale(${lerp(0.6, 1, clamp(p))})`; });
}
function fitFont(el, word, maxWidth, base = 200) {
  el.style.fontSize = base + 'px';
  const s = document.createElement('span'); s.style.display = 'inline-block'; s.style.whiteSpace = 'nowrap'; s.textContent = word; el.appendChild(s);
  const fs = Math.min(base, Math.floor(base * maxWidth / s.getBoundingClientRect().width)); s.remove(); el.style.fontSize = fs + 'px'; return fs;
}
// AmbientBackground: two cool blobs drifting slowly
function ambient(t, opacity) {
  const sc = 1080 / 390;
  const d1 = (1 - Math.cos(Math.PI * 2 * t / 32)) / 2, d2 = (1 - Math.cos(Math.PI * 2 * t / 38)) / 2;
  [[$('b1'), '89,62,199', -80, -60, 90, 140, 1, 1.25, d1], [$('b2'), '0,125,134', 170, 420, -110, -120, 1.1, 0.9, d2]].forEach(([el, rgb, x, y, dx, dy, s0, s1, d]) => {
    const size = (360 + 140) * sc;
    el.style.width = el.style.height = size + 'px';
    el.style.background = `radial-gradient(closest-side, rgba(${rgb},1), rgba(${rgb},.55) 70%, rgba(${rgb},0))`;
    el.style.left = (x - 70) * sc + 'px'; el.style.top = ((y - 70) * sc + 200) + 'px';
    el.style.opacity = opacity;
    el.style.transform = `translate(${dx * d * sc}px, ${dy * d * sc}px) scale(${lerp(s0, s1, d)})`;
  });
}
