"""Blender 5.2: reproducible conceptual reconstruction. Run with --background --python.
Front = negative Y; dimensions in metres. No external textures or dependencies.
"""
import bpy, math, json, random, sys, time, resource
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
BUILD_STARTED=time.perf_counter()
P=json.loads((ROOT/'parameters.json').read_text())
random.seed(P['seed'])
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.name='winter_day';s.unit_settings.system='METRIC'
W,D,T,B,H,R=[P[k] for k in ('width','depth','wall','base','storey','roof_rise')]
E=B+2*H; A=W/2+P['overhang']; C=D/2+P['overhang']; ridge=A-C

def mat(name,color,rough=.6,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
 return m
brick=mat('Brick fired red',(.32,.075,.035));white=mat('Paint ivory',(.8,.78,.68));dark=mat('Shutters forest black',(.025,.045,.035));roof=mat('Slate brown',(.065,.052,.042));snow=mat('Snow',(.87,.94,1));glass=mat('Glazing blue',(.12,.26,.34),.18);stone=mat('Limestone',(.38,.34,.27));green=mat('Winter shrubs',(.025,.09,.045));wood=mat('Door walnut',(.06,.023,.01));warm=mat('Warm interior', (1,.48,.12),emission=3)
glass.node_tree.nodes['Principled BSDF'].inputs['Transmission Weight'].default_value=.95
glass.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.85,.94,1,1)
# Procedural mortar with physical-scale coordinates; independent of object dimensions.
n=brick.node_tree.nodes;l=brick.node_tree.links
tex=n.new('ShaderNodeTexBrick');tex.inputs['Color1'].default_value=(.32,.065,.025,1);tex.inputs['Color2'].default_value=(.18,.035,.012,1);tex.inputs['Mortar'].default_value=(.24,.19,.15,1);tex.inputs['Scale'].default_value=1;tex.inputs['Brick Width'].default_value=.24;tex.inputs['Row Height'].default_value=.075;tex.inputs['Mortar Size'].default_value=.004
coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(1,1,1)
# Use Geometry Position swizzle X,Z for front/back; texture is supplemental relief.
geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');comb=n.new('ShaderNodeCombineXYZ');l.new(geo.outputs['Position'],sep.inputs[0]);l.new(sep.outputs['X'],comb.inputs['X']);l.new(sep.outputs['Z'],comb.inputs['Y']);l.new(sep.outputs['Y'],comb.inputs['Z']);l.new(comb.outputs[0],tex.inputs['Vector']);l.new(tex.outputs['Color'],n.get('Principled BSDF').inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.25;bump.inputs['Distance'].default_value=.008;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],n.get('Principled BSDF').inputs['Normal'])

def cube(name,loc,size,material,bevel=0):
 # Direct mesh construction avoids thousands of context-dependent operators.
 verts=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.update()
 o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.location=loc
 if material:me.materials.append(material)
 if bevel:m=o.modifiers.new('Edge detail','BEVEL');m.width=bevel;m.segments=2
 o['source']='inferred conceptual geometry';return o

def mesh(name,v,f,material):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.data.materials.append(material);return o

def line(name,pts,r,material):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,cu);s.collection.objects.link(o);o.data.materials.append(material);return o

SPHERE_MESHES={}
def sphere(name,loc,scale,material):
 if material.name not in SPHERE_MESHES:
  import bmesh
  me=bpy.data.meshes.new('Shared sphere '+material.name);bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=12,v_segments=8,radius=1);bm.to_mesh(me);bm.free();me.materials.append(material)
  for polygon in me.polygons:polygon.use_smooth=True
  SPHERE_MESHES[material.name]=me
 o=bpy.data.objects.new(name,SPHERE_MESHES[material.name]);s.collection.objects.link(o);o.location=loc;o.scale=scale;return o

cube('Foundation',(0,0,B/2),(W,D,B),stone,.04)
for level in range(3):
 slab=cube('Floor slab '+str(level),(0,0,B+level*H-.1),(W-.1,D-.1,.2),stone)
 if level:
  cut=cube('Stairwell cutter',(0,2.85,B+level*H),(1.35,4.3,.8),None)
  mod=slab.modifiers.new('Stairwell opening','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=slab;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Wall grids omit apertures: actual empty openings, no black decals.
openings=[]
for level in range(2):
 for x in P['window_axes']:openings.append((x,B+level*H+.5,P['window_width'],P['window_height']))
openings.append((0,B,1.45,2.55))
for side in (-1,1):
 holes=openings if side==-1 else [(x,z,w,h) for x,z,w,h in openings if x!=0]
 xs=sorted(set([-W/2,W/2]+[x+q*w/2 for x,z,w,h in holes for q in (-1,1)]));zs=sorted(set([B,E]+[z+q*h for x,z,w,h in holes for q in (0,1)]))
 for x1,x2 in zip(xs,xs[1:]):
  for z1,z2 in zip(zs,zs[1:]):
   x=(x1+x2)/2;z=(z1+z2)/2
   if not any(abs(x-hx)<w/2 and hz<z<hz+h for hx,hz,w,h in holes):cube('Brick wall', (x,side*(D-T)/2,z),(x2-x1,T,z2-z1),brick)
# Side apertures via booleans, applied to wall only.
for side in (-1,1):
 wall=cube('Side masonry',(side*(W-T)/2,0,(B+E)/2),(T,D,E-B),brick)
 for level in range(2):
  for y in (-3.3,0,3.3):
   z=B+level*H+.5+P['window_height']/2
   cut=cube('Opening cutter',(side*W/2,y,z),(T*3,1.3,P['window_height']),None)
   mod=wall.modifiers.new('Actual aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut;bpy.context.view_layer.objects.active=wall;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)

def window(x,y,z,w=1.15,h=2,side=False,shutters=True):
 # Build local front-facing assembly, rotate for side faces.
 objs=[]
 def c(name,loc,sz,ma):o=cube(name,loc,sz,ma,.012);objs.append(o);return o
 c('Glass', (0,0,h/2),(w,.035,h),glass)
 c('Interior luminous pane',(0,.06,h/2),(w-.12,.02,h-.12),warm)
 for xx in (-w/2,w/2):c('Window jamb',(xx,-.06,h/2),(.075,.16,h+.16),white)
 for zz in (0,h,h/2):c('Sash horizontal',(0,-.09,zz),(w+.12,.14,.065),white)
 for xx in (-w/6,w/6):c('Muntin',(xx,-.1,h/2),(.035,.08,h),white)
 for zz in (h/4,3*h/4):c('Muntin',(0,-.1,zz),(w,.08,.035),white)
 c('Stone sill',(0,-.11,-.08),(w+.26,.32,.12),white)
 if shutters:
  for sign in (-1,1):
   xx=sign*(w/2+.18);c('Shutter',(xx,0,h/2),(.28,.09,h),dark)
   for j in range(16):c('Shutter louvre',(xx,-.065,.08+j*(h-.16)/15),(.24,.035,.035),dark)
 for o in objs:
  lx,ly,lz=o.location
  if side:o.location=(x-ly,y+lx,z+lz);o.rotation_euler.z=math.pi/2
  else:o.location=(x+lx,y+ly,z+lz)
for face in (-1,1):
 for x,z,w,h in openings:
  if x:window(x,face*D/2,z,w,h)
for side in (-1,1):
 for lv in range(2):
  for y in (-3.3,0,3.3):window(side*W/2,y,B+lv*H+.5,1.3,2,True,False)
for z in (B,E):
 cube('Front cornice',(0,-D/2-.08,z),(W+.3,.3,.18),white,.025);cube('Rear cornice',(0,D/2+.08,z),(W+.3,.3,.18),white,.025)
 for x in (-W/2,W/2):cube('Side cornice',(x,0,z),(.3,D+.3,.18),white,.025)
# Hip roof surface; tile geometry conforms analytically.
def roofz(x,y):return E+R*max(0,min((A-abs(x))/C,(C-abs(y))/C))
v=[(-A,-C,E),(A,-C,E),(A,C,E),(-A,C,E),(-ridge,0,E+R),(ridge,0,E+R)]
base_roof=mesh('Hip roof',v,[(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)],roof)
mod=base_roof.modifiers.new('Roof thickness','SOLIDIFY');mod.thickness=.12
bpy.context.view_layer.objects.active=base_roof;bpy.ops.object.modifier_apply(modifier=mod.name)
for dx in P['dormer_axes']:
 cut=cube('Dormer aperture cutter',(dx,-3.25,E+1.5),(1.4,1.6,5),None)
 mod=base_roof.modifiers.new('Dormer roof opening','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=base_roof;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Batched individual quad shingles; deterministic snow coverage.
tv=[];tf=[];sv=[];sf=[]
for yi in range(int(2*C/.25)):
 y=-C+yi*.25
 for xi in range(int(2*A/.4)):
  x=-A+xi*.4
  if any(abs(x+.2-dx)<.9 and -4.3<y+.12<-2.2 for dx in P['dormer_axes']):continue
  verts=[(xx,yy,roofz(xx,yy)+.028) for xx,yy in ((x,y),(x+.385,y),(x+.385,y+.235),(x,y+.235))]
  idx=len(tv);tv+=verts;tf.append(tuple(range(idx,idx+4)))
  if (math.sin(x*.9)+math.cos(y*1.3)+.4*math.sin(x*2+y))>.55 or abs(y)<.4:
   idx=len(sv);sv += [(xx,yy,zz+.05) for xx,yy,zz in verts];sf.append(tuple(range(idx,idx+4)))
mesh('Individual slate tiles',tv,tf,roof);mesh('Snow patches roof',sv,sf,snow)
# Two dormers: hollow cheeks and roof apertures.
for x in P['dormer_axes']:
 y=-3.25;z=roofz(x,y)
 for sign in (-1,1):cube('Dormer side cheek',(x+sign*.765,y,z+.65),(.12,1.75,1.5),white)
 cube('Dormer front sill',(x,y-.85,z+.01),(1.65,.12,.12),white)
 for sign in (-1,1):cube('Dormer front jamb',(x+sign*.7,y-.85,z+.75),(.25,.12,1.5),white)
 window(x,y-.9,z+.08,1.15,1.35,False,False)
 mesh('Dormer gable',[(x-.92,y-1,z+1.5),(x+.92,y-1,z+1.5),(x,y-1,z+2.2)],[(0,1,2)],white)
 mesh('Dormer pitched roof',[(x-.98,y-1.08,z+1.5),(x,y-1.08,z+2.25),(x+.98,y-1.08,z+1.5),(x-.98,y+.95,z+1.5),(x,y+.95,z+2.25),(x+.98,y+.95,z+1.5)],[(0,1,4,3),(1,2,5,4)],roof)
for x in (-5.8,):cube('Chimney',(x,2,E+1.7),(.85,.95,2.8),brick);cube('Chimney cap',(x,2,E+3.12),(1.05,1.15,.16),stone)
# Entrance with real curved moulding, sidelights, fanlight and panelled door.
cube('Door',(0,-D/2+.04,B+1.12),(1.3,.12,2.24),wood,.02)
for xx in (-.32,.32):
 for zz in (.45,1.1,1.78):cube('Raised door panels',(xx,-D/2-.035,B+zz),(.5,.065,.48),wood,.025)
for x in (-1.04,1.04):
 cube('Portico pilaster',(x,-D/2-.42,B+1.2),(.23,.45,2.4),white,.025)
 cube('Pilaster capital',(x,-D/2-.42,B+2.42),(.36,.56,.16),white,.025)
 window(x*.79,-D/2-.08,B+.15,.25,2.15,False,False)
pts=[(1.18*math.cos(t),-D/2-.5,B+2.35+.7*math.sin(t)) for t in [i*math.pi/48 for i in range(49)]]
line('Arch moulding',pts,.13,white)
line('Snow arch',[(x,y,z+.15) for x,y,z in pts],.08,snow)
mesh('Fanlight',[(0,-D/2-.11,B+2.2)]+[(.7*math.cos(i*math.pi/24),-D/2-.11,B+2.2+.45*math.sin(i*math.pi/24)) for i in range(25)],[(0,i,i+1) for i in range(1,25)],glass)
for i in range(5):cube('Entrance step',(0,-D/2-1.8-i*.32,B-(i+1)*.16),(2.8,1.8+i*.64,.16),stone,.02)
for x in (-1.5,1.5):
 line('Handrail',[(x,-D/2-1,B+1),(x,-D/2-3.7,.7)],.035,dark)
 for j in range(6):line('Rail baluster',[(x,-D/2-1-j*.5,max(.08,B-j*.14)),(x,-D/2-1-j*.5,B+1-j*.14)],.025,dark)
# Curved raised beds, gaps at central stair.
for sign in (-1,1):
 for rad in (2.5,3.6):
  pts=[(sign*(2.5+rad*math.cos(t)),-D/2-.15-rad*.62*math.sin(t),.33) for t in [i*math.pi/40 for i in range(41)]]
  pts=[p for p in pts if abs(p[0])>1.6]
  line('Curved garden brick wall',pts,.18,brick);line('Snow bed coping',[(x,y,z+.2) for x,y,z in pts],.1,snow)
for x in (-6,-4.6,-3.2,3.2,4.6,6):
 sphere('Topiary',(x,-D/2-1.3,.9),(.55,.55,.65),green);sphere('Snow topiary',(x,-D/2-1.3,1.32),(.5,.5,.22),snow)
 if abs(x)==3.2:
  line('Topiary stem',[(x,-D/2-1.3,1),(x,-D/2-1.3,2)],.045,wood);sphere('Topiary crown',(x,-D/2-1.3,2),(.42,.42,.42),green)
cube('Site snow',(0,0,-.13),(45,40,.2),snow);cube('Street',(0,-13,-.02),(45,6,.04),stone)
# Interior hypothesis, partitions with door gaps and stair flights.
for lv in range(2):
 z=B+lv*H
 for x in (-1.35,1.35):
  for ya,yb in ((-D/2+.3,-2.8),(-1.7,1.8),(2.9,D/2-.3)):cube('Hypothetical hall partition',(x,(ya+yb)/2,z+(H-.2)/2),(.15,yb-ya,H-.2),white)
 for sign in (-1,1):cube('Hypothetical room partition',(sign*4.2,1,z+(H-.2)/2),(5.5,.15,H-.2),white)
 for i in range(18):cube('Stair tread',(0,1+i*.22,z+i*H/18), (1.1,.24,.10),wood)
# Camera and separate lighting scenes share all architectural data.
bpy.ops.object.camera_add(location=(23,-32,23));cam=bpy.context.object;cam.name='Reference view';cam.rotation_euler=(Vector((0,-.5,4.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=26;s.camera=cam
s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=1000;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Day sky');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.42,.62,.85,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.45
bpy.ops.object.light_add(type='SUN',location=(0,0,20));sun=bpy.context.object;sun.name='Day sun';sun.data.energy=3;sun.rotation_euler=(.5,-.5,-.4);sun.data.angle=.08
# Day pane emission off. Night gets per-scene material overrides through duplicated panes.
for o in list(s.objects):
 if o.name.startswith('Interior luminous'):o.hide_render=True
night=bpy.data.scenes.new('christmas_night')
for o in s.objects:
 if o==sun:continue
 if o.name.startswith('Interior luminous'):
  copy=o.copy();copy.hide_render=False;night.collection.objects.link(copy)
 else:night.collection.objects.link(o)
night.camera=cam;night.unit_settings.system='METRIC';night.render.engine='CYCLES';night.cycles.samples=32
night.render.resolution_x=night.render.resolution_y=1000;night.render.resolution_percentage=100
night.world=bpy.data.worlds.new('Night sky');night.world.use_nodes=True;night.world.node_tree.nodes['Background'].inputs[0].default_value=(.015,.035,.12,1);night.world.node_tree.nodes['Background'].inputs[1].default_value=.3
for name,loc,energy,col,size in [('Moon',(5,-2,18),1800,(.25,.42,1),15),('Front warm fill',(0,-10,7),900,(1,.48,.18),8)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.color=col;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);o.location=loc;o.rotation_euler=(Vector((0,0,3))-o.location).to_track_quat('-Z','Y').to_euler();night.collection.objects.link(o)
# Festoon bulbs confined to night scene.
bulb=mat('Christmas bulbs',(1,.7,.26),emission=8)
for i in range(70):
 o=sphere('Festoon bulb',(-W/2+i*W/69,-D/2-.2,E),(.065,.065,.065),bulb);s.collection.objects.unlink(o);night.collection.objects.link(o)
# Poster refinement remains a separate reproducible module.
import runpy
runpy.run_path(str(ROOT/'enhance.py'))['enhance'](ROOT)
runpy.run_path(str(ROOT/'detail.py'))['detail'](ROOT)
# Save and render. Architecture objects retained; count provides evidence.
report={'blender':bpy.app.version_string,'objects_day':len(s.objects),'objects_night':len(night.objects),'mesh_vertices':sum(len(o.data.vertices) for o in s.objects if o.type=='MESH'),'dimensions_m':P,'limitations':['Interior and rear invented','No construction certification; provisional stairs','Snow stylized deterministic patches; no physics','Neighborhood and vehicles are conceptual lower-detail models']}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'house.blend'))
render_metrics=[]
for scene in (() if '--no-render' in sys.argv else (s,night)):
 if '--preview' in sys.argv:scene.render.resolution_percentage=40;scene.cycles.samples=12
 scene.render.filepath=str(ROOT/(('preview_' if '--preview' in sys.argv else '')+scene.name+'.png'));t0=time.perf_counter();bpy.ops.render.render(write_still=True,scene=scene.name);render_metrics.append({'scene':scene.name,'seconds':round(time.perf_counter()-t0,3),'samples':scene.cycles.samples,'size':[int(scene.render.resolution_x*scene.render.resolution_percentage/100),int(scene.render.resolution_y*scene.render.resolution_percentage/100)]})

(ROOT/'performance.json').write_text(json.dumps({'blender':bpy.app.version_string,'mode':'preview' if '--preview' in sys.argv else 'no_render' if '--no-render' in sys.argv else 'final','total_seconds':round(time.perf_counter()-BUILD_STARTED,3),'process_peak_rss_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024 if sys.platform=='darwin' else 1024),2),'render_metrics':render_metrics},indent=2))
