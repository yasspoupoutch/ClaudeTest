// Renders the app screens and card faces used as textures in the 3D scene (public/tex/*.png).
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path'; import fs from 'node:fs';
const here = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(here, '../public/tex'); fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1179, height: 2556 } });
await pg.goto('file://' + path.join(here, 'screens.html'));
async function shot(name, kind, opts, w, h) {
  await pg.evaluate(([k, o]) => window.show(k, o), [kind, opts]);
  await pg.screenshot({ path: path.join(out, name + '.png'), clip: { x: 0, y: 0, width: w, height: h }, omitBackground: true });
}
const WORD = 'CHOUCROUTE';
await shot('game_00', 'game', { chrono: '0:24' }, 1179, 2556);
await shot('game_slots', 'game', { chrono: '0:24', slots: true }, 1179, 2556);
await shot('game_answer', 'game', { chrono: '0:24', answerGlow: true }, 1179, 2556);
for (let i = 1; i <= WORD.length; i++) await shot(`game_${String(i).padStart(2, '0')}`, 'game', { typed: WORD.slice(0, i), down: WORD[i - 1], chrono: '0:' + (24 + Math.round(i * 1.3)) }, 1179, 2556);
await shot('game_valid', 'game', { typed: WORD, validDown: true, chrono: '0:38' }, 1179, 2556);
await shot('game_lifted', 'game', { typed: WORD, lifted: true, chrono: '0:38' }, 1179, 2556);
await shot('game_result', 'game', { typed: WORD, sheet: true, chrono: '0:38' }, 1179, 2556);
await shot('board', 'board', {}, 1179, 2556);
await shot('card_front', 'cardFront', {}, 1200, 900);
await shot('card_back', 'cardBack', {}, 1200, 900);
for (const k of ['sprint', 'survie', 'double']) await shot(`mode_${k}`, 'mode', { kind: k }, 900, 1125);
await b.close();
console.log(fs.readdirSync(out).length, 'textures');
