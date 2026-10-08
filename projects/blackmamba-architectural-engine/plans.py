"""Standalone SVG drawings from same parameters as Blender. Python stdlib only."""
import json, math
from pathlib import Path
R=Path(__file__).resolve().parent;P=json.loads((R/'parameters.json').read_text());W,D,T,B,H,RR=[P[k] for k in ('width','depth','wall','base','storey','roof_rise')];E=B+2*H;S=32
out=[]
def ln(x,y,a,b,stroke='#243c4b',width=1):out.append(f'<line x1="{x}" y1="{y}" x2="{a}" y2="{b}" stroke="{stroke}" stroke-width="{width}"/>')
def rect(x,y,w,h,fill='none',stroke='#243c4b'):out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>')
def txt(x,y,t,size=12):out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="#243c4b">{t}</text>')
def start(title):
 global out
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="800" viewBox="0 0 1100 800"><rect width="1100" height="800" fill="#faf8f1"/><g font-family="Arial">'];txt(35,40,'BLACKMAMBA ARCHITECTURAL ENGINE',23);txt(35,68,title,19);txt(35,95,'CONCEPTUAL • Todas las medidas estimadas • Metros • Frente = −Y • Sin norte geográfico',13)
def end(name):
 txt(35,748,'v0.2 | Referencias ilustradas día/noche | Interiores y fachadas ocultas: hipótesis | No apto para obra',13)
 ln(35,701,35+5*S,701,width=3)
 for i in range(6):ln(35+i*S,695,35+i*S,707);txt(35+i*S,723,str(i),10)
 txt(230,723,'m — usar barra gráfica al imprimir',10);out.append('</g></svg>');(R/(name+'.svg')).write_text(''.join(out))
def dim(x,y,w,label):
 ln(x,y,x+w,y);ln(x,y-6,x,y+6);ln(x+w,y-6,x+w,y+6);txt(x+w/2-30,y-8,label)
x0,y0=180,170
for lv,title in enumerate(('Planta baja','Primera planta','Ático conceptual','Cubierta')):
 start(title);ww=W*S;dd=D*S
 rect(x0,y0,ww,dd,'#eee9db');rect(x0+T*S,y0+T*S,(W-2*T)*S,(D-2*T)*S,'#faf8f1')
 dim(x0,y0-30,ww,f'{W:.2f} m');txt(x0+ww+15,y0+dd/2+30,f'{D:.2f} m')
 if lv<2:
  for sign in (-1,1):
   x=x0+(W/2+sign*1.35)*S

   for ya,yb in ((-D/2+.3,-2.8),(-1.7,1.8),(2.9,D/2-.3)):ln(x,y0+(D/2-yb)*S,x,y0+(D/2-ya)*S,width=4)
   ln(x0+(T if sign<0 else W/2+1.35)*S,y0+(D/2-1)*S,x0+(W/2-1.35 if sign<0 else W-T)*S,y0+(D/2-1)*S,width=4)
  labels=['Cocina / comedor','Estudio','Salón','Biblioteca'] if lv==0 else ['Dormitorio A','Dormitorio B','Dormitorio C','Baño / vestidor']
  for text,x,y in zip(labels,[205,485,205,485],[230,230,410,410]):txt(x,y,text)
  txt(365,330,'Hall',12)
  for i in range(18):ln(x0+(W/2-.55)*S,y0+(D/2-1-i*.22)*S,x0+(W/2+.55)*S,y0+(D/2-1-i*.22)*S)
  txt(350,190,'Escalera',10)
  for face in (0,dd):
   for x in P['window_axes']:
    xx=x0+(x+W/2)*S;rect(xx-P['window_width']*S/2,y0+face-4,P['window_width']*S,8,'#d4eaf0')
  rect(x0+(W/2-.725)*S,y0+dd-7,1.45*S,14,'#faf8f1')
  for side in (0,ww):
   for yy in (-3.3,0,3.3):rect(x0+side-4,y0+(yy+D/2)*S-1.3*S/2,8,1.3*S,'#d4eaf0')
  txt(740,180,f'Cota piso: +{B+lv*H:.2f} m');txt(740,210,f'Muro exterior: {T:.2f} m');txt(740,240,'Tabiques: 0.15 m');txt(740,270,'Puertas interiores: 1.10 m');txt(740,300,'Distribución propuesta, no visible');txt(740,330,'Escalera: 18 contrahuellas');txt(740,350,f'{H/18:.3f} m / huella 0.22 m');txt(740,380,'Escalera preliminar sin cálculo');txt(740,400,'normativo ni estructural')
 elif lv==2:
  lim=(D/2+P['overhang'])*(2.1/RR)
  for yy in (lim,D-lim):ln(x0,y0+yy*S,x0+ww,y0+yy*S,stroke='#b87341');txt(x0+ww+15,y0+yy*S,'h = 2.10 m',10)
  txt(300,335,'Ático abierto — uso pendiente')
  for x in P['dormer_axes']:rect(x0+(x+W/2-.825)*S,y0+dd-2.2*S,1.65*S,1.75*S)
  txt(740,230,f'Piso ático: +{E:.2f} m');txt(740,265,'Líneas de altura libre estimadas');txt(740,290,'Dos buhardillas con huecos en');txt(740,310,'cubierta; dimensiones inferidas')
 else:
  a=W/2+P['overhang'];c=D/2+P['overhang'];rid=a-c
  rect(x0-P['overhang']*S,y0-P['overhang']*S,2*a*S,2*c*S)
  p1=(x0+(W/2-rid)*S,y0+dd/2);p2=(x0+(W/2+rid)*S,y0+dd/2)
  ln(*p1,*p2,width=2)
  for pt,corner in [(p1,(x0,y0)),(p1,(x0,y0+dd)),(p2,(x0+ww,y0)),(p2,(x0+ww,y0+dd))]:ln(*pt,*corner)
  for x in P['dormer_axes']:rect(x0+(x+W/2-.825)*S,y0+dd-2.2*S,1.65*S,1.75*S)
  txt(740,230,f'Alero: +{E:.2f} m');txt(740,260,f'Cumbrera: +{E+RR:.2f} m');txt(740,290,f'Pendiente: {math.degrees(math.atan(RR/c)):.1f}°');txt(740,320,'Voladizo: 0.45 m')
 txt(340,560,'FRENTE / acceso');ln(x0-20,y0+dd/2,x0+ww+20,y0+dd/2,stroke='#bd543e');txt(x0-40,y0+dd/2,'A');txt(x0+ww+30,y0+dd/2,'A');ln(x0+ww/2,y0-10,x0+ww/2,y0+dd+20,stroke='#bd543e');txt(x0+ww/2,y0-15,'B');txt(x0+ww/2,y0+dd+40,'B');end(f'plan_{lv}')
for face in ('front','rear','left','right'):
 start({'front':'Alzado frontal','rear':'Alzado posterior (inferido)','left':'Alzado izquierdo parcialmente visible','right':'Alzado derecho (inferido)'}[face]);span=W if face in ('front','rear') else D;xx=180;ground=570
 def z(v):return ground-v*S
 rect(xx,z(E),span*S,(E-B)*S,'#cc8c73');rect(xx,z(B),span*S,B*S,'#c2b5a0')
 c=D/2+P['overhang'];r=W/2+P['overhang']-c
 pts=[(xx-P['overhang']*S,z(E)),(xx+span*S+P['overhang']*S,z(E))]
 if face in ('front','rear'):pts += [(xx+(W/2+r)*S,z(E+RR)),(xx+(W/2-r)*S,z(E+RR))]
 else:pts += [(xx+span*S/2,z(E+RR))]
 out.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in pts)+'" fill="#655d50" stroke="#243c4b"/>')
 axes=P['window_axes'] if face in ('front','rear') else [-3.3,0,3.3]
 for lv in range(2):
  for axis in axes:
   wx=xx+(axis+span/2)*S;wh=P['window_height'];ww=P['window_width'] if span==W else 1.3
   rect(wx-ww*S/2,z(B+lv*H+.5+wh),ww*S,wh*S,'#e3f2f5');ln(wx,z(B+lv*H+.5),wx,z(B+lv*H+.5+wh));ln(wx-ww*S/2,z(B+lv*H+.5+wh/2),wx+ww*S/2,z(B+lv*H+.5+wh/2))
 if face=='front':
  rect(xx+(W/2-.725)*S,z(B+2.55),1.45*S,2.55*S,'#73503d')
  for axis in P['dormer_axes']:
   x=xx+(axis+W/2)*S;dz=E+RR*(1-3.25/c);rect(x-.825*S,z(dz+1.5),1.65*S,1.5*S,'#eee9db');ln(x-.92*S,z(dz+1.5),x,z(dz+2.2));ln(x,z(dz+2.2),x+.92*S,z(dz+1.5))
 for height in (0,B,B+H,E,E+RR):ln(150,z(height),720,z(height),stroke='#b4b4a9');txt(750,z(height)+4,f'+{height:.2f} m')
 dim(xx,625,span*S,f'{span:.2f} m');end('elevation_'+face)
for orient,span in [('A',W),('B',D)]:
 start(f'Sección {orient}–{orient} — longitudinal' if orient=='A' else 'Sección B–B — transversal');xx=180;ground=570
 def z(v):return ground-v*S
 for lv in range(3):
  if orient=='B' and lv:
   rect(xx,z(B+lv*H),(.4)*S,.2*S,'#929d9b');rect(xx+4.7*S,z(B+lv*H),(span-4.7)*S,.2*S,'#929d9b')
  else:rect(xx,z(B+lv*H),span*S,.2*S,'#929d9b')
  txt(740,z(B+lv*H)+4,f'Piso +{B+lv*H:.2f} m')
 for x in (xx,xx+(span-T)*S):rect(x,z(E),T*S,(E-B)*S,'#cc8c73')
 if orient=='A':
  ridge=W/2+P['overhang']-(D/2+P['overhang']);ln(xx,z(E),xx+(W/2-ridge)*S,z(E+RR),width=3);ln(xx+(W/2-ridge)*S,z(E+RR),xx+(W/2+ridge)*S,z(E+RR),width=3);ln(xx+(W/2+ridge)*S,z(E+RR),xx+span*S,z(E),width=3)
 else:
  ln(xx,z(E),xx+span*S/2,z(E+RR),width=3);ln(xx+span*S/2,z(E+RR),xx+span*S,z(E),width=3)
  for lv in range(2):
   for i in range(18):rect(xx+(span/2-1-i*.22)*S,z(B+lv*H+i*H/18),.24*S,.1*S,'#73503d')
 txt(740,185,f'Cumbrera +{E+RR:.2f} m');txt(740,215,'Forjados: 0.20 m hipotéticos');txt(740,245,'Sin estructura calculada');dim(xx,625,span*S,f'{span:.2f} m');end('section_'+orient)
print('10 SVG sheets generated')
