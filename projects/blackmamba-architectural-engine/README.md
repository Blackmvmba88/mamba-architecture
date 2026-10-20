# BLACKMAMBA ARCHITECTURAL ENGINE — v0.3

Reconstrucción conceptual paramétrica de la casa principal en las dos ilustraciones de invierno. El modelo y diez láminas comparten `parameters.json`. Unidades: metros, Z arriba, frente −Y, origen al centro de la casa. No se conoce orientación geográfica ni escala real.

## Entregables

- `house.blend`: escenas `winter_day` y `christmas_night`, misma geometría arquitectónica compartida; iluminación, cristales emisivos y guirnalda distintos.
- `winter_day.png`, `christmas_night.png`: vistas de revisión.
- `plan_0.svg`…`plan_3.svg`: baja, primera, ático, cubierta.
- `elevation_front/rear/left/right.svg`: cuatro alzados.
- `section_A.svg`, `section_B.svg`: secciones longitudinal y transversal.
- `index.html`: visor local de renders y láminas.
- `build.py`, `plans.py`: generación reproducible; `validation.json` y `audit.json`: comprobaciones del archivo guardado.

## Lo verificable y lo inferido

Verificable **en las ilustraciones**, no en un edificio real: casa de ladrillo rojo, dos plantas, cubierta a cuatro aguas, dos buhardillas frontales, ventanas verticales con marcos claros y contraventanas oscuras, acceso central arqueado, chimenea, escalones, barandas, jardines curvos y nieve. La noche incorpora iluminación cálida y guirnaldas. Son referencias artísticas con posibles diferencias entre versiones; no fotografías calibradas.

Inferido: todas las dimensiones, profundidad, pendiente, posición exacta de huecos, espesores, estructura, distribución de habitaciones, escalera, parte posterior y lateral oculto. La simetría y seis ejes de ventanas por planta son una simplificación de la lectura visual; las proporciones todavía no se ajustaron por fotogrametría.

| Parámetro | Hipótesis inicial | Intervalo orientativo sin medición |
|---|---:|---:|
| Frente | 14.40 m | 12–16 m |
| Fondo | 10.80 m | 9–13 m |
| Piso bajo | +0.80 m | 0.6–1.0 m |
| Altura entre pisos | 3.10 m | 2.8–3.4 m |
| Piso primera planta | +3.90 m | derivado |
| Piso ático / alero | +7.00 m | derivado |
| Cumbrera | +10.00 m | derivado |
| Muro exterior | 0.30 m | 0.25–0.40 m |
| Forjado | 0.20 m | 0.18–0.30 m |
| Ventana frontal | 1.15 × 2.00 m | no medida |
| Pendiente | 27.15° | 25–40° |

Estos intervalos expresan incertidumbre de diseño, no resultados estadísticos. La escala se propone usando una puerta residencial de 2.24 m como ancla convencional; no permite verificar el tamaño real.

## Geometría y límites

Muros con huecos vacíos, forjados con hueco de escalera, cubierta con perforaciones de buhardillas, carpintería con jambas, alféizares y divisiones de vidrio; contraventanas con lamas; paneles de puerta, fanlight, arco curvo, cornisa, chimenea, tejas individuales agrupadas en mallas, nieve procedural, topiarios y jardín curvo. El ladrillo usa shader procedural con relieve, **no ladrillos individuales modelados**. La nieve es una cobertura estilizada determinista, no simulación física. Vegetación de detalle básico.

Interiores y trasera son hipótesis útiles para comenzar. El ático queda abierto; los tabiques no son un proyecto ejecutivo. Escalera recta preliminar: 18 peldaños por vuelo, contrahuella 0.1722 m, huella 0.22 m; requiere rediseño, comprobación de altura libre y normativa local antes de uso constructivo. No hay cálculo estructural, instalaciones, impermeabilización ni mobiliario. Árboles ramificados, vehículos y barrio son geometría conceptual de menor detalle que la casa. Cubierta y nieve no resuelven constructivamente encuentros, drenajes o cargas. Los alzados SVG simplifican carpintería y ornamentación y las secciones muestran elementos principales, no todos los detalles de la malla.

## Reproducir

Blender 5.2.0 LTS, Python incluido. `plans.py` usa Python estándar sin paquetes externos.

```sh
python3 plans.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python build.py
/Applications/Blender.app/Contents/MacOS/Blender --background house.blend --python audit.py
```

En otros sistemas reemplazar la ruta por `blender`. Ejecutar scripts de archivos confiables. El generador crea una escena nueva en el proceso y reemplaza sus propios entregables. No lo ejecutar dentro de un archivo con trabajo sin guardar. Editar dimensiones en `parameters.json` y regenerar ambos scripts; la distribución y elementos ornamentales son hipótesis con offsets fijos y requieren revisión para cambios grandes. Semilla 88. Sin descargas, plugins ni texturas externas.

## Infraestructura inspeccionada

Reutilizado `Blackmvmba88/mamba-architecture`, privado: módulos de geometría sagrada, generación procedural y diseño paramétrico; no incluía casa residencial ni archivos `.blend`. Revisado también el exportador biomimético de `3defect`: su base es una forma orgánica genérica, no apropiada como casa; no se alteró ese proyecto. Blender local 5.2.0 disponible y usado para generar archivo y renders. Las referencias originales se consultaron desde los adjuntos de la conversación; no se redistribuyen en GitHub por derechos de autor no establecidos.


## Refinamiento v0.2 — composición del cartel

Se mantiene la casa y las medidas aprobadas en v0.1. Se añade encuadre vertical desde la izquierda, nieve continua con volumen, cornisa arqueada más profunda, corona y lazo de puerta, dinteles de ladrillo, buhardillas con molduras, jardineras de mampostería escalonadas y follaje por instancias. Se incorporan tres árboles desnudos ramificados, farolas, un coche rojo, camioneta y volúmenes de casas e iglesia. La noche incorpora cadenas de luces alrededor de ventanas, luz azul y cálida y un brillo moderado de las fuentes emisivas.

La referencia guía composición y ambiente. El barrio, árboles y vehículos son interpretaciones simplificadas, no reconstrucciones exactas. La iglesia se reduce como recurso compositivo: no tiene escala histórica verificable. El material de nieve sigue siendo procedural, no una simulación física. Las imágenes originales no se usan como texturas ni se redistribuyen; se registran sus hashes en `reference_manifest.json`.

`enhance.py` contiene este refinamiento y `build.py` lo aplica automáticamente. Ambos se ejecutan localmente en Blender sin servicios de generación de imagen. Los constructores usan la API de datos y mallas compartidas para evitar operaciones repetidas costosas. Previsualización económica: `blender --background --python build.py -- --preview`. Crea previews al 40% con 12 muestras; el archivo `.blend` guardado conserva la configuración final de 1050 × 1500 y 32 muestras con eliminación de ruido.

Para editar, consulta [EDITAR.md](EDITAR.md). Las colecciones separan casa, nieve, jardines, árboles, barrio, calle y Navidad nocturna. Los controles `MOVER CASA COMPLETA`, `MOVER Arbol ...`, `MOVER Auto rojo` y `MOVER Camioneta` permiten transformar conjuntos completos. Guarda los cambios manuales en una copia: regenerar sustituye el archivo generado.


## Ejecución v0.3 — PR #4

Esta revisión se ejecutó en el Mac local con Blender 5.2.0. Se conserva la casa y su escala conceptual; el generador trabaja en una carpeta nueva para proteger v0.2 y archivos editados manualmente.

`detail.py` corrige la proyección del ladrillo en fachadas laterales, reemplaza vehículos por carrocerías con parabrisas inclinados y huecos reales de rueda, añade neumáticos, rines, espejos, parrillas, placas, faros y tubos de la camioneta. Reemplaza las ramas lineales por curvas Bézier con grosor variable y ramificación jerárquica, agrega bordillos y banquetas, y modula rugosidad del asfalto. El bordillo y la nieve del borde se abren frente al acceso. Las contraventanas se estrechan para evitar que se interpenetren entre ventanas contiguas.

Los vehículos mantienen sus controles y son interpretaciones, no réplicas de fabricante. El barrio periférico sigue siendo de menor detalle. Nieve y cubiertas aún son estilizadas y requieren detalles de encuentros constructivos si se usan para diseño técnico. No hay personas ni levantamiento dimensional.

`preflight.py` valida entradas antes de usar Blender y ahora comprueba semilla entera y posición aproximada de buhardillas. `test_preflight.py` prueba seis casos, incluidos parámetros incorrectos. `audit.py` verifica también ruedas respecto al pavimento, huecos de carrocería, contraventanas sin solape y el manifiesto de seis módulos editables. `modules.json` registra dimensiones obtenidas de vértices editables y envolventes conservadoras de curvas en ejes mundiales, incluidos accesorios; no son dimensiones nominales de arquitectura.

`performance.json` registra tiempos de esta ejecución y memoria máxima RSS del proceso, no memoria de GPU. `before_winter_day.png` y `before_christmas_night.png` corresponden a v0.2; los renders actuales conservan cámara, encuadre y escala para comparación. La guía de edición y los controles siguen disponibles en `EDITAR.md`.

```sh
python3 preflight.py
python3 test_preflight.py
blender --background --python build.py -- --preview
blender --background --python build.py
blender --background house.blend --python audit.py
blender --background house.blend --python render.py
```

`render.py` produce las dos escenas y una vista cercana `vehicle_detail.png`; agrega una cámara alternativa al archivo manteniendo las cámaras principales.

Los scripts reemplazan exclusivamente sus entregables generados. Usa una copia para proteger ajustes manuales. Revisa `QUALITY_V03.md`, `audit.json` y `performance.json` para evidencia y límites de esta revisión.
