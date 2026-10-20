# Calidad y escalado de la escena invernal — propuesta v0.3

**Estado actual:** v0.3 ejecutada en el Mac local; preflight y auditoría geométrica aprobados. Se generaron renders nuevos y se revisaron visualmente. El apartado de captura conserva la evaluación original que inició este PR.

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
La última orden puede regenerar y sobrescribir entregables generados: correr solamente en una copia. La revisión inicial fue remota; esta continuación ejecuta Blender 5.2.0 localmente.

## Próximo cambio implementable
Agregar un modo de ensamblaje de manzana residencial, reutilizando `MOVER CASA COMPLETA`, árboles y vehículos y agregando identificadores de módulos; no duplicar el motor arquitectónico que ya existe.


## Evidencia ejecutada — 2026-10-08

- Parámetros: `preflight.py` aprobado; seis pruebas de entradas válidas/incorrectas aprobadas en `test_preflight.py`.
- Geometría: `audit.json` confirma ventanas frontales, huecos de escalera y buhardillas, escena compartida y controles de movimiento; verifica ocho neumáticos a menos de 4 mm de las superficies muestreadas, cuatro huecos reales de rueda, contraventanas sin solape y seis manifiestos de módulo.
- Materiales: la fachada lateral deja de usar el eje X constante para ladrillo y usa Y/Z según la normal de superficie. Asfalto con rugosidad espacial.
- Detalles: vehículos con cristales inclinados, arcos de rueda, rines, neumáticos, espejos, luces y rack; árboles con ramas curvas jerarquizadas; bordillos y banquetas abiertos frente al acceso. El coche se aparta de los escalones.
- Cámara: los renders generales mantienen cámara y encuadre v0.2. `before_*.png` permite comparar. `vehicle_detail.png` muestra una vista cercana adicional, no sustituye las escenas principales.
- Reproducibilidad: `build.py` reconstruye desde cero y llama `enhance.py` y `detail.py`; `render.py` renderiza un archivo ya auditado. `performance.json` mide tiempo y RSS del proceso para esta ejecución.

### Límites pendientes

Vecindario e iglesia continúan como contexto simplificado; no se completaron interiores, personas, encuentros constructivos ni nieve física. El manifiesto de módulos registra conjuntos y límites medidos, pero **no** implementa aún un ensamblador general de manzanas. Las verificaciones muestrean contactos y huecos concretos y no constituyen una detección exhaustiva de colisiones ni una certificación de arquitectura real. Ningún .blend con ajustes manuales se sobrescribió: esta revisión se generó en una carpeta nueva.

Medición de renders: día 27.02 s, noche 43.50 s, detalle 11.615 s; proceso 82.35 s y pico RSS 1452 MiB (~1.42 GiB). Una pasada adicional amplió el encuadre del detalle para conservar el vehículo completo; queda registrada en `performance.json`. `framing.json` confirma casa y vehículos dentro de la cámara general y camioneta completa en la cámara de detalle. Estos tiempos corresponden a esta estación y a estas resoluciones, no son un benchmark universal.

Reconstrucción limpia adicional aprobada: límites de seis conjuntos coinciden dentro de 1 mm con los del archivo entregado. Esta tolerancia prueba repetibilidad del script y no precisión de levantamiento arquitectónico. La copia limpia no tiene la cámara de detalle hasta ejecutar `render.py`; la auditoría registra expresamente ese chequeo como omitido en esa etapa.
