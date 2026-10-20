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
assert s.get('engine_version')=='0.3'
handle=bpy.data.objects['MOVER CASA COMPLETA'];child=bpy.data.objects['Foundation'];before=child.matrix_world.translation.copy();old=handle.location.copy();delta=Vector((.6,.2,0));handle.location+=delta;bpy.context.view_layer.update();assert (child.matrix_world.translation-before-delta).length<1e-5;handle.location=old;bpy.context.view_layer.update()
assert bpy.data.objects['MOVER Auto rojo'].parent is None
assert bpy.data.objects['MOVER Camioneta'].parent is None
assert len([o for o in bpy.data.objects if o.name.startswith('MOVER Arbol')])==3
tyres=[o for o in s.objects if o.name.startswith('v03 tire')];assert len(tyres)==8
for o in tyres:
 world=[o.matrix_world@v.co for v in o.data.vertices];low=min(p.z for p in world);center=sum(world,Vector())/len(world);origin=Vector((center.x,center.y,15));tops=[]
 for surface in s.objects:
  if surface.type=='MESH' and surface.name.startswith(('Winter road','Driveway','Entrance step','Site snow','v03 stone curb','v03 sidewalk','Roadside snow drift')):
   inv=surface.matrix_world.inverted();hit,point,*_=surface.ray_cast(inv@origin,inv.to_3x3()@Vector((0,0,-1)),distance=30)
   if hit:tops.append((surface.matrix_world@point).z)
 assert tops;ground=max(tops);assert 0<=low-ground<.004,(o.name,low,ground)
for handle,L,r,ground in [(bpy.data.objects['MOVER Auto rojo'],3.9,.34,.027),(bpy.data.objects['MOVER Camioneta'],4.8,.37,.012)]:
 body=next(o for o in handle.children if o.name in ('v03 red car body','v03 van body'))
 for x in (-L*.31,L*.31):
  pt=body.matrix_world.inverted()@(handle.matrix_world@Vector((x,-2,r+ground+.20)));hit,*_=body.ray_cast(pt,Vector((0,1,0)),distance=4);assert not hit, 'wheel arch obstructed'
shutters=[o for o in s.objects if o.name.startswith('Shutter') and not o.name.startswith('Shutter louvre') and o.location.y<-P['depth']/2+.1]
for i,o in enumerate(shutters):
 for other in shutters[i+1:]:
  if abs(o.location.z-other.location.z)<.1:assert abs(o.location.x-other.location.x)>=(o.dimensions.x+other.dimensions.x)/2-.001
modules=json.loads((R/'modules.json').read_text());assert len(modules)==6;assert len({m['id'] for m in modules})==6
for m in modules:assert {'id','kind','version','origin','dimensions_m','anchors','materials','lod','dependencies','evidence'}<=m.keys();assert all(v>0 for v in m['dimensions_m'])
from bpy_extras.object_utils import world_to_camera_view
import runpy
geometry_points=runpy.run_path(str(R/'detail.py'))['geometry_points']
framing={}
for name in ('MOVER CASA COMPLETA','MOVER Auto rojo','MOVER Camioneta'):
 handle=bpy.data.objects[name];points=[world_to_camera_view(s,s.camera,p) for o in handle.children_recursive for p in geometry_points(o)]
 assert all(.005<=p.x<=.995 and .005<=p.y<=.995 and p.z>0 for p in points),(name,'outside general camera')
 framing[name]={'min':[min(p[i] for p in points) for i in range(2)],'max':[max(p[i] for p in points) for i in range(2)]}
if bpy.data.objects.get('CAMARA Detalle camioneta'):
 old_y=s.render.resolution_y;s.render.resolution_y=700;cam=bpy.data.objects['CAMARA Detalle camioneta'];h=bpy.data.objects['MOVER Camioneta'];pts=[world_to_camera_view(s,cam,p) for o in h.children_recursive for p in geometry_points(o)];s.render.resolution_y=old_y
 assert all(.01<=p.x<=.99 and .01<=p.y<=.99 and p.z>0 for p in pts),'detail camera crops van'
 framing['Detalle camioneta']={'min':[min(p[i] for p in pts) for i in range(2)],'max':[max(p[i] for p in pts) for i in range(2)]}
(R/'framing.json').write_text(json.dumps(framing,indent=2))
report={'result':'PASS','blender':bpy.app.version_string,'checks':['two scene names','384+ shutter louvres','12 frontal windows clear of masonry','two slab stairwell openings','two roof dormer openings','foundation dimensions agree with parameters','shared architectural objects between scenes','transmissive glass and enabled night panes','house movement handle translates foundation correctly','three tree and two vehicle handles','eight tires within 4mm of sampled ground surfaces','four empty chassis wheel arches','front shutters do not overlap','six module manifests with measured bounds','house and vehicles fully inside main camera','van fully inside detail camera'],'objects':{s.name:len(s.objects) for s in bpy.data.scenes}}
if not bpy.data.objects.get('CAMARA Detalle camioneta'):report['checks'].remove('van fully inside detail camera');report['skipped']=['detail camera absent: render.py adds it']
(R/'audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
