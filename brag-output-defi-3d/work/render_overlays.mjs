// End card (black, typed text, CONSONNE) from endcard.html, and transparent overlays for the rewind.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path'; import fs from 'node:fs';
const here = path.dirname(new URL(import.meta.url).pathname);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await pg.goto('file://' + path.join(here, 'endcard.html'));
await pg.evaluate(() => window.setup());
fs.mkdirSync(path.join(here, 'overlays/end'), { recursive: true });
for (let f = 0; f < 156; f++) {   // endcard.html runs its end card from 23.3 s
  await pg.evaluate(t => window.render(t), 23.3 + f / 30);
  await pg.screenshot({ path: path.join(here, `overlays/end/e${String(f + 1).padStart(4, '0')}.png`) });
}
const ov = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const icon = '<svg width="300" height="200" viewBox="0 0 30 20"><path d="M14 2L2 10l12 8zM28 2L16 10l12 8z" fill="#fff"/></svg>';
for (const [name, text] of [['rewind', ''], ['etsi', 'Et si…']]) {
  await ov.setContent(`<html><body style="margin:0;width:1080px;height:1920px;background:transparent;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;font-family:Inter,sans-serif">
    <div style="filter:drop-shadow(0 6px 24px rgba(0,0,0,.6))">${icon}</div>
    ${text ? `<div style="font-size:100px;font-weight:700;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.75)">${text}</div>` : ''}</body></html>`);
  await ov.screenshot({ path: path.join(here, `overlays/${name}.png`), omitBackground: true });
}
await b.close();
