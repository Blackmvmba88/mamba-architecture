"""v0.2 poster study. Pure procedural Blender data API, seeded; no external assets.
Can run on the v0.1 file or be invoked by build.py after its two scenes exist.
"""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector, Matrix

def enhance(root):
 root=Path(root);P=json.loads((root/'parameters.json').read_text());day=bpy.data.scenes['winter_day'];night=bpy.data.scenes['christmas_night']
 if day.get('engine_version')=='0.2':return
 rng=random.Random(P['seed']);W=P['width'];D=P['depth'];E=P['base']+2*P['storey'];R=P['roof_rise'];A=W/2+P['overhang'];C=D/2+P['overhang']
 groups={}
 for label in ('01 Casa editable','02 Nieve','03 Jardines','04 Arboles','05 Vecindario conceptual','06 Calle y vehiculos','07 Navidad solo noche'):
  col=bpy.data.collections.new(label);groups[label]=col
  (night if label.startswith('07') else day).collection.children.link(col)
  if not label.startswith('07'):night.collection.children.link(col)
 # Organize all existing architecture into one shared editable collection.
 for o in list(day.collection.objects):
  if o.type in ('CAMERA','LIGHT') or o.name.startswith('Interior luminous'):continue
  target=groups['02 Nieve'] if o.name.startswith(('Snow','Site snow')) else groups['03 Jardines'] if o.name.startswith(('Topiary','Curved garden')) else groups['01 Casa editable'];target.objects.link(o);day.collection.objects.unlink(o)
  if night.collection.objects.get(o.name):night.collection.objects.unlink(o)
 def material(name,color,rough=.6,emit=0):
  m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
  if emit:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emit
  return m
 snow=bpy.data.materials['Snow'];white=bpy.data.materials['Paint ivory'];brick=bpy.data.materials['Brick fired red'];green=bpy.data.materials['Winter shrubs'];dark=bpy.data.materials['Shutters forest black'];roof=bpy.data.materials['Slate brown'];wood=bpy.data.materials['Door walnut'];glass=bpy.data.materials['Glazing blue']
 bark=material('Tree bark muted brown',(.035,.026,.02));red=material('Wreath ribbon burgundy',(.28,.015,.02));road=material('Wet winter asphalt',(.095,.13,.15),.24);sage=material('Neighbor sage clapboard',(.25,.36,.28));cream=material('Neighbor cream',(.52,.48,.37));churchmat=material('Church muted sandstone',(.38,.24,.19));bulb=material('Ivory fairy lights',(1,.73,.35),.3,18);carpaint=material('Car red lacquer',(.38,.018,.012),.22);vanpaint=material('Van faded teal',(.12,.31,.31),.36);rubber=material('Tire rubber',(.018,.019,.022),.8)
 def mesh(name,verts,faces,mat,group='01 Casa editable'):
  me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();me.materials.append(mat);o=bpy.data.objects.new(name,me);groups[group].objects.link(o);o['source']='visual reference guided; dimensions inferred';return o
 def box(name,loc,size,mat,group='01 Casa editable',bevel=0):
  v=[(loc[0]+x*size[0]/2,loc[1]+y*size[1]/2,loc[2]+z*size[2]/2) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))];o=mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],mat,group)
  if bevel:m=o.modifiers.new('Soft edge','BEVEL');m.width=bevel;m.segments=2
  return o
 def curve(name,pts,r,mat,group='01 Casa editable'):
  cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
  for p,v in zip(sp.points,pts):p.co=(*v,1)
  o=bpy.data.objects.new(name,cu);groups[group].objects.link(o);cu.materials.append(mat);return o
 spherecache={}
 def ball(name,loc,r,mat,group='03 Jardines'):
  key=mat.name
  if key not in spherecache:
   verts=[];faces=[];n=10;k=6
   for j in range(k+1):
    t=math.pi*j/k
    for i in range(n):a=2*math.pi*i/n;verts.append((math.sin(t)*math.cos(a),math.sin(t)*math.sin(a),math.cos(t)))
   for j in range(k):
    for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
   me=bpy.data.meshes.new('Shared sphere '+key);me.from_pydata(verts,[],faces);me.materials.append(mat)
   for p in me.polygons:p.use_smooth=True
   spherecache[key]=me
  o=bpy.data.objects.new(name,spherecache[key]);groups[group].objects.link(o);o.location=loc;o.scale=r if isinstance(r,tuple) else (r,r,r);return o
 def roofz(x,y):return E+R*max(0,min((A-abs(x))/C,(C-abs(y))/C))
 # Smooth coherent snow strips. No per-tile white squares; thickness at edge.
 for name in ('Snow patches roof',):
  if bpy.data.objects.get(name):bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
 for sign in (-1,1):
  vv=[];ff=[];nx=170;ny=12
  for i in range(nx+1):
   x=-A+2*A*i/nx;edge=.8+.5*math.sin(x*.65)+.25*math.sin(x*2.3)
   for j in range(ny+1):
    y=sign*(C-edge*j/ny);vv.append((x,y,roofz(x,y)+.09+.015*math.sin(x*2+y)))
  for i in range(nx):
   for j in range(ny):a=i*(ny+1)+j;ff.append((a,a+ny+1,a+ny+2,a+1))
  o=mesh('Drift along roof eave',vv,ff,snow,'02 Nieve');mod=o.modifiers.new('Snow thickness','SOLIDIFY');mod.thickness=.07
 # Snow along hips and ridge, variable radius-like ribbons.
 for sx in (-1,1):
  for sy in (-1,1):
   pts=[(sx*(A-C*t),sy*(C*(1-t)),E+R*t+.12) for t in [i/45 for i in range(46)]];curve('Hip snow drift',pts,.2,snow,'02 Nieve')
 curve('Ridge snow drift',[(-A+C,0,E+R+.1),(A-C,0,E+R+.1)],.2,snow,'02 Nieve')
 # Dormer roof framing and snowfall.
 for x in P['dormer_axes']:
  y=-3.25;z=roofz(x,y)
  for sign in (-1,1):
   curve('Dormer rake moulding',[(x+sign*.98,y-1.10,z+1.5),(x,y-1.10,z+2.25)],.055,white)
   curve('Dormer snow rake',[(x+sign*.98,y-1.1,z+1.57),(x,y-1.1,z+2.32)],.085,snow,'02 Nieve')
  box('Dormer apron',(x,y-1.02,z+.03),(1.9,.23,.15),white,bevel=.025)
 # Window brick lintels and corners, physical relief confined to important edges.
 for lv in range(2):
  for x in P['window_axes']:
   z=P['base']+lv*P['storey']+.5+P['window_height']+.10
   for j in range(9):box('Soldier brick lintel',(x+(j-4)*.15,-D/2-.035,z),(.135,.11,.22),brick)
 # Broader portico canopy with layered curved surfaces matching poster's arch silhouette.
 for rad,depth in ((1.23,.26),(1.38,.28)):
  pts=[(rad*math.cos(t),-D/2-.62,P['base']+2.35+.73*math.sin(t)) for t in [i*math.pi/64 for i in range(65)]];curve('Layered portico cornice',pts,.095,white)
 vv=[];ff=[]
 for i in range(65):
  t=i*math.pi/64
  for y in (-D/2-.92,-D/2+.1):vv.append((1.39*math.cos(t),y,P['base']+2.35+.8*math.sin(t)+.18))
 for i in range(64):a=i*2;ff.append((a,a+2,a+3,a+1))
 mesh('Curved entrance snow canopy',vv,ff,snow,'02 Nieve')
 # Fanlight rays, wreath foliage and bow.
 for i in range(7):
  t=i*math.pi/6;curve('Fanlight radial bar',[(0,-D/2-.145,P['base']+2.2),(.7*math.cos(t),-D/2-.145,P['base']+2.2+.45*math.sin(t))],.017,white)
 for i in range(30):
  t=i*math.tau/30;ball('Door wreath',(math.cos(t)*.30,-D/2-.15,P['base']+1.35+math.sin(t)*.30),.105,green)
 box('Wreath bow knot',(0,-D/2-.28,P['base']+1.12),(.14,.08,.12),red)
 for sign in (-1,1):
  ball('Bow loop',(sign*.13,-D/2-.28,P['base']+1.14),(.14,.07,.09),red);box('Ribbon tail',(sign*.06,-D/2-.25,P['base']+.97),(.085,.05,.23),red)
 # Garden wall is solid raised masonry instead of rounded pipe.
 for o in list(bpy.data.objects):
  if o.name.startswith(('Curved garden brick wall','Snow bed coping')):bpy.data.objects.remove(o,do_unlink=True)
 for sign in (-1,1):
  for rad,height in ((2.5,.65),(3.6,.30)):
   vv=[];ff=[];steps=72
   for i in range(steps+1):
    t=math.pi*i/steps;x=sign*(2.5+rad*math.cos(t));y=-D/2-.15-rad*.62*math.sin(t)
    for dr,z in ((-.12,0),(.12,0),(.12,height),(-.12,height)):vv.append((sign*(2.5+(rad+dr)*math.cos(t)),-D/2-.15-(rad+dr)*.62*math.sin(t),z))
   for i in range(steps):
    if abs(vv[i*4][0])<1.75 or abs(vv[(i+1)*4][0])<1.75:continue
    a=4*i
    for j in range(4):ff.append((a+j,a+(j+1)%4,a+4+(j+1)%4,a+4+j))
   mesh('Solid terraced garden wall',vv,ff,brick,'03 Jardines')
   pts=[(sign*(2.5+rad*math.cos(i*math.pi/72)),-D/2-.15-rad*.62*math.sin(i*math.pi/72),height+.04) for i in range(73)]
   # Keep separate arcs to avoid bridging stairs.
   segment=[]
   for pt in pts:
    if abs(pt[0])>1.75:segment.append(pt)
    elif len(segment)>1:curve('Snow wall coping',segment,.105,snow,'02 Nieve');segment=[]
   if len(segment)>1:curve('Snow wall coping',segment,.105,snow,'02 Nieve')
 # Shrub foliage clusters, clustered linked mesh instances instead of high-poly uniques.
 for x in (-6,-4.6,-3.2,3.2,4.6,6):
  for i in range(32):
   a=rng.uniform(0,math.tau);t=rng.uniform(-1,1);rr=.45*math.sqrt(1-t*t);loc=(x+rr*math.cos(a),-D/2-1.3+rr*math.sin(a),.95+t*.45)
   ball('Shrub foliage cluster',loc,rng.uniform(.09,.16),green)
 for sign in (-1,1):
  for i in range(15):
   t=.22+i*.17;x=sign*(2.5+3.1*math.cos(t));y=-D/2-.15-1.95*math.sin(t)
   if abs(x)<1.9:continue
   ball('Lower border shrub',(x,y,.44),(.26,.26,.29),green);ball('Border snow cap',(x,y,.65),(.23,.23,.09),snow,'02 Nieve')
 # Bare foreground trees: tapered trunk and branch tubes, asymmetric deterministic skeletons.
 def tree(tx,ty,height,seed):
  rr=random.Random(seed);parts=[]
  def branch(start,vec,radius,depth):
   end=Vector(start)+Vector(vec);mid=Vector(start)+Vector(vec)*.48+Vector((rr.uniform(-.3,.3),rr.uniform(-.3,.3),.1))
   cu=bpy.data.curves.new('Branch','CURVE');cu.dimensions='3D';cu.bevel_depth=radius;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(2)
   for p,v,rad in zip(sp.points,(start,mid,end),(1,.72,.32)):p.co=(*v,1);p.radius=rad
   o=bpy.data.objects.new('Bare tree branch',cu);groups['04 Arboles'].objects.link(o);cu.materials.append(bark);parts.append(o)
   if depth:
    for j in range(2 if depth<3 else 3):
     ang=rr.uniform(0,math.tau);length=Vector(vec).length*rr.uniform(.5,.72);nv=(math.cos(ang)*length*.7,math.sin(ang)*length*.55,length*.6);branch(end,nv,radius*.48,depth-1)
  branch(Vector((tx,ty,0)),Vector((.3,0,height*.5)),.31,3)
  for j in range(7):
   a=rr.uniform(0,math.tau);branch(Vector((tx+.1,ty,height*(.25+j*.08))),Vector((math.cos(a)*height*.36,math.sin(a)*height*.28,height*.23)),.10,2)
  rootobj=bpy.data.objects.new('MOVER Arbol '+str(seed),None);groups['04 Arboles'].objects.link(rootobj);rootobj.location=(tx,ty,0);rootobj.empty_display_type='PLAIN_AXES'
  for o in parts:o.parent=rootobj;o.matrix_parent_inverse=Matrix.Translation(Vector((-tx,-ty,0)))
  return parts
 tree(-9,-6.3,13,91);tree(9,-3.7,12,92);tree(-12,8,10,93)
 # Wet street and irregular ground snow boundary.
 old=bpy.data.objects.get('Street')
 if old:bpy.data.objects.remove(old,do_unlink=True)
 box('Winter road',(0,-14,-.015),(52,8,.05),road,'06 Calle y vehiculos')
 box('Driveway',(0,-9,-.005),(19,6,.06),road,'06 Calle y vehiculos')
 for side in (-1,1):
  vv=[];ff=[]
  for i in range(110):
   x=-25+i*50/109;y=-14+side*(3.8+.35*math.sin(x*.85)+.18*math.sin(x*2.7));vv.extend([(x,y,.045),(x,-14+side*5.0,.045)])
  for i in range(109):a=i*2;ff.append((a,a+2,a+3,a+1))
  mesh('Roadside snow drift',vv,ff,snow,'02 Nieve')
 # Neighbor massing is explicitly lower detail; church anchors the upper right of composition.
 def neighbor(x,y,w,d,h,mat):
  box('Context house',(x,y,h/2),(w,d,h),mat,'05 Vecindario conceptual')
  v=[(x-w/2-.3,y-d/2-.3,h),(x+w/2+.3,y-d/2-.3,h),(x+w/2+.3,y+d/2+.3,h),(x-w/2-.3,y+d/2+.3,h),(x,y-d/2-.3,h+2.6),(x,y+d/2+.3,h+2.6)]
  mesh('Context gable roof',v,[(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)],roof,'05 Vecindario conceptual')
  curve('Context snowy ridge',[(x,y-d/2-.3,h+2.7),(x,y+d/2+.3,h+2.7)],.18,snow,'02 Nieve')
  for lv in range(2):
   for wx in (-w*.28,w*.28):
    box('Context front window',(x+wx,y-d/2-.035,1.6+lv*2.5),(1,.07,1.5),glass,'05 Vecindario conceptual')
    for sign in (-1,1):box('Context window trim',(x+wx+sign*.54,y-d/2-.08,1.6+lv*2.5),(.08,.1,1.62),white,'05 Vecindario conceptual')
    box('Context sash',(x+wx,y-d/2-.09,1.6+lv*2.5),(.05,.09,1.5),white,'05 Vecindario conceptual')
 for args in [(-12,12,8,9,6.5,cream),(0,15,8,9,7,sage),(12,11,7,10,7,cream),(-19,24,8,9,6,sage),(1,29,9,10,7,cream),(18,28,8,10,6,sage)]:neighbor(*args)
 cx,cy=15,26
 box('Church nave',(cx,cy,4),(7,14,8),churchmat,'05 Vecindario conceptual')
 mesh('Church pitched roof',[(cx-4,cy-7.5,8),(cx,cy-7.5,12),(cx+4,cy-7.5,8),(cx-4,cy+7.5,8),(cx,cy+7.5,12),(cx+4,cy+7.5,8)],[(0,1,4,3),(1,2,5,4)],roof,'05 Vecindario conceptual')
 box('Church tower',(cx,cy-7,10),(4.4,4.4,20),churchmat,'05 Vecindario conceptual')
 for sign in (-1,1):
  for xx in (-1.9,1.9):box('Church tower buttress',(cx+xx,cy-7+sign*1.9,10.8),(.45,.45,21.6),churchmat,'05 Vecindario conceptual')
 for dx in (-.8,.8):
  box('Church lancet dark recess',(cx+dx,cy-9.23,15),(.9,.12,5),dark,'05 Vecindario conceptual')
  curve('Gothic lancet stone trim',[(cx+dx-.5,cy-9.32,12.5),(cx+dx-.5,cy-9.32,17),(cx+dx,cy-9.32,18),(cx+dx+.5,cy-9.32,17),(cx+dx+.5,cy-9.32,12.5)],.075,white,'05 Vecindario conceptual')
 for i in range(5):box('Tower crenellation',(cx-1.8+i*.9,cy-9.2,20.4),(.5,.45,.8),churchmat,'05 Vecindario conceptual')
 # Keep background church a contextual silhouette and frame its complete tower.
 for o in groups['05 Vecindario conceptual'].objects:
  if o.name.startswith(('Church','Gothic','Tower')):
   for v in (o.data.vertices if o.type=='MESH' else [p for spline in o.data.splines for p in spline.points]):
    v.co.x=cx+(v.co.x-cx)*.76;v.co.y=cy+(v.co.y-cy)*.76;v.co.z*=.66
 # Procedural clapboard and slate detail use shaders rather than extra objects.
 for mat in (sage,cream):
  n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');wave=n.new('ShaderNodeMath');wave.operation='MULTIPLY';wave.inputs[1].default_value=40;sin=n.new('ShaderNodeMath');sin.operation='SINE';bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.2;bump.inputs['Distance'].default_value=.012;l.new(geo.outputs['Position'],sep.inputs[0]);l.new(sep.outputs['Z'],wave.inputs[0]);l.new(wave.outputs[0],sin.inputs[0]);l.new(sin.outputs[0],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 # Foreground lamps, simple recognizable editable vehicles.
 for x in (-10,10):
  curve('Streetlamp post',[(x,-14,0),(x,-14,2.4)],.055,dark,'06 Calle y vehiculos');box('Lantern',(x,-14,2.6),(.3,.3,.42),white,'06 Calle y vehiculos');box('Lantern cap',(x,-14,2.87),(.42,.42,.1),dark,'06 Calle y vehiculos')
  ball('Lantern luminous core',(x,-14,2.6),.11,bulb,'07 Navidad solo noche')
 def vehicle(x,y,isvan):
  existing=set(groups['06 Calle y vehiculos'].objects);ma=vanpaint if isvan else carpaint;length=4.8 if isvan else 3.8;width=1.9
  box('Van body' if isvan else 'Red car body',(x,y,.8),(length,width,1.15 if isvan else .65),ma,'06 Calle y vehiculos',.12)
  box('Van cabin' if isvan else 'Red car cabin',(x-.1,y,1.6 if isvan else 1.3),(length*.68,width*.9,1.1 if isvan else .75),ma,'06 Calle y vehiculos',.09)
  for sign in (-1,1):
   box('Vehicle side glazing',(x-.1,y+sign*(width*.455),1.75 if isvan else 1.43),(length*.55,.025,.55),glass,'06 Calle y vehiculos')
   for wx in (-length*.32,length*.32):ball('Vehicle wheel',(x+wx,y+sign*width/2,.46),(.39,.13,.39),rubber,'06 Calle y vehiculos')
  box('Vehicle bumper',(x+length/2+.02,y,.58),(.1,width,.12),white,'06 Calle y vehiculos')
  if isvan:
   for yy in (-.45,.45):curve('Van roof rack',[(x-2, y+yy,2.25),(x+1.7,y+yy,2.25)],.035,dark,'06 Calle y vehiculos')
  rootobj=bpy.data.objects.new('MOVER Camioneta' if isvan else 'MOVER Auto rojo',None);groups['06 Calle y vehiculos'].objects.link(rootobj);rootobj.location=(x,y,0);rootobj.empty_display_type='PLAIN_AXES'
  for o in list(groups['06 Calle y vehiculos'].objects):
   if o not in existing and o!=rootobj:o.parent=rootobj;o.matrix_parent_inverse=Matrix.Translation(Vector((-x,-y,0)))
 vehicle(2,-10.5,False);vehicle(-8,-16.0,True)
 # Night decorations follow trim, not embedded inside cornice.
 for o in list(bpy.data.objects):
  if o.name.startswith('Festoon bulb'):bpy.data.objects.remove(o,do_unlink=True)
 for i in range(82):ball('Eave fairy light',(-W/2+i*W/81,-D/2-.32,E-.08),.048,bulb,'07 Navidad solo noche')
 for lv in range(2):
  for x in P['window_axes']:
   z=P['base']+lv*P['storey']+.5
   pts=[]
   for i in range(19):
    t=i/18
    if t<.33:xx=x-P['window_width']/2-.08;zz=z+2*t/.33
    elif t<.66:xx=x-P['window_width']/2-.08+(P['window_width']+.16)*(t-.33)/.33;zz=z+2
    else:xx=x+P['window_width']/2+.08;zz=z+2*(1-(t-.66)/.34)
    pts.append((xx,-D/2-.22,zz));ball('Window fairy light',pts[-1],.04,bulb,'07 Navidad solo noche')
   curve('Window light cable',pts,.009,dark,'07 Navidad solo noche')
 # Shrub and trunk fairy lights add the festive points visible in the reference.
 for x in (-6,-4.6,-3.2,3.2,4.6,6):
  for i in range(14):
   t=i*math.tau/14;ball('Shrub fairy light',(x+.49*math.cos(t),-D/2-1.3+.49*math.sin(t),1.02+.12*math.sin(t*3)),.036,bulb,'07 Navidad solo noche')
 for tx,ty in ((-9,-6.3),(9,-3.7)):
  pts=[]
  for i in range(50):
   t=i*.45;pt=(tx+.33*math.cos(t),ty+.33*math.sin(t),.5+i*.08);pts.append(pt);lamp=ball('Tree trunk fairy light',pt,.028,bulb,'07 Navidad solo noche');lamp.parent=bpy.data.objects['MOVER Arbol '+('91' if tx<0 else '92')];lamp.matrix_parent_inverse=Matrix.Translation(Vector((-tx,-ty,0)))
  cable=curve('Tree light string',pts,.008,dark,'07 Navidad solo noche');cable.parent=bpy.data.objects['MOVER Arbol '+('91' if tx<0 else '92')];cable.matrix_parent_inverse=Matrix.Translation(Vector((-tx,-ty,0)))
 # Context roof shader supplies slate courses and irregular snow, no texture downloads.
 n=roof.node_tree.nodes;l=roof.node_tree.links;ps=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=.7;noise.inputs['Detail'].default_value=3;l.new(geo.outputs['Position'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.54;ramp.color_ramp.elements[0].color=(.045,.035,.026,1);ramp.color_ramp.elements[1].position=.65;ramp.color_ramp.elements[1].color=(.8,.88,.96,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],ps.inputs['Base Color']);fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=25;l.new(geo.outputs['Position'],fine.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.25;bump.inputs['Distance'].default_value=.012;l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],ps.inputs['Normal'])
 # Accessible movement handles; all transforms shared across both scenes.
 handle=bpy.data.objects.new('MOVER CASA COMPLETA',None);groups['01 Casa editable'].objects.link(handle);handle.empty_display_type='CUBE';handle.empty_display_size=1
 for o in list(groups['01 Casa editable'].objects):
  if o!=handle:o.parent=handle
 for scene in (day,night):
  for o in scene.objects:
   if o.name.startswith(('Interior luminous','Door wreath','Bow loop','Ribbon tail','Snow arch','Drift along roof eave','Hip snow drift','Ridge snow drift','Dormer snow','Curved entrance snow','Eave fairy light','Window fairy light','Window light cable')):o.parent=handle
 # Recenter unique mesh origins for sensible individual rotations.
 for col in groups.values():
  for o in col.objects:
   if o.type=='MESH' and o.data.users==1 and len(o.data.vertices):
    center=sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)
    for v in o.data.vertices:v.co-=center
    o.location+=center
 # Lighting and cinematic portrait composition; shared camera remains user editable.
 cam=day.camera;cam.location=P.get('camera_location',[-27,-47,34]);cam.rotation_euler=(Vector(P.get('camera_target',[0,5,6.5]))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=P.get('camera_ortho_scale',38)
 bpy.data.objects['Front warm fill'].data.energy=450;bpy.data.objects['Front warm fill'].data.color=(1,.64,.38)
 bpy.data.objects['Moon'].data.energy=2500;bpy.data.objects['Moon'].data.color=(.22,.36,1)
 for scene in (day,night):
  scene['engine_version']='0.2';scene['editing']='Shared architecture collections; save manual edits as a separate .blend before regeneration.';scene.render.resolution_x=P.get('render_width',1050);scene.render.resolution_y=P.get('render_height',1500);scene.render.resolution_percentage=100;scene.cycles.samples=P.get('render_samples',32);scene.cycles.use_denoising=True
  tree=bpy.data.node_groups.new(scene.name+' compositor','CompositorNodeTree');scene.compositing_node_group=tree;tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');nodes=tree.nodes;rl=nodes.new('CompositorNodeRLayers');rl.scene=scene;out=nodes.new('NodeGroupOutput')
  if scene==night:
   glow=nodes.new('CompositorNodeGlare');glow.inputs['Type'].default_value='Fog Glow';glow.inputs['Quality'].default_value='Medium';glow.inputs['Threshold'].default_value=1.8;glow.inputs['Strength'].default_value=.25;tree.links.new(rl.outputs['Image'],glow.inputs['Image']);tree.links.new(glow.outputs['Image'],out.inputs['Image'])
  else:tree.links.new(rl.outputs['Image'],out.inputs['Image'])
 (root/'enhancement.json').write_text(json.dumps({'version':'0.2','seed':P['seed'],'main_dimensions_unchanged':True,'shared_architecture':True,'reference_guided':['portrait camera from left','bare trees','terraced garden','arch canopy','coherent snow','window fairy lights','church silhouette','red car and teal van'],'inferred':['all sizes','neighborhood positions','vehicle proportions','tree branching'],'limits':['vehicles and neighborhood are simplified blockouts','no people or proprietary illustration textures','no exact photo match']},indent=2))

if __name__=='__main__':
 import sys
 root=Path(__file__).resolve().parent;enhance(root);bpy.ops.wm.save_as_mainfile(filepath=str(root/'house.blend'))
 preview='--preview' in sys.argv
 for scene in bpy.data.scenes:
  if preview:scene.render.resolution_percentage=40;scene.cycles.samples=12
  scene.render.filepath=str(root/(('preview_' if preview else '')+scene.name+'.png'));bpy.ops.render.render(write_still=True,scene=scene.name)
