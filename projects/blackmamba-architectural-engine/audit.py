import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;P=json.loads((R/'parameters.json').read_text());s=bpy.data.scenes['winter_day'];bpy.context.window.scene=s
assert {'winter_day','christmas_night'}<=set(bpy.data.scenes.keys())
assert len([o for o in s.objects if o.name.startswith('Shutter louvre')])>=384
walls=[o for o in s.objects if o.name.startswith('Brick wall')]
assert walls
# Rays through front apertures must not intersect masonry.
for lv in range(2):
 for x in P['window_axes']:
  z=P['base']+lv*P['storey']+.5+P['window_height']/2
  for o in walls:
   origin=o.matrix_world.inverted()@Vector((x,-P['depth']/2-1,z))
   hit,*_=o.ray_cast(origin,Vector((0,1,0)),distance=2)
   assert not hit, (o.name,x,z)
for name in ('Floor slab 1','Floor slab 2'):
 o=bpy.data.objects[name];pt=o.matrix_world.inverted()@Vector((0,2.8,15));hit,*_=o.ray_cast(pt,Vector((0,0,-1)));assert not hit
for x in P['dormer_axes']:
 o=bpy.data.objects['Hip roof'];pt=o.matrix_world.inverted()@Vector((x,-3.25,15));hit,*_=o.ray_cast(pt,Vector((0,0,-1)));assert not hit
assert abs(bpy.data.objects['Foundation'].dimensions.x-P['width'])<1e-5
assert abs(bpy.data.objects['Foundation'].dimensions.y-P['depth'])<1e-5
night=bpy.data.scenes['christmas_night']
for o in s.objects:
 if o.type=='MESH' and not o.name.startswith('Interior luminous'):assert night.objects.get(o.name)==o
assert bpy.data.materials['Glazing blue'].node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value>.9
assert len([o for o in night.objects if o.name.startswith('Interior luminous') and not o.hide_render])>=12
report={'result':'PASS','blender':bpy.app.version_string,'checks':['two scene names','384+ shutter louvres','12 frontal windows clear of masonry','two slab stairwell openings','two roof dormer openings','foundation dimensions agree with parameters','shared architectural objects between scenes','transmissive glass and enabled night panes'],'objects':{s.name:len(s.objects) for s in bpy.data.scenes}}
(R/'audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
