# BLACKMAMBA ARCHITECTURAL ENGINE — v0.1

Primera reconstrucción conceptual paramétrica de la casa principal en las dos ilustraciones de invierno. El modelo y diez láminas comparten `parameters.json`. Unidades: metros, Z arriba, frente −Y, origen al centro de la casa. No se conoce orientación geográfica ni escala real.

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

Interiores y trasera son hipótesis útiles para comenzar. El ático queda abierto; los tabiques no son un proyecto ejecutivo. Escalera recta preliminar: 18 peldaños por vuelo, contrahuella 0.1722 m, huella 0.22 m; requiere rediseño, comprobación de altura libre y normativa local antes de uso constructivo. No hay cálculo estructural, instalaciones, impermeabilización, mobiliario, árbol complejo, vehículos ni barrio en esta versión. Cubierta y nieve no resuelven constructivamente encuentros, drenajes o cargas. Los alzados SVG simplifican carpintería y ornamentación y las secciones muestran elementos principales, no todos los detalles de la malla.

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
