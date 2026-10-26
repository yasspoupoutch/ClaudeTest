// Shared by the CNSNN promo concepts: the app's game screen, vowel slots, countdown ring and the App Store end card.
const APPLE = 'M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701';
const TIKTOK = 'M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z';

// A word written as in the game: consonants shown, a gold slot where each vowel goes.
// fill(L, pFor) grows vowel j from its slot to its letter as pFor(j) goes 0 -> 1.
function buildSlots(el, word) {
  el.classList.add('slots'); el.innerHTML = '';
  return [...word].map(c => { const sp = document.createElement('span'); const v = isVowel(c);
    sp.innerHTML = v ? `<b>${c}</b><i></i>` : c; if (v) sp.className = 'v'; if (c === ' ') sp.style.minWidth = '0.32em'; el.appendChild(sp); return { sp, c, v }; });
}
function measureSlots(L) { L.forEach(l => { l.sp.style.width = ''; l.w = l.sp.offsetWidth; }); }   // layout widths, unaffected by transforms
function fill(L, pFor) {
  let j = 0; L.forEach(l => { if (!l.v) return; const p = pFor(j++), k = clamp(p);
    l.sp.style.width = lerp(l.w * 0.62, l.w, k) + 'px';
    l.sp.querySelector('b').style.opacity = clamp(p * 1.6); l.sp.querySelector('i').style.opacity = 1 - clamp(p * 2.5);
    l.sp.querySelector('b').style.display = 'inline-block'; l.sp.querySelector('b').style.transform = `translateY(${-0.4 * (1 - k)}em) scale(${lerp(0.6, 1, k)})`; });
}

// The game screen of the app, with the real layout and keyboard. ids are prefixed so that two phones can coexist.
const KB_ROWS = ['AZERTYUIOP', 'QSDFGHJKLM', 'WXCVBN'];
function appScreen(id, { cat = 'Général · Difficile', hint = '' } = {}) {
  const kb = KB_ROWS.map(r => `<div class="kr">${[...r].map(c => `<i data-k="${c}" class="${'AEIOUY'.includes(c) ? 'g' : ''}">${c}</i>`).join('')}</div>`).join('');
  return `<div class="scr app"><div class="isl"></div><div class="sb"><span>20:31</span><span>●●● ▮</span></div>
    <div class="xb">✕</div><div class="hd"><b>Mot du jour</b><small>${cat}</small></div><div class="chr" id="${id}-chr">0:00</div>
    <div class="hw" id="${id}-hw"></div><div class="rule"></div><div class="hint">${hint}</div>
    <div class="ans" id="${id}-ans"><em>votre réponse</em></div><div class="msg" id="${id}-msg"></div>
    <div class="kb">${kb}<div class="val" id="${id}-val">Valider</div></div></div>`;
}
const chrono = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
// typing: a word typed letter by letter from t0, one key every dt; the pressed key flashes
function typeInto(id, word, t, t0, dt) {
  const n = clamp(Math.floor((t - t0) / dt) + 1, 0, word.length), ans = document.getElementById(id + '-ans');
  if (t < t0) return 0;
  ans.textContent = word.slice(0, n);
  document.querySelectorAll(`#${id} .kr i`).forEach(k => { k.style.filter = ''; k.style.transform = ''; });
  const cur = word[n - 1], since = t - t0 - (n - 1) * dt;
  if (n <= word.length && since < 0.12 && cur) { const k = document.querySelector(`#${id} .kr i[data-k="${cur}"]`); if (k) { k.style.filter = 'brightness(1.8)'; k.style.transform = 'scale(1.15)'; } }
  return n;
}

// Countdown ring: build once, then ring(el, p, digit)
function makeRing(el, color = '#ffc65a') {
  el.innerHTML = `<svg width="220" height="220" viewBox="0 0 220 220"><circle cx="110" cy="110" r="96" stroke="rgba(255,255,255,.12)"/>
    <circle class="arc" cx="110" cy="110" r="96" stroke="${color}" stroke-linecap="round" transform="rotate(-90 110 110)" style="filter: drop-shadow(0 0 10px ${color})"/></svg><b></b>`;
}
function ring(el, p, digit) { const c = 2 * Math.PI * 96; const a = el.querySelector('.arc'); a.style.strokeDasharray = c; a.style.strokeDashoffset = c * p; el.querySelector('b').textContent = digit; }

// End card: "CNSNN", typed in the App Store search, the app as result, CONSONNE, free.
function buildEnd() {
  const d = document.createElement('div'); d.id = 'end';
  d.innerHTML = `<div id="e-mark"></div><div id="e-tag">Le mot du jour. Sans ses voyelles.</div><div id="e-cap">Tape CNSNN sur l’App Store</div>
    <div id="search"><svg width="44" height="44" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="#8e8e93" stroke-width="2.4"/><path d="M15.5 15.5 L21 21" stroke="#8e8e93" stroke-width="2.6" stroke-linecap="round"/></svg><span id="typed"></span><i id="caret"></i><em id="sph">Jeux, apps, articles…</em></div>
    <div id="result"><img src="appicon.png"><div class="ri"><b>CNSNN</b><small>Jeu de mots</small></div><div id="get">Obtenir</div></div>
    <div id="free"><span>GRATUIT</span></div>
    <div id="tiktok"><svg width="58" height="58" viewBox="0 0 24 24"><path class="tt" fill="#25F4EE" transform="translate(-0.7,-0.5)"/><path class="tt" fill="#FE2C55" transform="translate(0.7,0.5)"/><path class="tt" fill="#fff"/></svg>@jeuCNSNN</div>`;
  $('stage').appendChild(d);
  d.querySelectorAll('.tt').forEach(p => p.setAttribute('d', TIKTOK));
  fitFont($('e-mark'), 'CONSONNE', 940, 190); END_L = buildWord($('e-mark'), 'CONSONNE'); measure(END_L);
}
let END_L;
function renderEnd(t, t0) {
  const lt = t - t0; set($('end'), lt >= 0 ? 1 : 0); if (lt < 0) return;
  const mk = ease(prog(lt, 0, 0.45)); set($('e-mark'), mk, `scale(${lerp(1.2, 1, mk)})`);
  reveal(END_L, i => spring(lt - (3.3 + i * 0.18)));                       // "it's just consonne without its vowels"
  const tg = ease(prog(lt, 0.4, 0.8)); set($('e-tag'), tg, `translateY(${(1 - tg) * 20}px)`);
  const cp = ease(prog(lt, 0.8, 1.2)); set($('e-cap'), cp, `translateY(${(1 - cp) * 20}px)`);
  const sb = spring(lt - 1.0, 0.5, 0.75); set($('search'), clamp(sb * 1.4), `translateY(${(1 - sb) * 40}px)`);
  const typed = 'CNSNN'.slice(0, clamp(Math.floor((lt - 1.5) / 0.26) + 1, 0, 5)); $('typed').textContent = lt >= 1.5 ? typed : '';
  $('sph').style.opacity = lt >= 1.5 ? 0 : 1; $('caret').style.opacity = Math.floor(t * 2.2) % 2 || (lt > 1.4 && lt < 2.9) ? 1 : 0;
  const rs = spring(lt - 2.8, 0.5, 0.7); set($('result'), clamp(rs * 1.4), `translateY(${(1 - rs) * 40}px)`);
  const fr = spring(lt - 4.0, 0.45, 0.55); set($('free'), clamp(fr * 1.5), `scale(${lerp(0.6, 1, clamp(fr))})`);
  const on = lt > 4.0; $('get').style.background = on ? '#0a84ff' : '#2c2c2e'; $('get').style.color = on ? '#fff' : '#0a84ff';
  $('get').style.transform = `scale(${1 + 0.1 * Math.exp(-Math.pow((lt - 4.1) / 0.15, 2))})`;
  const tk = spring(lt - 4.4, 0.5, 0.75); set($('tiktok'), clamp(tk * 1.4), `translateY(${(1 - tk) * 40}px)`);
}
// End-card sound cues for music.py (relative to t0): search keys, result, vowels into CONSONNE, "free"
