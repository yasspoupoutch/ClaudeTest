# Procedural dark walnut table top: planks with long grain, pores and slight colour variation.
import numpy as np, sys
from PIL import Image
rng = np.random.default_rng(3)
W, H = 2048, 2048
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
def noise(scale, octaves=4):
    out = np.zeros((H, W), np.float32); amp = 1.0
    for o in range(octaves):
        s = scale * 2 ** o
        g = rng.standard_normal((int(H / s) + 3, int(W / s) + 3)).astype(np.float32)
        img = Image.fromarray(g).resize((W + int(2 * s), H + int(2 * s)), Image.BICUBIC)
        out += amp * np.asarray(img)[:H, :W]; amp *= 0.5
    return out / out.std()
plank_w = 340
plank = (x // plank_w).astype(int)
tone = rng.uniform(-0.08, 0.08, plank.max() + 2)[plank]
warp = noise(220, 3) * 18
grain = np.sin((x + warp + noise(60, 2) * 4) * 0.09 + plank * 7.0) * 0.5 + 0.5           # long fibres along y
rings = np.sin((x + warp * 2.2) * 0.022 + noise(400, 2) * 1.2 + plank * 3.0) * 0.5 + 0.5    # broad figure
pores = np.clip(noise(3, 1), 1.8, 4) - 1.8
seams = np.minimum(1, np.abs((x % plank_w) - plank_w / 2) / (plank_w / 2))
seam = np.where(np.abs(x % plank_w) < 3, 0.55, 1.0)
base = np.array([0.20, 0.115, 0.06]); dark = np.array([0.09, 0.05, 0.026])
t = np.clip(0.55 * rings + 0.3 * grain + 0.15 * noise(30, 2) * 0.3 + tone[..., None][..., 0] * 2, 0, 1)
col = dark[None, None] + (base - dark)[None, None] * t[..., None]
col *= (1 - 0.35 * pores)[..., None] * seam[..., None]
col = np.clip(col ** (1 / 2.2), 0, 1)
Image.fromarray((col * 255).astype(np.uint8)).save(sys.argv[1], optimize=True)
rough = np.clip(0.42 + 0.18 * grain + 0.25 * pores + 0.1 * (1 - seam), 0, 1)
Image.fromarray((rough * 255).astype(np.uint8)).save(sys.argv[2], optimize=True)
print('ok')
