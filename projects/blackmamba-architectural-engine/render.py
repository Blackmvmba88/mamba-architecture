"""Render the audited saved scene; preserves main cameras/settings and adds detail camera."""
import bpy,json,time,resource,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;started=time.perf_counter();metrics=[]
for s in bpy.data.scenes:
 s.render.resolution_percentage=100;s.render.resolution_x=1050;s.render.resolution_y=1500;s.cycles.samples=32;s.cycles.use_denoising=True
 s.render.filepath=str(R/(s.name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True,scene=s.name);metrics.append({'scene':s.name,'seconds':round(time.perf_counter()-t,3),'samples':32,'size':[1050,1500]})
s=bpy.data.scenes['winter_day'];main=s.camera;data=bpy.data.cameras.new('Detalle camioneta');cam=bpy.data.objects.new('CAMARA Detalle camioneta',data);s.collection.objects.link(cam);bpy.data.scenes['christmas_night'].collection.objects.link(cam)
loc=bpy.data.objects['MOVER Camioneta'].location;cam.location=loc+Vector((6,-8,7));target=loc+Vector((0,0,1.2));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=6.2;s.camera=cam;s.render.resolution_y=700;s.cycles.samples=24;s.render.filepath=str(R/'vehicle_detail.png');t=time.perf_counter();bpy.ops.render.render(write_still=True,scene=s.name);metrics.append({'scene':'vehicle_detail','seconds':round(time.perf_counter()-t,3),'samples':24,'size':[1050,700]})
s.camera=main;s.render.resolution_y=1500;s.cycles.samples=32;s.render.filepath=str(R/'winter_day.png');bpy.ops.wm.save_as_mainfile(filepath=str(R/'house.blend'))
(R/'performance.json').write_text(json.dumps({'blender':bpy.app.version_string,'mode':'final','stage':'renders of audited saved scene','total_seconds':round(time.perf_counter()-started,3),'process_peak_rss_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024*1024 if sys.platform=='darwin' else 1024),2),'render_metrics':metrics},indent=2))
