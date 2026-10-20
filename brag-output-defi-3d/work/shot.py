"""CNSNN 3D shot: a phone lying on a duvet in a bedroom at night, the screen playing a frame sequence.
Usage: python shot.py -- <screen_dir> <hdr> <out_dir> <shot_name> [frames] [first_frame]"""
import bpy, bmesh, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index('--') + 1:]
screen_dir, hdr, out_dir, shot = argv[:4]
nframes = int(argv[4]) if len(argv) > 4 else len([f for f in os.listdir(screen_dir) if f.endswith('.png')])
first = int(argv[5]) if len(argv) > 5 else 1
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

# World: dim indoor HDRI for reflections
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; nt = w.node_tree
env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdr)
nt.nodes['Background'].inputs[1].default_value = 0.06; nt.links.new(env.outputs[0], nt.nodes['Background'].inputs[0])

# Duvet with soft folds
bpy.ops.mesh.primitive_plane_add(size=1.4, location=(0, 0.25, 0)); bed = bpy.context.object
sub = bed.modifiers.new('s', 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = sub.render_levels = 7
tx = bpy.data.textures.new('folds', 'CLOUDS'); tx.noise_scale = 0.09; tx.noise_depth = 2
dp = bed.modifiers.new('d', 'DISPLACE'); dp.texture = tx; dp.strength = 0.03; dp.mid_level = 0.5
m, b = principled('duvet', **{'Base Color': (0.5, 0.42, 0.36, 1), 'Roughness': 0.92})
b.inputs['Sheen Weight'].default_value = 0.8; b.inputs['Sheen Roughness'].default_value = 0.4
n = m.node_tree.nodes; weave = n.new('ShaderNodeTexNoise'); weave.inputs['Scale'].default_value = 900
bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.15
m.node_tree.links.new(weave.outputs[0], bump.inputs['Height']); m.node_tree.links.new(bump.outputs[0], b.inputs['Normal'])
bed.data.materials.append(m); bpy.ops.object.shade_smooth()
bed.location.z = -0.006
# Pillow behind (out of focus)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0.15, 0.75, 0.06)); pil = bpy.context.object
pil.scale = (0.38, 0.2, 0.09); pil.data.materials.append(m); bpy.ops.object.shade_smooth()
# Wall + headboard
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 1.15, 1.0), rotation=(math.radians(90), 0, 0)); wall = bpy.context.object
mw, _ = principled('wall', **{'Base Color': (0.3, 0.24, 0.2, 1), 'Roughness': 0.8}); wall.data.materials.append(mw)
# Bedside lamp: glowing shade (bokeh) and its light
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.2, location=(-0.75, 0.95, 0.42)); shade = bpy.context.object
ms, sb = principled('shade', **{'Base Color': (1, 0.8, 0.6, 1)}); sb.inputs['Emission Color'].default_value = (1, 0.55, 0.25, 1); sb.inputs['Emission Strength'].default_value = 7
shade.data.materials.append(ms)
bpy.ops.object.light_add(type='POINT', location=(-0.55, 0.55, 0.22)); L = bpy.context.object
L.data.energy = 38; L.data.color = (1, 0.58, 0.3); L.data.shadow_soft_size = 0.1
# A faint cool fill from the window side so the phone frame reads
bpy.ops.object.light_add(type='AREA', location=(0.9, -0.4, 0.8)); F = bpy.context.object
F.data.energy = 2.5; F.data.color = (0.75, 0.82, 1); F.data.size = 1.0; F.rotation_euler = (math.radians(55), 0, math.radians(60))

# Phone: 71.6 x 150.8 x 8.25 mm, titanium frame, rounded corners
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
# Black glass front (bezel) and the screen
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
first_file = sorted(f for f in os.listdir(screen_dir) if f.endswith('.png'))[0]
img.image = bpy.data.images.load(os.path.join(screen_dir, first_file)); img.image.source = 'SEQUENCE'
img.image_user.frame_duration = nframes; img.image_user.frame_start = 1; img.image_user.frame_offset = first - 1; img.image_user.use_auto_refresh = True
sbsdf.inputs['Base Color'].default_value = (0, 0, 0, 1); sbsdf.inputs['Roughness'].default_value = 0.03
sbsdf.inputs['Coat Weight'].default_value = 1; sbsdf.inputs['Coat Roughness'].default_value = 0.02
m.node_tree.links.new(img.outputs[0], sbsdf.inputs['Emission Color']); sbsdf.inputs['Emission Strength'].default_value = 1.7
scr.data.materials.append(m)
# Group the phone and lay it on the duvet at a slight angle
rig = bpy.data.objects.new('rig', None); sc.collection.objects.link(rig)
for o in (ph, glass, scr): o.parent = rig
rig.rotation_euler = (0, 0, math.radians(-8)); rig.location = (0, 0, 0.002)

# Camera: slow glide across the thread, focus on the lower half where messages arrive
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 50; cam.data.sensor_width = 36
cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = 5.0
tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt)
c = cam.constraints.new('TRACK_TO'); c.target = tgt; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
cam.data.dof.focus_object = tgt
keys = {  # frame: (camera location, target location)
    1: ((-0.06, -0.175, 0.15), (-0.004, -0.018, 0.0)),
    nframes: ((0.04, -0.16, 0.135), (0.004, -0.036, 0.0)),
}
for f, (cl, tl) in keys.items():
    sc.frame_set(f); cam.location = cl; tgt.location = tl
    cam.keyframe_insert('location'); tgt.keyframe_insert('location')
os.makedirs(out_dir, exist_ok=True)
print('FRAMES', nframes)
only = os.environ.get('ONLY')
if only:
    for f in [int(x) for x in only.split(',')]:
        sc.frame_set(f); sc.render.filepath = os.path.join(out_dir, f'{shot}_test_{f:04d}'); bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
print('DONE')
