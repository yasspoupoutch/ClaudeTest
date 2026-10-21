import React, { useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ThreeCanvas } from '@remotion/three';
import { staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { useThree } from '@react-three/fiber';
import { Text } from '@react-three/drei';
import { EXRLoader } from 'three/examples/jsm/loaders/EXRLoader.js';
import * as THREE from 'three';
import { Post } from './Post';
import {
  FPS, clamp, ease, hold, io, ioSoft, lerp, prog, roundedPlane, roundedRectCurve, roundedRectShape, spring, tex, track, trackN,
} from './kit';

// ---------------------------------------------------------------------------------------------
// Units: 1 = 10 cm. The phone lies on the table at the origin, screen up (+y), its top towards -z.
// Screen texture is 1179 x 2556 px (SwiftUI points x 3), mapped onto 0.68 x 1.4742.
// ---------------------------------------------------------------------------------------------
const PW = 0.716, PH = 1.508, PD = 0.0825;                  // phone body
const SW = 0.68, SH = (0.68 * 2556) / 1179;                 // screen
const TOP = PD + 0.002;                                      // screen surface height
const TX = 1179, TY = 2556;
/** Screen pixel -> point on the lying phone's screen, in phone space. */
const sp = (px: number, py: number, lift = 0) => new THREE.Vector3((px / TX - 0.5) * SW, TOP + lift, (py / TY - 0.5) * SH);

const GOLD = new THREE.Color(1.0, 0.776, 0.353);
/** Gold for 3D letters: more saturated, so it stays gold through AgX tone mapping. */
const GOLD_TEXT = new THREE.Color(1.0, 0.66, 0.16);
const T = (s: number) => s * FPS;                            // seconds -> frames

// ----------------------------------- timeline (seconds) -----------------------------------
const WORD = 'CHOUCROUTE';
const TYPE0 = 4.0, TSTEP = 0.2, VALID = 6.05;               // typing in the app
const LIFT = 6.3, VOWELS = 7.3, FLIP = 9.0, BACKDOWN = 10.3, RESULT = 10.75;
const MODES = 11.0, BOARD = 15.0, END = 17.0;
export const DURATION = T(20.5);

function screenTexture(t: number) {
  if (t >= BOARD) return t >= END + 0.6 ? 'game_result.png' : 'board.png';
  if (t >= RESULT) return 'game_result.png';
  if (t >= LIFT) return 'game_lifted.png';
  if (t >= VALID - 0.05) return t < VALID + 0.2 ? 'game_valid.png' : 'game_10.png';
  const n = WORD.split('').filter((_, i) => t >= TYPE0 + i * TSTEP).length;
  return `game_${String(n).padStart(2, '0')}.png`;
}

// ----------------------------------- glyph metrics -----------------------------------
// Letter advances of Instrument Serif, measured in the page once the font is loaded (fraction of font size).
const ADV: Record<string, number> = {};
let advReady = false;
function useAdvances() {
  const [, set] = useState(0);
  useLayoutEffect(() => {
    if (advReady) return;
    const done = hold('advances');
    const face = new FontFace('IS', `url(${staticFile('fonts/InstrumentSerif-Regular.ttf')})`);
    face.load().then((f) => {
      (document.fonts as any).add(f);
      const ctx = document.createElement('canvas').getContext('2d')!;
      ctx.font = '100px IS';
      for (const c of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') ADV[c] = ctx.measureText(c).width / 100;
      advReady = true; set(1); done();
    });
  }, []);
}
/** x of each letter's centre: vowels take p (0..1) of their width, so consonants close up when vowels are out. */
function layout(word: string, size: number, spacing: number, vowelP: (i: number) => number) {
  const isV = (c: string) => 'AEIOUY'.includes(c);
  let vi = 0;
  const widths = word.split('').map((c) => (ADV[c] ?? 0.6) * size * (isV(c) ? vowelP(vi++) : 1) + spacing * (isV(c) ? vowelP(vi - 1) : 1));
  const total = widths.reduce((a, b) => a + b, 0);
  let x = -total / 2;
  return widths.map((w) => { const c = x + w / 2; x += w; return c; });
}

// ----------------------------------- pieces -----------------------------------
const SyncText: React.FC<React.ComponentProps<typeof Text>> = (props) => {
  // Troika lays text out lazily on first draw; force it now so the frame never renders without glyphs.
  const ref = useRef<any>(null);
  const key = String(props.children) + String(props.font) + String(props.fontSize);
  useLayoutEffect(() => {
    const done = hold('text');
    let called = false;
    const finish = () => { if (!called) { called = true; done(); } };
    if (ref.current?.sync) ref.current.sync(finish); else finish();
    const timer = setTimeout(finish, 20000);
    return () => clearTimeout(timer);
  }, [key]);
  return <Text ref={ref} {...props} />;
};

const Phone: React.FC<{ screen: string; glow: number }> = ({ screen, glow }) => {
  const body = useMemo(() => {
    const g = new THREE.ExtrudeGeometry(roundedRectShape(PW - 0.024, PH - 0.024, 0.105), {
      depth: PD - 0.024, bevelEnabled: true, bevelThickness: 0.012, bevelSize: 0.012, bevelSegments: 6, curveSegments: 32,
    });
    g.translate(0, 0, 0.012); g.rotateX(-Math.PI / 2); g.translate(0, 0, 0); return g;
  }, []);
  const glass = useMemo(() => roundedPlane(PW - 0.02, PH - 0.02, 0.108), []);
  const scr = useMemo(() => roundedPlane(SW, SH, 0.092), []);
  const map = tex(screen);
  return (
    <group>
      <mesh geometry={body} castShadow receiveShadow>
        <meshPhysicalMaterial color="#45413c" metalness={1} roughness={0.28} clearcoat={0.4} envMapIntensity={1.1} />
      </mesh>
      <mesh geometry={glass} rotation-x={-Math.PI / 2} position-y={PD + 0.0005}>
        <meshPhysicalMaterial color="#030304" roughness={0.04} clearcoat={1} clearcoatRoughness={0.02} envMapIntensity={1.4} />
      </mesh>
      <mesh geometry={scr} rotation-x={-Math.PI / 2} position-y={TOP}>
        <meshBasicMaterial map={map} toneMapped={false} color={new THREE.Color(glow, glow, glow)} />
      </mesh>
      {/* glass reflection over the screen */}
      <mesh geometry={scr} rotation-x={-Math.PI / 2} position-y={TOP + 0.0008}>
        <meshPhysicalMaterial color="#000" transparent opacity={0.18} roughness={0.05} clearcoat={1} envMapIntensity={2.2} depthWrite={false} />
      </mesh>
    </group>
  );
};

/** Gold neon: a tube along a curve, drawn up to `p`, with a bright head that lights its surroundings. */
const Neon: React.FC<{ curve: THREE.Curve<THREE.Vector3>; p: number; fade?: number; radius?: number; light?: number; power?: number }> = ({ curve, p, fade = 1, radius = 0.006, light = 0.6, power = 4.5 }) => {
  const geo = useMemo(() => new THREE.TubeGeometry(curve, 400, radius, 10, false), [curve, radius]);
  const count = geo.index!.count;
  geo.setDrawRange(0, Math.floor((count * clamp(p)) / 60) * 60);
  const head = curve.getPointAt(clamp(p, 0.0001, 1));
  const on = p > 0.001 && fade > 0.01;
  return (
    <group visible={on}>
      <mesh geometry={geo}>
        <meshBasicMaterial color={GOLD.clone().multiplyScalar(power * fade)} toneMapped={false} />
      </mesh>
      <mesh position={head} visible={p < 1}>
        <sphereGeometry args={[radius * 2.6, 16, 16]} />
        <meshBasicMaterial color={new THREE.Color(9, 7, 3.5).multiplyScalar(fade)} toneMapped={false} />
      </mesh>
      <pointLight position={head} color="#ffc65a" intensity={light * fade * (p < 1 ? 1 : 0.3)} distance={1.2} decay={2} />
    </group>
  );
};

/** The word card (ShareCard) that comes out of the screen: CHCRT, vowels flying in, flip to the result. */
const WordCard: React.FC<{ t: number }> = ({ t }) => {
  const CW = 0.64, CH = 0.48;
  const front = tex('card_front.png'), back = tex('card_back.png');
  const face = useMemo(() => roundedPlane(CW, CH, 0.048), []);
  const slab = useMemo(() => {
    const g = new THREE.ExtrudeGeometry(roundedRectShape(CW, CH, 0.048), { depth: 0.016, bevelEnabled: false, curveSegments: 24 });
    g.translate(0, 0, -0.008); return g;
  }, []);
  const edge = useMemo(() => roundedRectCurve(CW - 0.006, CH - 0.006, 0.045, 0.0095), []);
  // Out of the screen and back
  const up = ease(prog(t, LIFT, LIFT + 1.0)), down = io(prog(t, BACKDOWN, RESULT));
  const k = up * (1 - down);
  const start = sp(590, 600, 0.004);
  const pos = start.clone().lerp(new THREE.Vector3(0, 0.78, -0.18), k);
  pos.y += Math.sin(t * 2.1) * 0.012 * k;                                  // gentle float
  const flip = io(prog(t, FLIP, FLIP + 0.55)) * Math.PI * (1 - io(prog(t, BACKDOWN, BACKDOWN + 0.35)));
  const rotX = lerp(-Math.PI / 2, -0.12, k), rotY = flip + Math.sin(t * 1.3) * 0.05 * k;
  const scale = lerp(0.75, 1, k);
  const visible = t >= LIFT && t < RESULT + 0.02;
  // Letters: consonants close up until the vowels arrive one by one
  const vp = (i: number) => spring(t - (VOWELS + i * 0.26), 0.42, 0.62);
  const size = 0.092, spacing = 0.004;
  const xs = layout(WORD, size, spacing, vp);
  const glowPulse = ease(prog(t, VOWELS + 1.35, VOWELS + 1.6)) * (1 - prog(t, VOWELS + 1.6, FLIP));
  let vi = 0;
  return (
    <group position={pos} rotation={[rotX, rotY, 0]} scale={scale} visible={visible}>
      <mesh geometry={slab} castShadow><meshPhysicalMaterial color="#0a0b12" roughness={0.35} clearcoat={0.6} /></mesh>
      <mesh geometry={face} position-z={0.0085}><meshBasicMaterial map={front} toneMapped={false} transparent /></mesh>
      <mesh geometry={face} position-z={-0.0085} rotation-y={Math.PI}><meshBasicMaterial map={back} toneMapped={false} transparent /></mesh>
      <Neon curve={edge} p={1} fade={0.3 + 0.7 * up + glowPulse} radius={0.0016} light={0.2} power={2.2} />
      {WORD.split('').map((c, i) => {
        const vowel = 'AEIOUY'.includes(c);
        const p = vowel ? vp(vi++) : 1;
        // a vowel flies in from below-front along an arc, then settles into its slot
        const from = new THREE.Vector3(xs[i] * 0.4 + (i % 2 ? 0.25 : -0.25), -0.55, 0.35);
        const at = new THREE.Vector3(xs[i], 0.0, 0.012);
        const q = clamp(p);
        const fly = vowel ? from.clone().lerp(at, ease(q)).add(new THREE.Vector3(0, Math.sin(q * Math.PI) * 0.12, 0)) : at;
        return (
          <SyncText key={i} font={staticFile('fonts/InstrumentSerif-Regular.ttf')} fontSize={size} anchorX="center" anchorY="middle"
            position={fly} scale={vowel ? lerp(0.4, 1, q) : 1} visible={!vowel || t >= VOWELS + (vi - 1) * 0.26 - 0.05}>
            {c}
            <meshBasicMaterial color={vowel ? GOLD_TEXT.clone().multiplyScalar(1.0 + 0.3 * glowPulse) : new THREE.Color(1.0, 1.0, 1.02)} toneMapped={false} />
          </SyncText>
        );
      })}
    </group>
  );
};

/** A mode card rising from the screen to its spot in the air. */
const ModeCard: React.FC<{ t: number; t0: number; name: string; spot: THREE.Vector3; turn: number }> = ({ t, t0, name, spot, turn }) => {
  const map = tex(name);
  const face = useMemo(() => roundedPlane(0.46, 0.575, 0.048), []);
  const slab = useMemo(() => { const g = new THREE.ExtrudeGeometry(roundedRectShape(0.46, 0.575, 0.048), { depth: 0.014, bevelEnabled: false, curveSegments: 24 }); g.translate(0, 0, -0.007); return g; }, []);
  const edge = useMemo(() => roundedRectCurve(0.454, 0.569, 0.045, 0.0085), []);
  const k = ease(prog(t, t0, t0 + 0.8));
  const away = io(prog(t, BOARD - 0.5, BOARD + 0.1));
  const pos = sp(590, 1300, 0.004).lerp(spot, k).add(new THREE.Vector3(0, away * 1.6, 0));
  pos.y += Math.sin(t * 2 + t0) * 0.01 * k;
  return (
    <group position={pos} rotation={[lerp(-Math.PI / 2, -0.08, k), turn * k, 0]} scale={lerp(0.5, 1, k)} visible={t >= t0 && away < 1}>
      <mesh geometry={slab} castShadow><meshPhysicalMaterial color="#0a0b12" roughness={0.35} clearcoat={0.6} /></mesh>
      <mesh geometry={face} position-z={0.0075}><meshBasicMaterial map={map} toneMapped={false} transparent /></mesh>
      <Neon curve={edge} p={1} fade={0.35 + 0.65 * k} radius={0.0014} light={0.1} power={2.0} />
    </group>
  );
};

/** End: CNSNN in Fraunces, the gold vowels drop in to make CONSONNE. */
const Logo: React.FC<{ t: number }> = ({ t }) => {
  const size = 0.2, word = 'CONSONNE';
  const vp = (i: number) => spring(t - (END + 1.75 + i * 0.16), 0.42, 0.62);
  // Fraunces Black is wider than Instrument Serif: scale the advances
  const xs = layout(word, size * 1.18, 0.01, vp);
  const sweep = io(prog(t, END + 0.9, END + 1.5));
  const tag = ease(prog(t, END + 2.5, END + 2.9));
  let vi = 0;
  return (
    <group position={[0, 2.22, -0.62]} visible={t >= END + 0.85}>
      {word.split('').map((c, i) => {
        const vowel = 'AEIOU'.includes(c); const p = vowel ? vp(vi++) : 1;
        const shown = vowel ? clamp(p) : clamp((sweep - (xs[i] + 0.9) / 1.8) * 6 + 0.5);
        return (
          <SyncText key={i} font={staticFile('fonts/Fraunces-Black.ttf')} fontSize={size} anchorX="center" anchorY="middle"
            position={[xs[i], vowel ? (1 - clamp(p)) * 0.25 : 0, 0]} scale={vowel ? lerp(0.6, 1, clamp(p)) : 1} fillOpacity={shown} visible={shown > 0.01}>
            {c}
            <meshBasicMaterial color={vowel ? GOLD_TEXT.clone() : new THREE.Color(0.96, 0.96, 0.98)} toneMapped={false} transparent opacity={shown} />
          </SyncText>
        );
      })}
      <SyncText font={staticFile('fonts/InstrumentSerif-Italic.ttf')} fontSize={0.09} anchorX="center" anchorY="middle" position={[0, -0.2, 0]} fillOpacity={tag}>
        Le mot du jour. Sans ses voyelles.
        <meshBasicMaterial color={new THREE.Color(0.95, 0.95, 0.97)} toneMapped={false} transparent opacity={tag} />
      </SyncText>
      <SyncText font={staticFile('fonts/Fraunces-Black.ttf')} fontSize={0.05} letterSpacing={0.12} anchorX="center" anchorY="middle" position={[0, -0.33, 0]} fillOpacity={tag}>
        GRATUIT · SANS PUBLICITÉ
        <meshBasicMaterial color={GOLD.clone().multiplyScalar(1.0)} toneMapped={false} transparent opacity={tag} />
      </SyncText>
    </group>
  );
};

const Backdrop: React.FC = () => {
  const map = useMemo(() => {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d')!;
    const bg = g.createLinearGradient(0, 0, 0, 512); bg.addColorStop(0, '#120a06'); bg.addColorStop(1, '#2a170c'); g.fillStyle = bg; g.fillRect(0, 0, 1024, 512);
    for (const [x, y, r, a] of [[260, 300, 260, 0.55], [800, 330, 180, 0.3], [560, 420, 120, 0.25]] as number[][]) {
      const rg = g.createRadialGradient(x, y, 0, x, y, r); rg.addColorStop(0, `rgba(255,170,90,${a})`); rg.addColorStop(1, 'rgba(255,170,90,0)');
      g.fillStyle = rg; g.fillRect(0, 0, 1024, 512);
    }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }, []);
  return (
    <mesh position={[0, 2.2, -7]}>
      <planeGeometry args={[18, 9]} />
      <meshBasicMaterial map={map} toneMapped={false} />
    </mesh>
  );
};

const Table: React.FC = () => {
  const map = tex('wood.jpg'), rough = tex('wood_rough.jpg', false);
  for (const m of [map, rough]) { m.wrapS = m.wrapT = THREE.RepeatWrapping; m.repeat.set(3, 3); }
  return (
    <mesh rotation-x={-Math.PI / 2} receiveShadow>
      <planeGeometry args={[40, 40]} />
      <meshStandardMaterial map={map} roughnessMap={rough} roughness={1} envMapIntensity={0.6} />
    </mesh>
  );
};

/** Soft contact shadow under the lying phone, so it sits on the wood. */
const Contact: React.FC<{ opacity: number }> = ({ opacity }) => {
  const map = useMemo(() => {
    const c = document.createElement('canvas'); c.width = 256; c.height = 512;
    const g = c.getContext('2d')!; g.filter = 'blur(18px)'; g.fillStyle = '#000';
    g.beginPath(); (g as any).roundRect(40, 40, 176, 432, 30); g.fill();
    const t = new THREE.CanvasTexture(c); return t;
  }, []);
  return (
    <mesh rotation-x={-Math.PI / 2} position-y={0.001}>
      <planeGeometry args={[PW * 1.35, PH * 1.18]} />
      <meshBasicMaterial map={map} transparent opacity={0.75 * opacity} depthWrite={false} />
    </mesh>
  );
};

// ----------------------------------- camera direction -----------------------------------
// Each key: [seconds, camera position, look-at]. Positions are in world space (phone at the origin).
const CAM: [number, number[], number[]][] = [
  [0.0, [-0.36, 0.86, 0.72], [-0.03, 0.08, -0.42]],
  [1.9, [0.12, 0.72, 0.62], [0.02, 0.08, -0.4]],
  [3.7, [0.22, 0.55, 0.7], [0.0, 0.08, 0.02]],
  [4.6, [-0.12, 0.38, 0.95], [0.0, 0.08, 0.26]],
  [6.1, [0.1, 0.42, 0.95], [0.0, 0.08, 0.12]],
  [7.0, [0.55, 1.1, 2.15], [0.0, 0.78, -0.18]],
  [8.8, [0.18, 0.95, 2.0], [0.0, 0.78, -0.18]],
  [9.7, [0.06, 0.88, 1.8], [0.0, 0.78, -0.18]],
  [10.3, [0.03, 0.95, 1.85], [0.0, 0.66, -0.2]],
  [10.95, [0.0, 1.45, 1.75], [0.0, 0.25, -0.1]],
  [11.7, [-0.72, 1.0, 1.75], [-0.56, 0.72, -0.25]],
  [13.0, [0.0, 1.0, 1.8], [0.0, 0.72, -0.28]],
  [14.3, [0.62, 1.0, 1.8], [0.5, 0.72, -0.25]],
  [15.3, [0.05, 1.25, 0.85], [0.0, 0.09, -0.25]],
  [16.8, [0.1, 0.9, 0.6], [0.0, 0.09, -0.33]],
  [17.6, [0.0, 1.3, 3.9], [0.0, 1.28, -0.5]],
  [20.5, [0.0, 1.3, 3.55], [0.0, 1.3, -0.5]],
];
// Focus point for the depth of field
const FOCUS: [number, number[]][] = [
  [0.0, [0.0, 0.09, -0.41]], [1.9, [0.0, 0.09, -0.41]], [3.7, [0.0, 0.09, 0.0]], [4.6, [0.0, 0.09, 0.3]], [6.1, [0.0, 0.09, 0.05]],
  [6.55, [0.0, 0.7, -0.15]], [7.0, [0.0, 0.76, -0.18]], [10.3, [0.0, 0.76, -0.18]], [10.6, [0.0, 0.09, 0.1]],
  [11.7, [-0.56, 0.72, -0.25]], [13.0, [0.0, 0.72, -0.28]], [14.3, [0.5, 0.72, -0.25]],
  [15.3, [0.0, 0.09, -0.25]], [16.8, [0.0, 0.09, -0.33]], [17.6, [0.0, 1.0, -0.45]], [20.5, [0.0, 1.05, -0.5]],
];

const Rig: React.FC<{ t: number }> = ({ t }) => {
  const { camera } = useThree();
  useLayoutEffect(() => {
    const p = track(CAM.map(([s, a]) => [s, a]), t, ioSoft), l = track(CAM.map(([s, , b]) => [s, b]), t, ioSoft);
    camera.position.copy(p); camera.lookAt(l);
    camera.updateMatrixWorld();
  }, [t, camera]);
  return null;
};

/** Indoor HDRI for reflections on the metal frame and the glass (loaded once, waited for). */
const useRoomEnvironment = () => {
  const { scene } = useThree();
  useLayoutEffect(() => {
    if (scene.environment) return;
    const done = hold('env');
    new EXRLoader().load(staticFile('room.exr'), (t) => {
      t.mapping = THREE.EquirectangularReflectionMapping; scene.environment = t; (scene as any).environmentIntensity = 0.45; done();
    }, undefined, () => done());
  }, [scene]);
};

const Scene: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  useAdvances();
  useRoomEnvironment();
  // Neon paths
  const underline = useMemo(() => new THREE.CatmullRomCurve3([
    sp(-60, 760, 0.006), sp(260, 760, 0.006), sp(590, 770, 0.006), sp(930, 760, 0.006), sp(1120, 820, 0.01),
    sp(1000, 1060, 0.012), sp(700, 1130, 0.008), sp(420, 1300, 0.006), sp(120, 1330, 0.006),
  ]), []);
  const boardLoop = useMemo(() => {
    const c = roundedRectCurve(0.62, 0.105, 0.05, 0);
    const pts = c.getSpacedPoints(160).map((v) => new THREE.Vector3(v.x, TOP + 0.006, -v.y + sp(0, 700).z));
    return new THREE.CatmullRomCurve3(pts, true);
  }, []);
  // Phone stands up at the end, pivoting on its bottom edge
  const stand = io(prog(t, END, END + 0.9));
  const phonePos = new THREE.Vector3(0, lerp(0, PH / 2 - 0.05, stand), lerp(0, -0.2, stand));
  const phoneRot = lerp(0, Math.PI / 2 - 0.12, stand);
  const focus = track(FOCUS, t, ioSoft);
  const bokeh = trackN([[0, 5], [6.2, 4.5], [7, 6], [10.5, 4], [15, 4.5], [17.0, 3], [17.6, 1.2], [20.5, 1.2]], t);
  const flash = Math.exp(-Math.pow((t - (VOWELS + 1.45)) / 0.18, 2));
  return (
    <>
      <color attach="background" args={['#0b0705']} />
      <ambientLight intensity={0.05} />
      {/* warm key light, like a desk lamp off to the left */}
      <spotLight position={[-2.6, 3.4, -1.2]} angle={0.45} penumbra={0.9} intensity={170} color="#ffb877" castShadow
        shadow-mapSize-width={2048} shadow-mapSize-height={2048} shadow-bias={-0.0004} shadow-radius={6} target-position={[0, 0, 0]} />
      <pointLight position={[1.8, 1.4, 1.6]} intensity={5} color="#8fb2ff" />
      <Backdrop />
      <Table />
      <Contact opacity={1 - stand} />
      <group position={phonePos} rotation-x={phoneRot}>
        <Phone screen={screenTexture(t)} glow={1.0 + 0.25 * flash} />
        <Neon curve={underline} p={io(prog(t, 2.0, 3.7))} fade={1 - prog(t, 3.9, 4.4)} />
        <Neon curve={boardLoop} p={io(prog(t, 15.5, 16.4))} fade={1 - prog(t, 16.9, 17.2)} radius={0.0022} power={2.0} light={0.2} />
      </group>
      <WordCard t={t} />
      <ModeCard t={t} t0={MODES} name="mode_sprint.png" spot={new THREE.Vector3(-0.56, 0.72, -0.25)} turn={0.3} />
      <ModeCard t={t} t0={MODES + 1.2} name="mode_survie.png" spot={new THREE.Vector3(0, 0.72, -0.28)} turn={0} />
      <ModeCard t={t} t0={MODES + 2.4} name="mode_double.png" spot={new THREE.Vector3(0.5, 0.72, -0.25)} turn={-0.3} />
      <Logo t={t} />
      <Rig t={t} />
      <Post focus={focus} bokeh={bokeh} bloom={0.9 + 0.8 * flash} />
    </>
  );
};

export const Promo: React.FC = () => {
  const { width, height } = useVideoConfig();
  return (
    <ThreeCanvas width={width} height={height} linear={false} flat={false} gl={{ antialias: false, preserveDrawingBuffer: true }} shadows
      camera={{ fov: 34, near: 0.02, far: 40, position: [0, 1, 1] }}>
      <Scene />
    </ThreeCanvas>
  );
};
