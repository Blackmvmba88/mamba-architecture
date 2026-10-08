"""v0.3 reference-guided detail, editable data API geometry and local assets only."""
import bpy,math,random,json,bmesh
from pathlib import Path
from mathutils import Vector

def world_pose(obj):
 # Scene-independent for this generator's un-constrained object hierarchy.
 return world_pose(obj.parent) @ obj.matrix_parent_inverse @ obj.matrix_basis if obj.parent else obj.matrix_basis

def geometry_points(obj):
 matrix=world_pose(obj)
 if obj.type=='MESH':return [matrix@v.co for v in obj.data.vertices]
 if obj.type=='CURVE':
  points=[]
  for spline in obj.data.splines:
   if spline.type=='BEZIER':
    for index,p in enumerate(spline.bezier_points):
     controls=[p.co]
     if index>0 or spline.use_cyclic_u:controls.append(p.handle_left)
     if index<len(spline.bezier_points)-1 or spline.use_cyclic_u:controls.append(p.handle_right)
     for co in controls:
      rad=obj.data.bevel_depth*p.radius
      for delta in ((rad,0,0),(-rad,0,0),(0,rad,0),(0,-rad,0),(0,0,rad),(0,0,-rad)):points.append(matrix@(co+Vector(delta)))
   else:
    for p in spline.points:
     rad=obj.data.bevel_depth*p.radius
     for delta in ((rad,0,0),(-rad,0,0),(0,rad,0),(0,-rad,0),(0,0,rad),(0,0,-rad)):points.append(matrix@(Vector(p.co[:3])+Vector(delta)))
  return points
 return []

def export_modules(root,P):
 bpy.context.view_layer.update()
 modules=[]
 roots=[(bpy.data.objects['MOVER CASA COMPLETA'],'residence'),(bpy.data.objects['MOVER Auto rojo'],'vehicle'),(bpy.data.objects['MOVER Camioneta'],'vehicle')]+[(o,'tree') for o in bpy.data.objects if o.name.startswith('MOVER Arbol')]
 for handle,kind in roots:
  points=[p for o in handle.children_recursive for p in geometry_points(o)]
  dimensions=[max(p[i] for p in points)-min(p[i] for p in points) for i in range(3)]
  entry={'id':handle.name,'kind':kind,'version':'0.3','origin':list(handle.location),'dimensions_m':dimensions,'bounds_method':'editable mesh vertices and conservative curve control hulls with bevel radius, in world axes; scene-independent parent transforms','anchors':{'origin':[0,0,0]},'materials':sorted({m.name for o in handle.children_recursive if o.type in ('MESH','CURVE') for m in o.data.materials if m}),'lod':'conceptual_detail','dependencies':[],'evidence':'illustration guided; dimensions inferred'};modules.append(entry);handle['module_id']=entry['id'];handle['module_version']='0.3'
 (Path(root)/'modules.json').write_text(json.dumps(modules,indent=2,ensure_ascii=False))


def detail(root):
 root=Path(root);day=bpy.data.scenes['winter_day'];night=bpy.data.scenes['christmas_night'];P=json.loads((root/'parameters.json').read_text());rng=random.Random(P['seed']+300)
 if day.get('engine_version')=='0.3':return
 def mat(name,color,rough=.5,emit=0):
  m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1);p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
  if emit:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emit
  return m
 steel=mat('v03 brushed metal',(.22,.25,.27),.28);rubber=bpy.data.materials['Tire rubber'];glass=mat('v03 vehicle smoked glazing',(.018,.055,.07),.12);glass.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value=.25
 black=bpy.data.materials['Shutters forest black'];white=bpy.data.materials['Paint ivory'];carpaint=bpy.data.materials['Car red lacquer'];vanpaint=bpy.data.materials['Van faded teal'];snow=bpy.data.materials['Snow'];road=bpy.data.materials['Wet winter asphalt'];stone=bpy.data.materials['Limestone'];wood=bpy.data.materials['Tree bark muted brown'];light=mat('v03 warm lamp',(1,.65,.26),.3,6);rear=mat('v03 rear red lens',(.5,.01,.005),.2,1)
 vehiclecol=bpy.data.collections['06 Calle y vehiculos'];treecol=bpy.data.collections['04 Arboles'];nightcol=bpy.data.collections['07 Navidad solo noche'];snowcol=bpy.data.collections['02 Nieve']
 def mesh(name,v,f,ma,col,parent=None):
  me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();me.materials.append(ma);o=bpy.data.objects.new(name,me);col.objects.link(o);o.parent=parent;o['source']='inferred v0.3 editable detail';return o
 def box(name,loc,size,ma,col,parent=None,bevel=.015):
  v=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in ((-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1))];o=mesh(name,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],ma,col,parent);o.location=loc
  if bevel:m=o.modifiers.new('Small rounded edges','BEVEL');m.width=bevel;m.segments=3
  return o
 def curve(name,pts,r,ma,col,parent=None):
  cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
  for p,co in zip(sp.bezier_points,pts):p.co=co;p.handle_left_type=p.handle_right_type='AUTO'
  o=bpy.data.objects.new(name,cu);col.objects.link(o);cu.materials.append(ma);o.parent=parent;return o
 def extrude(name,profile,width,ma,col,parent=None,bevel=.04):
  v=[(x,y,z) for y in (-width/2,width/2) for x,z in profile];n=len(profile);f=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];o=mesh(name,v,f,ma,col,parent)
  if bevel:m=o.modifiers.new('Body edge rounding','BEVEL');m.width=bevel;m.segments=3
  return o
 def wheel(name,x,y,z,radius,ma,parent):
  v=[];f=[];N=40
  # Ring cross-section, visible sidewall and rolling surface.
  profile=[(-.12,radius*.73),(-.15,radius*.88),(-.11,radius),( .11,radius),(.15,radius*.88),(.12,radius*.73)]
  for dy,rr in profile:
   for i in range(N):a=i*math.tau/N;v.append((x+rr*math.sin(a),y+dy,z+rr*math.cos(a)))
  for j in range(len(profile)-1):
   for i in range(N):a=j*N+i;b=j*N+(i+1)%N;f.append((a,b,b+N,a+N))
  o=mesh(name,v,f,ma,vehiclecol,parent)
  for p in o.data.polygons:p.use_smooth=True
 def rim(x,y,z,r,parent):
  N=32;v=[(x,y,z)]+[(x+r*math.sin(i*math.tau/N),y,z+r*math.cos(i*math.tau/N)) for i in range(N)];mesh('v03 alloy wheel hub',v,[(0,i+1,(i+1)%N+1) for i in range(N)],steel,vehiclecol,parent)
  for i in range(6):
   a=i*math.tau/6;curve('v03 hub spoke',[(x,y-.012,z),(x+r*.8*math.sin(a),y-.012,z+r*.8*math.cos(a))],.021,white,vehiclecol,parent)
 # Correct physical brick coordinates: X/Z on front and rear, Y/Z on sides.
 brick=bpy.data.materials['Brick fired red'];n=brick.node_tree.nodes;l=brick.node_tree.links;geo=next(q for q in n if q.bl_idname=='ShaderNodeNewGeometry');pos=n.new('ShaderNodeSeparateXYZ');normal=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],pos.inputs[0]);l.new(geo.outputs['Normal'],normal.inputs[0]);ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(normal.outputs['X'],ab.inputs[0]);test=n.new('ShaderNodeMath');test.operation='GREATER_THAN';test.inputs[1].default_value=.5;l.new(ab.outputs[0],test.inputs[0]);mix=n.new('ShaderNodeMixRGB');l.new(test.outputs[0],mix.inputs[0])
 for key,slot in (('X',1),('Y',2)):
  c=n.new('ShaderNodeCombineXYZ');l.new(pos.outputs[key],c.inputs['X']);l.new(pos.outputs['Z'],c.inputs['Y']);l.new(c.outputs[0],mix.inputs[slot])
 tex=next(q for q in n if q.bl_idname=='ShaderNodeTexBrick');l.new(mix.outputs[0],tex.inputs['Vector'])
 # Vehicles retained at original handles and approximate proportions.
 for handle,isvan in ((bpy.data.objects['MOVER Auto rojo'],False),(bpy.data.objects['MOVER Camioneta'],True)):
  handle.location=P.get('van_location',[-8,-16,0]) if isvan else P.get('car_location',[3.8,-10.5,0])
  for o in list(handle.children):bpy.data.objects.remove(o,do_unlink=True)
  L=4.8 if isvan else 3.9;w=1.92;r=.37 if isvan else .34;wheelz=r+(.012 if isvan else .027);front=L*.31;back=-L*.31;ma=vanpaint if isvan else carpaint
  if isvan:
   body=[(-L/2,.55),(-L/2,2.13),(L*.18,2.13),(L/2,1.63),(L/2,.55)]
   bodyobj=extrude('v03 van body',body,w,ma,vehiclecol,handle,.08)
   # Sloped windshield and inset glazing, front = +X.
   mesh('v03 van windscreen',[(L*.19,-.77,2.08),(L*.19,.77,2.08),(L/2-.03,.77,1.68),(L/2-.03,-.77,1.68)],[(0,1,2,3)],glass,vehiclecol,handle)
   for sign in (-1,1):
    yy=sign*(w/2+.012)
    mesh('v03 van cab side window',[(.3,yy,1.32),(.3,yy,2.01),(.87,yy,2.01),(1.95,yy,1.62),(1.95,yy,1.32)],[(0,1,2,3,4)],glass,vehiclecol,handle)
    box('v03 van cargo glazing',(-1.0,yy,1.68),(1.7,.022,.53),glass,vehiclecol,handle)
    curve('v03 van door seam',[(.2,yy,.68),(.2,yy,2.06)],.01,black,vehiclecol,handle)
    box('v03 van door handle',(.6,yy+sign*.035,1.19),(.23,.045,.045),steel,vehiclecol,handle)
    for y in (-.55,.55):curve('v03 roof rack rail',[(-2.1,y,2.22),(1,y,2.22)],.03,steel,vehiclecol,handle)
   for xx in (-1.8,-.6,.7):box('v03 roof rack crossbar',(xx,0,2.24),(.04,1.4,.05),steel,vehiclecol,handle)
   for yy in (-.3,.05,.34):curve('v03 carried pipe',[(-2.1,yy,2.34),(1.15,yy,2.34)],.05,steel,vehiclecol,handle)
  else:
   bodyobj=extrude('v03 red car body',[(-1.95,.52),(-1.88,.96),(-1.2,1.03),(.90,1.03),(1.91,.90),(1.95,.53)],w,ma,vehiclecol,handle,.07)
   extrude('v03 car cabin',[(-1.2,.98),(-.82,1.66),(.3,1.66),(.94,1.0)],w*.91,ma,vehiclecol,handle,.045)
   for sign in (-1,1):
    yy=sign*(w*.455+.008)
    for pts in [[(-1.06,yy,1.07),(-.75,yy,1.58),(-.2,yy,1.58),(-.2,yy,1.07)],[(-.13,yy,1.07),(-.13,yy,1.58),(.24,yy,1.58),(.78,yy,1.07)]]:mesh('v03 car side glazing',pts,[(0,1,2,3)],glass,vehiclecol,handle)
    curve('v03 car door seam',[(-.16,sign*(w/2+.009),.60),(-.16,sign*(w/2+.009),1.02)],.01,black,vehiclecol,handle)
    box('v03 car handle',(.1,sign*(w/2+.028),.89),(.19,.04,.04),steel,vehiclecol,handle)
   mesh('v03 car windscreen',[(.31,-.77,1.63),(.31,.77,1.63),(.90,.77,1.05),(.90,-.77,1.05)],[(0,1,2,3)],glass,vehiclecol,handle)
   mesh('v03 car rear glass',[(-.83,-.77,1.63),(-1.16,-.77,1.06),(-1.16,.77,1.06),(-.83,.77,1.63)],[(0,1,2,3)],glass,vehiclecol,handle)
  # Actual wheel arches in bodywork, before the bevel to avoid modifier-order artefacts.
  for modifier in list(bodyobj.modifiers):bodyobj.modifiers.remove(modifier)
  for xx in (front,back):
   v=[];f=[];N=40;radius=r+.045
   for yy in (-1.3,1.3):
    for i in range(N):a=i*math.tau/N;v.append((xx+radius*math.sin(a),yy,wheelz+radius*math.cos(a)))
   f=[tuple(range(N-1,-1,-1)),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
   cut=mesh('Wheel arch cutter',v,f,black,vehiclecol,handle);bpy.context.view_layer.update();mod=bodyobj.modifiers.new('Wheel arch opening','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=bodyobj;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
  mod=bodyobj.modifiers.new('Body edge rounding','BEVEL');mod.width=.055;mod.segments=3
  # Separate wheels at ground contact, rims, mirrors, plates and lamps.
  for xx in (front,back):
   for sign in (-1,1):wheel('v03 tire',xx,sign*(w/2-.02),wheelz,r,rubber,handle);rim(xx,sign*(w/2+.135),wheelz,r*.60,handle)
  for sign in (-1,1):
   box('v03 mirror',(.72 if not isvan else 1.45,sign*(w/2+.13),1.20 if not isvan else 1.48),(.24,.19,.12),ma,vehiclecol,handle,.04)
   box('v03 headlight lens',(L/2+.012,sign*.65,.79 if not isvan else 1.05),(.025,.32,.17),white,vehiclecol,handle)
   box('v03 night headlight',(L/2+.028,sign*.65,.79 if not isvan else 1.05),(.02,.27,.13),light,nightcol,handle)
   box('v03 tail light',(-L/2-.015,sign*.68,.8),(.025,.22,.14),rear,vehiclecol,handle)
  for xx in (-L/2,L/2):box('v03 bumper',(xx,0,.55),(.13,w*.95,.16),steel,vehiclecol,handle,.025)
  box('v03 radiator grille',(L/2+.08,0,.79),(.025,.68,.22),black,vehiclecol,handle)
  for j in range(6):box('v03 grille slat',(L/2+.10,(j-2.5)*.10,.79),(.012,.017,.20),steel,vehiclecol,handle,.002)
  box('v03 license plate',(L/2+.12,0,.56),(.025,.38,.11),white,vehiclecol,handle,.005)
 # Tree trunks and branching replaced; night strings stay attached to the same controls.
 for handle in [o for o in bpy.data.objects if o.name.startswith('MOVER Arbol')]:
  for o in list(handle.children):
   if o.name.startswith('Bare tree branch'):bpy.data.objects.remove(o,do_unlink=True)
  rr=random.Random(int(handle.name.split()[-1]));h=12 if handle.name.endswith('92') else 13;rootx=0;rooty=0
  trunk=[(0,0,0),(.08,.10,h*.22),(-.18,.03,h*.44),(.15,-.12,h*.62)]
  o=curve('v03 organic trunk',trunk,.28,wood,treecol,handle)
  for pt,radius in zip(o.data.splines[0].bezier_points,(1,.8,.55,.28)):pt.radius=radius
  def branch(start,vec,rad,depth):
   mid=Vector(start)+Vector(vec)*.45+Vector((rr.uniform(-.25,.25),rr.uniform(-.2,.2),.1));end=Vector(start)+Vector(vec);o=curve('v03 curved branch',[start,mid,end],rad,wood,treecol,handle)
   for p,factor in zip(o.data.splines[0].bezier_points,(1,.75,.35)):p.radius=factor
   if depth:
    base=Vector(vec).normalized()
    for j in range(2):
     v=base+Vector((rr.uniform(-.65,.65),rr.uniform(-.5,.5),rr.uniform(-.12,.3)));v.normalize();branch(end,v*Vector(vec).length*rr.uniform(.52,.72),rad*.48,depth-1)
  for j in range(8):
   a=j*2.4+rr.uniform(-.3,.3);start=(0,0,h*(.29+j*.045));length=rr.uniform(2.6,4.1);branch(start,(math.cos(a)*length,math.sin(a)*length*.68,length*.6),.09 if j<4 else .065,3)
 # Pavement, curbs and access stay separate from building geometry.
 for sign in (-1,1):
  for xa,xb in ((-25,-9.5),(9.5,25)) if sign==1 else ((-25,25),):
   box('v03 stone curb',((xa+xb)/2,-14+sign*4.1,.07),(xb-xa,.22,.22),stone,vehiclecol,bevel=.025)
   box('v03 sidewalk',((xa+xb)/2,-14+sign*4.75,-.006),(xb-xa,1.1,.07),stone,vehiclecol,bevel=.01)
  # Slab joints are curves, no texture downloads.
  for i in range(35):
   x=-24+i*1.4
   if sign==1 and abs(x)<9.5:continue
   curve('v03 sidewalk joint',[(x,-14+sign*4.24,.034),(x,-14+sign*5.24,.034)],.004,black,vehiclecol)
 for o in list(snowcol.objects):
  if o.name.startswith('Roadside snow drift'):
   bm=bmesh.new();bm.from_mesh(o.data);faces=[f for f in bm.faces if (o.matrix_world@f.calc_center_median()).y>-14 and abs((o.matrix_world@f.calc_center_median()).x)<9.5];bmesh.ops.delete(bm,geom=faces,context='FACES');bm.to_mesh(o.data);bm.free()
 # Asphalt procedural roughness avoids a uniform mirror surface.
 n=road.node_tree.nodes;l=road.node_tree.links;p=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3;noise.inputs['Detail'].default_value=2;l.new(geo.outputs['Position'],noise.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.18,.18,.18,1);ramp.color_ramp.elements[1].color=(.48,.48,.48,1);l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Roughness']);bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.007;bump.inputs['Strength'].default_value=.15;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 export_modules(root,P)
 for scene in (day,night):scene['engine_version']='0.3'
 (root/'detail.json').write_text(json.dumps({'version':'0.3','changes':['side brick projection corrected','sloped vehicle glazing, rims, tires, mirrors and lamps','curved tapered trees with hierarchical branching','curbs and sidewalks','wet asphalt roughness variation'],'main_dimensions_unchanged':True,'limits':['context buildings remain simplified','no people, exact survey or engineering validation','vehicles are interpretations, not manufacturer models']},indent=2))
