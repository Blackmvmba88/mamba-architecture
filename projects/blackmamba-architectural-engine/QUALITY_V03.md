# Calidad y escalado de la escena invernal — propuesta v0.3

**Estado:** especificación y primera validación estática; **no** equivale a un render nuevo ni a una mejora visual validada. Referencia visual: captura del barrio nevado compartida el 2026-10-08.

## Principio
Mantener la casa y el barrio editables. Mejorar por capas, empezando por defectos visuales comprobables, sin sacrificar el uso del Mac mini ni sobrescribir modificaciones manuales del archivo .blend.

## Hallazgos de la captura (observación, no geometría verificada)
- La casa principal ya tiene volumen, buhardillas, vanos, material de ladrillo e iluminación interior.
- Árboles desnudos, vehículos, banquetas, nieve y carretera establecen el entorno.
- La calle refleja luz, pero todavía se perciben vehículos como bloques simplificados.
- El arbolado es muy lineal y la periferia del barrio se ve incompleta.
- La imagen incluye cuadrícula y gizmos de Blender: es una vista de trabajo, **no** el render definitivo.
- La luz solar está seleccionada; su icono visible no es un objeto decorativo de la escena.

## Prioridad de detalle (orden de construcción)
| Fase | Área | Criterios observables |
| --- | --- | --- |
| A | Composición / cámara | Render de día y noche sin cuadrícula ni gizmos, casa legible, calle y vehículos dentro de encuadre |
| B | Techo / nieve | Cubierta continua, acumulación sin atravesar ventanas, pendientes y aleros coherentes |
| C | Vehículos | Ruedas, cristales, faros, proporciones y contacto con pavimento; objetos separados y editables |
| D | Arbolado / calle | Ramas jerarquizadas, variaciones de silueta, señalización y bordillos sin intersecciones evidentes |
| E | Materiales / luz | Nieve con rugosidad, asfalto húmedo con reflejos moderados, ventanas cálidas, contraste día/noche |
| F | Reutilización | Casas, calles, vegetación y accesorios convertidos en módulos colocables y reutilizables |

## Puertas de calidad
1. **Preflight de parámetros**: `python3 preflight.py` detecta datos mal formados y límites básicos. No demuestra corrección geométrica.
2. **Reconstrucción aislada**: ejecutar scripts en carpeta/copia de trabajo limpia. Nunca sobreescribir un .blend editado manualmente.
3. **Auditoría Blender existente**: `blender --background house.blend --python audit.py`; comprobar aperturas, colecciones compartidas y controles.
4. **Revisión visual**: tomar dos renders reproducibles (día/noche) con la misma cámara y comparar encuadre, penetraciones, sombras y superficies.
5. **Rendimiento**: registrar tiempo de render, memoria y número de objetos; instanciar geometría repetida; mantener modo preview económico.
6. **Resultado**: cada fase adjunta imagen antes/después, cambio reproducible y riesgo pendiente. No marcar *validado* sin ejecutar las pruebas.

## Contrato de módulos futuros
Cada módulo de ciudad debe declarar `id`, `kind`, `version`, `origin`, `dimensions_m`, `anchors`, `materials`, `lod`, `dependencies` y `evidence`. Los anclajes permiten acoplar vía, banqueta, puerta, luminaria o parque sin posiciones rígidas globales.

## Comandos iniciales
```sh
cd projects/blackmamba-architectural-engine
python3 preflight.py
blender --background house.blend --python audit.py
blender --background --python build.py -- --preview
```
La última orden puede regenerar y sobrescribir entregables generados: correr solamente en una copia. No se ejecutó Blender desde esta revisión remota.

## Próximo cambio implementable
Agregar un modo de ensamblaje de manzana residencial, reutilizando `MOVER CASA COMPLETA`, árboles y vehículos y agregando identificadores de módulos; no duplicar el motor arquitectónico que ya existe.
