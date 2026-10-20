"""CNSNN video 2, 3D shots: a phone lying on a bed at night, its screen playing a frame sequence.
Usage: python shot.py -- <shot> <screen_dir> <hdr> <out_dir>   (ONLY=1,60 renders single test frames)"""
import bpy, bmesh, math, sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
shot, screen_dir, hdr, out_dir = argv[:4]

# Per shot: lens, f-stop and keys {frame: (camera, look-at, focus)} in phone space (x right, y towards the top, z out of the screen),
# except 'open' which is in room space. Units: metres.
SHOTS = {
    'open':    dict(lens=35, fstop=2.8, world=True, keys={
        1: ((0.62, -1.15, 0.62), (0.0, 0.05, 0.0), (0.0, 0.0, 0.0)),
        60: ((0.36, -0.70, 0.40), (0.0, 0.02, 0.0), (0.0, 0.0, 0.0))}),
    'chat':    dict(lens=50, fstop=4.5, keys={
        1: ((-0.060, -0.175, 0.150), (-0.004, -0.018, 0.0), (0.0, -0.02, 0.07)),
        30: ((-0.048, -0.173, 0.148), (-0.003, -0.021, 0.0), (0.0, -0.022, 0.0)),
        144: ((-0.008, -0.165, 0.140), (0.0, -0.030, 0.0), (0.0, -0.033, 0.0))}),
    'type':    dict(lens=50, fstop=4.0, keys={
        1: ((-0.030, -0.128, 0.088), (-0.004, -0.024, 0.0), (-0.004, -0.022, 0.0)),
        117: ((0.012, -0.122, 0.082), (0.004, -0.024, 0.0), (0.004, -0.020, 0.0))}),
    'mock':    dict(lens=50, fstop=4.5, keys={
        1: ((0.062, -0.150, 0.150), (0.0, 0.010, 0.0), (0.0, 0.010, 0.0)),
        96: ((0.040, -0.136, 0.136), (0.0, 0.006, 0.0), (0.0, 0.004, 0.0))}),
    'app':     dict(lens=50, fstop=4.5, keys={
        1: ((-0.016, -0.128, 0.112), (0.0, -0.008, 0.0), (0.0, -0.006, 0.0)),
        70: ((-0.008, -0.126, 0.110), (0.0, -0.010, 0.0), (0.0, -0.008, 0.0)),
        105: ((0.006, -0.195, 0.185), (0.0, -0.028, 0.0), (0.0, -0.028, 0.0)),
        165: ((0.014, -0.188, 0.178), (0.0, -0.030, 0.0), (0.0, -0.030, 0.0))}),
    'revenge': dict(lens=50, fstop=4.5, keys={
        1: ((0.060, -0.190, 0.160), (0.0, -0.028, 0.0), (0.0, -0.022, 0.0)),
        180: ((-0.010, -0.172, 0.145), (0.0, -0.040, 0.0), (0.0, -0.045, 0.0))}),
}
cfg = SHOTS[shot]
pngs = sorted(f for f in os.listdir(screen_dir) if f.endswith('.png'))
nframes = len(pngs)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 12; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.render.use_persistent_data = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 67
sc.render.fps = 30; sc.frame_start, sc.frame_end = 1, nframes
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.4
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = os.path.join(out_dir, shot + '_')

def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m, b
def box(name, size, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new('bv', 'BEVEL'); bv.width = 0.01; bv.segments = 3
    o.data.materials.append(mat); return o

# World: dim indoor HDRI for reflections
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdr)
nt.nodes['Background'].inputs[1].default_value = 0.05; nt.links.new(env.outputs[0], nt.nodes['Background'].inputs[0])

# --- Bedroom. The phone lies at the origin; the bed is centred to its right. ---
BX, BY = 0.42, 0.18            # bed centre
fabric, fb = principled('duvet', **{'Base Color': (0.5, 0.42, 0.36, 1), 'Roughness': 0.92})
fb.inputs['Sheen Weight'].default_value = 0.8; fb.inputs['Sheen Roughness'].default_value = 0.4
n = fabric.node_tree.nodes; weave = n.new('ShaderNodeTexNoise'); weave.inputs['Scale'].default_value = 900
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.15
fabric.node_tree.links.new(weave.outputs[0], bump.inputs['Height']); fabric.node_tree.links.new(bump.outputs[0], fb.inputs['Normal'])
bpy.ops.mesh.primitive_plane_add(size=1, location=(BX, BY, -0.006)); duvet = bpy.context.object
duvet.scale = (1.75, 2.15, 1); bpy.ops.object.transform_apply(scale=True)
sub = duvet.modifiers.new('s', 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = sub.render_levels = 7
big = bpy.data.textures.new('folds', 'CLOUDS'); big.noise_scale = 0.32; big.noise_depth = 1
d1 = duvet.modifiers.new('d1', 'DISPLACE'); d1.texture = big; d1.strength = 0.05; d1.mid_level = 0.5
small = bpy.data.textures.new('creases', 'CLOUDS'); small.noise_scale = 0.07; small.noise_depth = 1
d2 = duvet.modifiers.new('d2', 'DISPLACE'); d2.texture = small; d2.strength = 0.012; d2.mid_level = 0.5
duvet.data.materials.append(fabric); bpy.ops.object.shade_smooth()
sheet, _ = principled('sheet', **{'Base Color': (0.55, 0.5, 0.45, 1), 'Roughness': 0.9})
box('mattress', (1.8, 2.2, 0.26), (BX, BY, -0.15), sheet)
wood, _ = principled('wood', **{'Base Color': (0.16, 0.09, 0.05, 1), 'Roughness': 0.45})
box('headboard', (1.9, 0.08, 0.95), (BX, BY + 1.16, 0.1), wood)
for px in (BX - 0.42, BX + 0.42):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(px, BY + 0.9, 0.06)); p = bpy.context.object
    p.scale = (0.34, 0.2, 0.09); p.data.materials.append(sheet); bpy.ops.object.shade_smooth()
box('nightstand', (0.45, 0.4, 0.5), (BX - 1.2, BY + 0.95, -0.25), wood)
wallm, _ = principled('wall', **{'Base Color': (0.32, 0.26, 0.22, 1), 'Roughness': 0.85})
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, BY + 1.22, 1.0), rotation=(math.radians(90), 0, 0)); bpy.context.object.data.materials.append(wallm)
floorm, _ = principled('floor', **{'Base Color': (0.12, 0.08, 0.06, 1), 'Roughness': 0.5})
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.5)); bpy.context.object.data.materials.append(floorm)
# Bedside lamp: base + glowing shade + its light
brass, _ = principled('brass', **{'Base Color': (0.6, 0.45, 0.25, 1), 'Metallic': 1, 'Roughness': 0.3})
bpy.ops.mesh.primitive_cylinder_add(radius=0.015, depth=0.22, location=(BX - 1.2, BY + 0.98, 0.11)); bpy.context.object.data.materials.append(brass)
bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.09, depth=0.19, location=(BX - 1.2, BY + 0.98, 0.3), end_fill_type='NOTHING'); shade = bpy.context.object
ms, sb = principled('shade', **{'Base Color': (1, 0.85, 0.65, 1), 'Roughness': 0.8})
sb.inputs['Emission Color'].default_value = (1, 0.55, 0.25, 1); sb.inputs['Emission Strength'].default_value = 2.2
sb.inputs['Transmission Weight'].default_value = 0.5; shade.data.materials.append(ms)
bpy.ops.object.light_add(type='POINT', location=(BX - 1.2, BY + 0.98, 0.28)); L = bpy.context.object
L.data.energy = 120; L.data.color = (1, 0.56, 0.28); L.data.shadow_soft_size = 0.06
# Warm bounce near the phone so the close-ups keep the grazing lamp light on the folds
bpy.ops.object.light_add(type='POINT', location=(-0.55, 0.55, 0.22)); K = bpy.context.object
K.data.energy = 30; K.data.color = (1, 0.58, 0.3); K.data.shadow_soft_size = 0.15
bpy.ops.object.light_add(type='AREA', location=(0.9, -0.4, 0.8)); F = bpy.context.object
F.data.energy = 2.5; F.data.color = (0.75, 0.82, 1); F.data.size = 1.0; F.rotation_euler = (math.radians(55), 0, math.radians(60))

# --- Phone: 71.6 x 150.8 x 8.25 mm, titanium frame, rounded corners ---
W, H, D = 0.0716, 0.1508, 0.00825
bpy.ops.mesh.primitive_cube_add(size=1); ph = bpy.context.object
ph.scale = (W, H, D); bpy.ops.object.transform_apply(scale=True)
bm = bmesh.new(); bm.from_mesh(ph.data)
vert = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > D * 0.5]
bmesh.ops.bevel(bm, geom=vert, offset=0.0115, segments=18, affect='EDGES', profile=0.5)
bm.to_mesh(ph.data); bm.free()
bv = ph.modifiers.new('bv', 'BEVEL'); bv.width = 0.0028; bv.segments = 6; bv.limit_method = 'ANGLE'
mt, _ = principled('titanium', **{'Base Color': (0.2, 0.19, 0.18, 1), 'Metallic': 1.0, 'Roughness': 0.3})
ph.data.materials.append(mt); bpy.ops.object.shade_smooth()
ph.location = (0, 0, D / 2)
def rounded_plane(w, h, r, z, name):
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.name = name
    o.scale = (w, h, 1); bpy.ops.object.transform_apply(scale=True)
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.bevel(bm, geom=list(bm.verts), offset=r, segments=18, affect='VERTICES', profile=0.5)
    bm.to_mesh(o.data); bm.free()
    uvl = o.data.uv_layers.new()
    for poly in o.data.polygons:
        for li in poly.loop_indices:
            co = o.data.vertices[o.data.loops[li].vertex_index].co
            uvl.data[li].uv = (co.x / w + 0.5, co.y / h + 0.5)
    o.location.z = z; return o
glass = rounded_plane(W - 0.0016, H - 0.0016, 0.0108, D + 0.00005, 'glass')
mg, gb = principled('bezel', **{'Base Color': (0.004, 0.004, 0.005, 1), 'Roughness': 0.03})
gb.inputs['Coat Weight'].default_value = 1; gb.inputs['Coat Roughness'].default_value = 0.02
glass.data.materials.append(mg)
SW, SH = 0.0680, 0.0680 * 2337 / 1080
scr = rounded_plane(SW, SH, 0.0095, D + 0.0001, 'screen')
m = bpy.data.materials.new('screen'); m.use_nodes = True; nn = m.node_tree.nodes; sbsdf = nn['Principled BSDF']
img = nn.new('ShaderNodeTexImage')
img.image = bpy.data.images.load(os.path.join(screen_dir, pngs[0])); img.image.source = 'SEQUENCE'
img.image_user.frame_duration = nframes; img.image_user.frame_start = 1; img.image_user.use_auto_refresh = True
sbsdf.inputs['Base Color'].default_value = (0, 0, 0, 1); sbsdf.inputs['Roughness'].default_value = 0.03
sbsdf.inputs['Coat Weight'].default_value = 1; sbsdf.inputs['Coat Roughness'].default_value = 0.02
m.node_tree.links.new(img.outputs[0], sbsdf.inputs['Emission Color']); sbsdf.inputs['Emission Strength'].default_value = 1.7
scr.data.materials.append(m)
rig = bpy.data.objects.new('rig', None); sc.collection.objects.link(rig)
rig.rotation_euler = (0, 0, math.radians(-8)); rig.location = (0, 0, 0.002)
for o in (ph, glass, scr): o.parent = rig

# --- Camera, look-at and focus targets (phone space unless the shot is in room space) ---
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = cfg['lens']; cam.data.sensor_width = 36
cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = cfg['fstop']
look = bpy.data.objects.new('look', None); sc.collection.objects.link(look)
focus = bpy.data.objects.new('focus', None); sc.collection.objects.link(focus)
if not cfg.get('world'):
    for o in (cam, look, focus): o.parent = rig
c = cam.constraints.new('TRACK_TO'); c.target = look; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
cam.data.dof.focus_object = focus
for f, (cl, ll, fl) in cfg['keys'].items():
    sc.frame_set(f); cam.location = cl; look.location = ll; focus.location = fl
    for o in (cam, look, focus): o.keyframe_insert('location')

os.makedirs(out_dir, exist_ok=True)
only = os.environ.get('ONLY')
if only:
    for f in [int(x) for x in only.split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(out_dir, f'{shot}_test_{f:04d}'); bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print('DONE', shot, nframes)
