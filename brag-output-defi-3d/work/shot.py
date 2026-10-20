"""CNSNN video 2, 3D shots: a phone lying on a bed at night, its screen playing a frame sequence.
Usage: python shot.py -- <shot> <screen_dir> <hdr> <out_dir>   (ONLY=1,60 renders single test frames)"""
import bpy, bmesh, math, sys, os
argv = sys.argv[sys.argv.index('--') + 1:]
shot, screen_dir, hdr, out_dir = argv[:4]

# Per shot: lens, f-stop and keys {frame: (camera, look-at, focus)} in phone space (x right, y towards the top, z out of the screen),
# except 'open' which is in room space. Units: metres.
SHOTS = {
    'open':    dict(lens=40, fstop=2.0, world=True, keys={
        1: ((0.46, -0.92, 0.46), (-0.04, 0.22, 0.02), (0.0, 0.0, 0.0)),
        39: ((0.33, -0.64, 0.33), (-0.03, 0.16, 0.02), (0.0, 0.0, 0.0))}),
    'chat':    dict(lens=50, fstop=8.0, keys={
        1: ((-0.060, -0.175, 0.150), (-0.004, -0.018, 0.0), (0.0, -0.03, 0.08)),
        30: ((-0.048, -0.173, 0.148), (-0.003, -0.021, 0.0), (0.0, -0.031, 0.0)),
        144: ((-0.008, -0.165, 0.140), (0.0, -0.030, 0.0), (0.0, -0.033, 0.0))}),
    'type':    dict(lens=50, fstop=5.6, keys={
        1: ((-0.030, -0.128, 0.088), (-0.004, -0.024, 0.0), (-0.004, -0.022, 0.0)),
        117: ((0.012, -0.122, 0.082), (0.004, -0.024, 0.0), (0.004, -0.020, 0.0))}),
    'mock':    dict(lens=50, fstop=7.0, keys={
        1: ((0.062, -0.150, 0.150), (0.0, 0.010, 0.0), (0.0, 0.010, 0.0)),
        96: ((0.040, -0.136, 0.136), (0.0, 0.006, 0.0), (0.0, 0.004, 0.0))}),
    'app':     dict(lens=50, fstop=7.0, keys={
        1: ((-0.016, -0.128, 0.112), (0.0, -0.008, 0.0), (0.0, -0.006, 0.0)),
        70: ((-0.008, -0.126, 0.110), (0.0, -0.010, 0.0), (0.0, -0.008, 0.0)),
        105: ((0.006, -0.195, 0.185), (0.0, -0.028, 0.0), (0.0, -0.028, 0.0)),
        165: ((0.014, -0.188, 0.178), (0.0, -0.030, 0.0), (0.0, -0.030, 0.0))}),
    'revenge': dict(lens=50, fstop=8.0, keys={
        1: ((0.060, -0.190, 0.160), (0.0, -0.030, 0.0), (0.0, -0.040, 0.0)),
        180: ((-0.010, -0.172, 0.145), (0.0, -0.042, 0.0), (0.0, -0.048, 0.0))}),
}
cfg = SHOTS[shot]
pngs = sorted(f for f in os.listdir(screen_dir) if f.endswith('.png'))
nframes = len(pngs)

bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scene.blend'))
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 12; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.cycles.max_bounces = 4; sc.render.use_persistent_data = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, int(os.environ.get('RES', 67))
sc.render.fps = 30; sc.frame_start, sc.frame_end = 1, nframes
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.4
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = os.path.join(out_dir, shot + '_')
# Screen plays the shot's frame sequence
m = bpy.data.materials['screen']; nn = m.node_tree.nodes; sbsdf = nn['Principled BSDF']
img = nn.new('ShaderNodeTexImage')
img.image = bpy.data.images.load(os.path.join(screen_dir, pngs[0])); img.image.source = 'SEQUENCE'
img.image_user.frame_duration = nframes; img.image_user.frame_start = 1; img.image_user.use_auto_refresh = True
m.node_tree.links.new(img.outputs[0], sbsdf.inputs['Emission Color'])
rig = bpy.data.objects['rig']

# --- Camera, look-at and focus targets (phone space unless the shot is in room space) ---
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = cfg['lens']; cam.data.sensor_width = 36
cam.data.dof.use_dof = True; cam.data.dof.aperture_fstop = float(os.environ.get('FSTOP', cfg['fstop']))
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
