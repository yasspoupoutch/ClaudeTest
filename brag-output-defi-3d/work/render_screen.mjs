// Renders the phone screen flat (1080x2337) as the texture for the 3D shots.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path'; import fs from 'node:fs';
const [t0, t1, outDir, fps = 30] = process.argv.slice(2);
const here = path.dirname(new URL(import.meta.url).pathname);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1080, height: 2337 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('PAGE ERROR', e.message));
await page.addInitScript(() => { window.SCREEN = true; });
await page.goto('file://' + path.join(here, 'screen.html'));
await page.addStyleTag({ content: 'html,body,#stage{width:1080px!important;height:2337px!important} #room,#vig,#grain,#rw,#end{display:none!important}' });
await page.evaluate(() => window.setup());
fs.mkdirSync(outDir, { recursive: true });
const n = Math.round((Number(t1) - Number(t0)) * fps);
for (let f = 0; f < n; f++) {
  await page.evaluate(t => window.render(t), Number(t0) + f / fps);
  await page.screenshot({ path: path.join(outDir, `s${String(f + 1).padStart(4, '0')}.png`), clip: { x: 0, y: 0, width: 1080, height: 2337 } });
}
await browser.close();
