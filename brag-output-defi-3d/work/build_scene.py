"""Builds scene.blend: a bedroom at night with a phone lying on a cloth-simulated duvet.
Usage: python build_scene.py -- <hdr> <out.blend>"""
import bpy, bmesh, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
hdr, out = argv[:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m, b
def link(m, a, b): m.node_tree.links.new(a, b)
def bumpy(m, b, kind, scale, strength, **kw):
    n = m.node_tree.nodes; t = n.new(kind); t.inputs['Scale'].default_value = scale
    for k, v in kw.items(): t.inputs[k].default_value = v
    bu = n.new('ShaderNodeBump'); bu.inputs['Strength'].default_value = strength
    link(m, t.outputs[0] if kind != 'ShaderNodeTexVoronoi' else t.outputs['Distance'], bu.inputs['Height']); link(m, bu.outputs[0], b.inputs['Normal'])
    return t
def obj_box(name, size, loc, mat, bevel=0.01):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.location = loc
    if bevel: bv = o.modifiers.new('bv', 'BEVEL'); bv.width = bevel; bv.segments = 4
    o.data.materials.append(mat); return o

# World: very dim, the lamp does the work
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdr)
nt.nodes['Background'].inputs[1].default_value = 0.025; nt.links.new(env.outputs[0], nt.nodes['Background'].inputs[0])

# --- Materials ---
linen, lb = principled('linen', **{'Base Color': (0.56, 0.5, 0.45, 1), 'Roughness': 0.95})
lb.inputs['Sheen Weight'].default_value = 1.0; lb.inputs['Sheen Roughness'].default_value = 0.35
bumpy(linen, lb, 'ShaderNodeTexWave', 1400, 0.25, Distortion=3.0)
pillowm, pb = principled('pillow', **{'Base Color': (0.62, 0.58, 0.54, 1), 'Roughness': 0.95})
pb.inputs['Sheen Weight'].default_value = 1.0; bumpy(pillowm, pb, 'ShaderNodeTexNoise', 900, 0.2)
wood, wb = principled('wood', **{'Roughness': 0.38})
n = wood.node_tree.nodes; wave = n.new('ShaderNodeTexWave'); wave.wave_type = 'RINGS'
wave.inputs['Scale'].default_value = 0.9; wave.inputs['Distortion'].default_value = 4; wave.inputs['Detail'].default_value = 6
ramp = n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (0.13, 0.07, 0.035, 1); ramp.color_ramp.elements[1].color = (0.2, 0.11, 0.055, 1)
link(wood, wave.outputs[1], ramp.inputs[0]); link(wood, ramp.outputs[0], wb.inputs['Base Color'])
uph, ub = principled('upholstery', **{'Base Color': (0.16, 0.15, 0.17, 1), 'Roughness': 0.9})
ub.inputs['Sheen Weight'].default_value = 0.8
vor = bumpy(uph, ub, 'ShaderNodeTexVoronoi', 7, 0.6)
plaster, plb = principled('plaster', **{'Base Color': (0.36, 0.33, 0.30, 1), 'Roughness': 0.9})
bumpy(plaster, plb, 'ShaderNodeTexNoise', 60, 0.08)
floorm, fb = principled('floor', **{'Roughness': 0.35})
n = floorm.node_tree.nodes; brick = n.new('ShaderNodeTexBrick'); brick.inputs['Scale'].default_value = 3
brick.inputs['Color1'].default_value = (0.14, 0.08, 0.045, 1); brick.inputs['Color2'].default_value = (0.11, 0.06, 0.035, 1)
brick.inputs['Mortar'].default_value = (0.05, 0.03, 0.02, 1); brick.inputs['Mortar Size'].default_value = 0.003
brick.inputs['Brick Width'].default_value = 1.6; brick.inputs['Row Height'].default_value = 0.12
link(floorm, brick.outputs[0], fb.inputs['Base Color'])
ceramic, _ = principled('ceramic', **{'Base Color': (0.75, 0.72, 0.66, 1), 'Roughness': 0.2, 'Coat Weight': 0.6})
curtain, cb = principled('curtain', **{'Base Color': (0.12, 0.13, 0.15, 1), 'Roughness': 0.95}); cb.inputs['Sheen Weight'].default_value = 0.6
cable, _ = principled('cable', **{'Base Color': (0.8, 0.8, 0.78, 1), 'Roughness': 0.4})

# --- Room: phone at the origin, bed to its right, headboard behind ---
BX, BY = 0.42, 0.18
MZ = -0.02                                      # mattress top
obj_box('mattress', (1.8, 2.1, 0.28), (BX, BY, MZ - 0.14), linen, 0.04)
obj_box('bedframe', (1.9, 2.2, 0.22), (BX, BY, MZ - 0.36), wood, 0.01)
hb = obj_box('headboard', (1.95, 0.09, 1.0), (BX, BY + 1.12, MZ + 0.25), uph, 0.035)
obj_box('floor', (8, 8, 0.02), (0, 0, -0.5), floorm, 0)
wall = obj_box('wall', (8, 0.05, 4), (0, BY + 1.2, 1.5), plaster, 0)
obj_box('sidewall', (0.05, 8, 4), (BX - 2.3, 0, 1.5), plaster, 0)
# Pillows: soft rounded blocks with a slight sag
pillows = []
for i, px in enumerate((BX - 0.45, BX + 0.45)):
    bpy.ops.mesh.primitive_cube_add(size=1); p = bpy.context.object; p.name = f'pillow{i}'
    p.scale = (0.72, 0.42, 0.16); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    p.location = (px, BY + 0.86, MZ + 0.07)
    p.rotation_euler = (math.radians(-12), 0, math.radians(3 - 6 * i))
    s = p.modifiers.new('s', 'SUBSURF'); s.levels = s.render_levels = 3
    c = p.modifiers.new('c', 'CAST'); c.factor = 0.45
    t = bpy.data.textures.new(f'pw{i}', 'CLOUDS'); t.noise_scale = 0.08
    d = p.modifiers.new('d', 'DISPLACE'); d.texture = t; d.strength = 0.012
    p.data.materials.append(pillowm); bpy.ops.object.shade_smooth(); pillows.append(p)

# Duvet: cloth simulation draped over the mattress and pillows
bpy.ops.mesh.primitive_grid_add(x_subdivisions=110, y_subdivisions=96, size=1, location=(BX, BY - 0.28, MZ + 0.2))
duvet = bpy.context.object; duvet.name = 'duvet'; duvet.scale = (2.1, 1.7, 1); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
t = bpy.data.textures.new('ruffle', 'CLOUDS'); t.noise_scale = 0.42; t.noise_depth = 1
d = duvet.modifiers.new('ruffle', 'DISPLACE'); d.texture = t; d.strength = 0.09
bpy.ops.object.modifier_apply(modifier='ruffle')
cl = duvet.modifiers.new('cloth', 'CLOTH'); cs = cl.settings
cs.quality = 6; cs.mass = 0.6; cs.tension_stiffness = 12; cs.compression_stiffness = 12; cs.shear_stiffness = 6; cs.bending_stiffness = 3.0
cs.air_damping = 2.0
cl.collision_settings.distance_min = 0.006; cl.collision_settings.use_self_collision = False
for o in [bpy.data.objects['mattress'], bpy.data.objects['bedframe']] + pillows:
    m = o.modifiers.new('col', 'COLLISION'); o.collision.thickness_outer = 0.01; o.collision.cloth_friction = 8
sc.frame_start, sc.frame_end = 1, 45
cl.point_cache.frame_start, cl.point_cache.frame_end = 1, 45
for f in range(1, 46): sc.frame_set(f)
bpy.context.view_layer.objects.active = duvet
bpy.ops.object.modifier_apply(modifier='cloth')
tx = bpy.data.textures.new('folds', 'CLOUDS'); tx.noise_scale = 0.3; tx.noise_depth = 1
dm = duvet.modifiers.new('folds', 'DISPLACE'); dm.texture = tx; dm.strength = 0.02
rx = bpy.data.textures.new('ridges', 'WOOD'); rx.wood_type = 'BANDNOISE'; rx.noise_scale = 0.25; rx.turbulence = 10
dr = duvet.modifiers.new('ridges', 'DISPLACE'); dr.texture = rx; dr.strength = 0.007
so = duvet.modifiers.new('thick', 'SOLIDIFY'); so.thickness = 0.03; so.offset = -1
sm = duvet.modifiers.new('sub', 'SUBSURF'); sm.levels = sm.render_levels = 2
duvet.data.materials.append(linen); bpy.ops.object.shade_smooth()
for o in [bpy.data.objects['mattress'], bpy.data.objects['bedframe']] + pillows: o.modifiers.remove(o.modifiers['col'])
sc.frame_set(1)

# Nightstand with books, a mug and the lamp
NX, NY = BX - 1.2, BY + 0.95
obj_box('nightstand', (0.46, 0.4, 0.52), (NX, NY, -0.24), wood, 0.012)
for i, (h, col) in enumerate(((0.035, (0.35, 0.08, 0.06)), (0.028, (0.08, 0.15, 0.22)), (0.04, (0.55, 0.45, 0.3)))):
    bm_, _ = principled(f'book{i}', **{'Base Color': (*col, 1), 'Roughness': 0.6})
    obj_box(f'book{i}', (0.17 - i * 0.01, 0.24 - i * 0.015, h), (NX + 0.08, NY - 0.06, 0.02 + sum((0.035, 0.028, 0.04)[:i]) + h / 2), bm_, 0.004).rotation_euler.z = math.radians(8 - i * 7)
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.09, location=(NX - 0.13, NY - 0.1, 0.065)); mug = bpy.context.object
mug.data.materials.append(ceramic); bpy.ops.object.shade_smooth()
brass, _ = principled('brass', **{'Base Color': (0.6, 0.45, 0.25, 1), 'Metallic': 1, 'Roughness': 0.3})
bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.03, location=(NX - 0.05, NY + 0.07, 0.035)); bpy.context.object.data.materials.append(brass)
bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.32, location=(NX - 0.05, NY + 0.07, 0.2)); bpy.context.object.data.materials.append(brass)
bpy.ops.mesh.primitive_cone_add(radius1=0.17, radius2=0.11, depth=0.22, location=(NX - 0.05, NY + 0.07, 0.42), end_fill_type='NOTHING'); shade = bpy.context.object
so = shade.modifiers.new('t', 'SOLIDIFY'); so.thickness = 0.003
ms, sb = principled('shade', **{'Base Color': (1, 0.86, 0.68, 1), 'Roughness': 0.85})
sb.inputs['Transmission Weight'].default_value = 0.6
sb.inputs['Emission Color'].default_value = (1, 0.55, 0.25, 1); sb.inputs['Emission Strength'].default_value = 1.6
shade.data.materials.append(ms)
LX, LY, LZ = NX - 0.05, NY + 0.07, 0.42
bpy.ops.object.light_add(type='POINT', location=(LX, LY, LZ)); L = bpy.context.object
L.data.energy = 70; L.data.color = (1, 0.55, 0.27); L.data.shadow_soft_size = 0.03
for z, rot in ((0.5, 0), (0.33, math.pi)):           # light pools up and down the wall
    bpy.ops.object.light_add(type='SPOT', location=(LX, LY, LZ + (0.08 if rot == 0 else -0.08)), rotation=(rot, 0, 0)); S = bpy.context.object
    S.data.energy = 60; S.data.color = (1, 0.55, 0.27); S.data.spot_size = math.radians(95); S.data.spot_blend = 0.6; S.data.shadow_soft_size = 0.05
# Warm bounce near the phone (grazing light across the folds) and a faint cold window light
bpy.ops.object.light_add(type='POINT', location=(-0.55, 0.55, 0.22)); K = bpy.context.object
K.data.energy = 22; K.data.color = (1, 0.58, 0.3); K.data.shadow_soft_size = 0.15
bpy.ops.object.light_add(type='AREA', location=(1.6, -0.6, 1.2)); F = bpy.context.object
F.data.energy = 6; F.data.color = (0.6, 0.72, 1); F.data.size = 1.2; F.rotation_euler = (math.radians(60), 0, math.radians(70))
# Framed print above the bed, curtain on the right
obj_box('frame', (0.62, 0.025, 0.44), (BX + 0.1, BY + 1.17, 0.95), wood, 0.006)
bpy.ops.mesh.primitive_plane_add(size=1, location=(BX + 0.1, BY + 1.155, 0.95), rotation=(math.radians(90), 0, 0)); art = bpy.context.object
art.scale = (0.54, 0.36, 1)
ma, ab = principled('print', **{'Roughness': 0.7}); n = ma.node_tree.nodes
gr = n.new('ShaderNodeTexNoise'); gr.inputs['Scale'].default_value = 2.2; gr.inputs['Detail'].default_value = 3
rp = n.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (0.05, 0.08, 0.12, 1); rp.color_ramp.elements[1].color = (0.6, 0.42, 0.25, 1)
link(ma, gr.outputs[0], rp.inputs[0]); link(ma, rp.outputs[0], ab.inputs['Base Color']); art.data.materials.append(ma)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=80, y_subdivisions=4, size=1, location=(BX + 1.6, BY + 1.05, 0.9), rotation=(math.radians(90), 0, 0))
cur = bpy.context.object; cur.scale = (0.9, 2.6, 1)
t = bpy.data.textures.new('pleats', 'WOOD'); t.wood_type = 'BANDNOISE'; t.noise_scale = 0.05
dc = cur.modifiers.new('d', 'DISPLACE'); dc.texture = t; dc.strength = 0.05; dc.direction = 'Z'
cur.data.materials.append(curtain); bpy.ops.object.shade_smooth()

# --- Phone (71.6 x 150.8 x 8.25 mm), resting on the duvet at the origin ---
W, H, D = 0.0716, 0.1508, 0.00825
bpy.ops.mesh.primitive_cube_add(size=1); ph = bpy.context.object; ph.name = 'phone'
ph.scale = (W, H, D); bpy.ops.object.transform_apply(scale=True)
bm = bmesh.new(); bm.from_mesh(ph.data)
vert = [e for e in bm.edges if abs(e.verts[0].co.z - e.verts[1].co.z) > D * 0.5]
bmesh.ops.bevel(bm, geom=vert, offset=0.0115, segments=18, affect='EDGES', profile=0.5)
bm.to_mesh(ph.data); bm.free()
bv = ph.modifiers.new('bv', 'BEVEL'); bv.width = 0.0028; bv.segments = 6; bv.limit_method = 'ANGLE'
mt, _ = principled('titanium', **{'Base Color': (0.2, 0.19, 0.18, 1), 'Metallic': 1.0, 'Roughness': 0.3})
ph.data.materials.append(mt); bpy.ops.object.shade_smooth(); ph.location = (0, 0, D / 2)
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
m = bpy.data.materials.new('screen'); m.use_nodes = True; sbsdf = m.node_tree.nodes['Principled BSDF']
sbsdf.inputs['Base Color'].default_value = (0, 0, 0, 1); sbsdf.inputs['Roughness'].default_value = 0.03
sbsdf.inputs['Coat Weight'].default_value = 1; sbsdf.inputs['Coat Roughness'].default_value = 0.02
sbsdf.inputs['Emission Strength'].default_value = 1.7
scr.data.materials.append(m)
rig = bpy.data.objects.new('rig', None); sc.collection.objects.link(rig)
for o in (ph, glass, scr): o.parent = rig
# Sit the phone on the duvet surface: ray-cast down at its corners
dg = bpy.context.evaluated_depsgraph_get()
eval_duvet = duvet.evaluated_get(dg); inv = eval_duvet.matrix_world.inverted()
def surface_z(x, y):
    hit, loc, nrm, idx = eval_duvet.ray_cast(inv @ Vector((x, y, 1.0)), Vector((0, 0, -1)))
    return (eval_duvet.matrix_world @ loc).z if hit else MZ
rot = math.radians(-8)
pts = [(sx * W / 2, sy * H / 2) for sx in (-1, 1) for sy in (-1, 1)]
world = [(x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)) for x, y in pts]
zs = [surface_z(x, y) for x, y in world]
z0 = max(zs) - 0.004                                 # sink a little into the soft duvet
tilt_x = math.atan2((zs[1] + zs[3]) - (zs[0] + zs[2]), 2 * H) * 0.7
tilt_y = -math.atan2((zs[2] + zs[3]) - (zs[0] + zs[1]), 2 * W) * 0.7
rig.location = (0, 0, z0); rig.rotation_euler = (tilt_x, tilt_y, rot)
# Charging cable from the phone's bottom edge, trailing across the duvet
cu = bpy.data.curves.new('cable', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.0018; cu.bevel_resolution = 4
sp = cu.splines.new('BEZIER'); pts = [(0.012, -0.08), (0.03, -0.16), (-0.05, -0.26), (0.06, -0.42), (0.3, -0.55)]
sp.bezier_points.add(len(pts) - 1)
for bp, (x, y) in zip(sp.bezier_points, pts):
    bp.co = (x, y, surface_z(x, y) + 0.003); bp.handle_left_type = bp.handle_right_type = 'AUTO'
co = bpy.data.objects.new('cable', cu); sc.collection.objects.link(co); co.data.materials.append(cable)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(out))
print('SAVED', out, 'phone z', round(z0, 4))
