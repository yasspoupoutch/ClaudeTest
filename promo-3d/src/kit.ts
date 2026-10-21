import * as THREE from 'three';
import { continueRender, delayRender, staticFile } from 'remotion';

// ---------- timing ----------
export const FPS = 30;
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;
export const prog = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
export function bezier(x1: number, y1: number, x2: number, y2: number) {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = (u: number) => ((ax * u + bx) * u + cx) * u, sy = (u: number) => ((ay * u + by) * u + cy) * u;
  return (x: number) => {
    if (x <= 0) return 0; if (x >= 1) return 1; let u = x;
    for (let i = 0; i < 8; i++) { const d = (3 * ax * u + 2 * bx) * u + cx; if (Math.abs(d) < 1e-6) break; u -= (sx(u) - x) / d; }
    return sy(clamp(u));
  };
}
export const ease = bezier(0.2, 0.9, 0.25, 1);       // CNSNN's own ease curve
export const io = bezier(0.65, 0, 0.35, 1);
export const ioSoft = bezier(0.45, 0, 0.25, 1);
/** Camera curves: 'snap' = fast in the middle with hard stops (speed ramp), 'glide' = slow drift. */
export const CURVES = { snap: bezier(0.8, 0, 0.12, 1), glide: bezier(0.35, 0.1, 0.65, 0.9), soft: ioSoft };
export type CurveName = keyof typeof CURVES;
export function spring(t: number, response = 0.42, damping = 0.62) {
  if (t <= 0) return 0;
  const w = (2 * Math.PI) / response, wd = w * Math.sqrt(1 - damping * damping);
  return 1 - Math.exp(-damping * w * t) * (Math.cos(wd * t) + ((damping * w) / wd) * Math.sin(wd * t));
}
const V = (a: number[]) => new THREE.Vector3(a[0], a[1], a[2]);
/** Keyframed vector track with eased segments: [[time, [x,y,z]], ...] */
export function track(keys: [number, number[]][], t: number, curve = io): THREE.Vector3 {
  if (t <= keys[0][0]) return V(keys[0][1]);
  for (let i = 0; i < keys.length - 1; i++) {
    const [ta, a] = keys[i], [tb, b] = keys[i + 1];
    if (t <= tb) return V(a).lerp(V(b), curve(prog(t, ta, tb)));
  }
  return V(keys[keys.length - 1][1]);
}
/** Like track(), each key naming the curve of the segment that ends on it: [time, value, curve?] */
export function trackC(keys: [number, number[], CurveName?][], t: number): THREE.Vector3 {
  if (t <= keys[0][0]) return V(keys[0][1]);
  for (let i = 0; i < keys.length - 1; i++) {
    const [ta, a] = keys[i], [tb, b, c] = keys[i + 1];
    if (t <= tb) return V(a).lerp(V(b), CURVES[c ?? 'soft'](prog(t, ta, tb)));
  }
  return V(keys[keys.length - 1][1]);
}
export function trackN(keys: [number, number][], t: number, curve = io): number {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [ta, a] = keys[i], [tb, b] = keys[i + 1];
    if (t <= tb) return lerp(a, b, curve(prog(t, ta, tb)));
  }
  return keys[keys.length - 1][1];
}

// ---------- assets, loaded once with delayRender so no frame renders before they are ready ----------
const texCache = new Map<string, THREE.Texture>();
let pending = 0;
export const isReady = () => pending === 0;
export function hold(label: string) {
  pending++; const h = delayRender(label);
  return () => { pending--; continueRender(h); };
}
export function tex(name: string, srgb = true): THREE.Texture {
  const hit = texCache.get(name); if (hit) return hit;
  const done = hold('tex ' + name);
  const t = new THREE.TextureLoader().load(staticFile('tex/' + name), () => done(), undefined, () => done());
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 16; t.generateMipmaps = true; t.minFilter = THREE.LinearMipmapLinearFilter;
  texCache.set(name, t); return t;
}

// ---------- geometry ----------
export function roundedRectShape(w: number, h: number, r: number) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}
/** Flat rounded rectangle with 0..1 UVs across its bounds. */
export function roundedPlane(w: number, h: number, r: number, seg = 24) {
  const g = new THREE.ShapeGeometry(roundedRectShape(w, h, r), seg);
  const p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5);
  return g;
}
/** Closed path around a rounded rectangle, for neon outlines. */
export function roundedRectCurve(w: number, h: number, r: number, z = 0) {
  const pts = roundedRectShape(w, h, r).getSpacedPoints(160).map((p) => new THREE.Vector3(p.x, p.y, z));
  return new THREE.CatmullRomCurve3(pts, true);
}
