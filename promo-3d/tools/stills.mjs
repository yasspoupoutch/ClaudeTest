// Renders stills at the given seconds in one browser session: node tools/stills.mjs 1 3.5 7 ...
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import path from 'node:path';
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const serveUrl = await bundle({ entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public') });
const opts = { browserExecutable: '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell', chromiumOptions: { gl: 'swangle' }, timeoutInMilliseconds: 120000 };
const composition = await selectComposition({ serveUrl, id: 'Promo', ...opts });
for (const s of process.argv.slice(2)) {
  const t0 = Date.now();
  await renderStill({ serveUrl, composition, frame: Math.round(Number(s) * 30), output: path.join(root, `out/s_${s}.png`), ...opts });
  console.log(s, ((Date.now() - t0) / 1000).toFixed(1) + 's');
}
