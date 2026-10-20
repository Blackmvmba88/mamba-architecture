# Sacred Dome P3 — exportación Blender y auditoría independiente

Genera y valida una cubierta *conceptual abierta*, no un edificio completo. El objeto contiene un paraboloide discretizado con óculo abierto; sin espesor estructural, costillas reales, muros, puerta, vidrio ni unión física.

## Reproducción (en la raíz de mamba-architecture)
```bash
python3 -m lab.sacred_dome_p2 --radius 6 --segments 12 --output out/sacred-p3.json
blender --background --python lab/blender_sacred_dome.py -- --input out/sacred-p3.json --output out/sacred-p3.blend
blender --background --python lab/audit_sacred_dome.py -- --input out/sacred-p3.json --blend out/sacred-p3.blend --report out/sacred-p3-audit.json
python3 -m unittest discover -s lab/tests -v
```
Usar **dos procesos Blender separados**: la auditoría abre el archivo guardado y compara conteos, conectividad, coordenadas (tolerancia 0.00002 m), transformación e identificador SHA-256 del JSON canónico. La comprobación cubre geometría digital, no una verificación independiente de seguridad ni de condiciones físicas.

Se rechaza sobrescribir el archivo Blender o reporte. Blender debe invocarse en modo background: el exportador reinicia una escena en su proceso y no debe correrse dentro de una sesión GUI con trabajo no guardado.

**Gate:** P3 de intercambio digital. Pendientes: ensayos de transferencia a otro sistema, revisión de norma, cargas y diseño detallado.
