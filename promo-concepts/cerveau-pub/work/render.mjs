import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path'; import fs from 'node:fs';
const [mode, ...rest] = process.argv.slice(2);
const here = path.dirname(new URL(import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.setDefaultTimeout(180000);
page.on('pageerror', e => console.error('PAGE ERROR', e.message));
const cut = process.env.CUT || '25';   // which ad cut to render: 6, 15 or 25 seconds
await page.goto('file://' + path.join(here, 'composition.html') + '#cut=' + cut);
await page.evaluate(() => window.setup());
async function shot(t, file) { await page.evaluate(t => window.render(t), t); await page.screenshot({ path: file, type: 'jpeg', quality: 93 }); }
if (mode === 'stills') {
  fs.mkdirSync(path.join(here, 'stills'), { recursive: true });
  for (const t of rest.map(Number)) await shot(t, path.join(here, 'stills', `c${cut}_t${t.toFixed(2)}.jpg`));
} else {
  const fps = 30, dur = Number(rest[0] || 21), dir = path.join(here, 'frames_' + cut);
  fs.mkdirSync(dir, { recursive: true });
  const [from, to] = [Number(rest[1] || 0), Number(rest[2] || Math.round(dur * fps))];
  for (let f = from; f < to; f++) await shot(f / fps, path.join(dir, `f${String(f).padStart(4, '0')}.jpg`));
}
await browser.close();
