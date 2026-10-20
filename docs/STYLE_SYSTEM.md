# BlackMamba Architecture Lab — Sistema de estilos v0.2

## Alcance
Catálogo parametrizado de siete familias estéticas tomadas como **inspiración general** de referencias visuales aportadas por el propietario del proyecto. Ninguna fotografía se incorpora ni distribuye. Los renders o fotografías no acreditan dimensiones reales, solución de estructura ni viabilidad normativa.

## Familias
| ID | Macro-lenguaje | Gramática de diseño | Materialidad sugerida | Consideración crítica |
|---|---|---|---|---|
| sacred_dome | Sagrado/ceremonial | eje radial, costillas y lucernario | madera y vidrio | conexiones, fuego y cargas |
| geodesic_suite | Futurista orgánico | celdas facetadas, mirada panorámica | madera/acero/vidrio | uniones y clima |
| stained_glass_pavilion | Sagrado/ceremonial | anillo, vitrales, simetría | metal y vidrio coloreado | protección térmica y del vidrio |
| heritage_villa | Patrimonio/ornamental | composición axial, arcos | piedra, ladrillo, hierro | intervención patrimonial |
| ceremonial_estate | Patrimonio/ornamental | patio y ejes ceremoniales | piedra y estuco | accesibilidad |
| biophilic_oasis | Biofílico | vacío verde, óculo, agua | madera, vidrio, piedra | higiene y humedad |
| stone_timber_rotunda | Refugio contemplativo | rotonda con nervios de madera | piedra y madera | humo y protección al fuego |

## Variables compartidas
`roof_type`, `symmetry_mode`, `aperture_style`, `material_palette`, `light_strategy`, `biophilia_level`, `ornament_density`, `ritual_center`, `water_feature`, `glazing_ratio`, `radial_pattern_complexity`.

Los nombres de estilos no son certificaciones ni sistemas constructivos. `radial_pattern_complexity` indica resolución decorativa propuesta, no número de piezas estructurales verificadas. `glazing_ratio` es un objetivo conceptual, no un porcentaje calculado del proyecto.

## Implementación
`lab/style_presets.py`: catálogo tipado e inmutable, sin dependencias externas.
`lab/styled_habitat.py`: exporta un **esquema plano de anillo y radios**, no un domo real.

```bash
python3 -m lab.styled_habitat --style sacred_dome --radius 6 --segments 12 --output out/sacred_dome.json
python3 -m lab.styled_habitat --style biophilic_oasis --radius 5
python3 -m unittest discover -s lab/tests -v
```

## Iteración posterior
1. Construir geometrías 3D por tipología con contratos geométricos separados de estilos.
2. Implementar exportador Blender basado en coordenadas, no en fotos.
3. Reimportar y medir cotas digitales contra parámetros.
4. Añadir modelos de luz/sombra y métricas con incertidumbre.
5. Exigir cálculo profesional para cargas, uniones, incendios, accesibilidad y obras reales.

**Gate actual: P0 — intención formal y parámetros, sin validación de ingeniería.**

## Blender: volumen radial editable y medición

El adaptador conserva el esquema plano por defecto. `--height 3` añade un
prisma radial cerrado de 3 m de altura, con caras editables. Es una envolvente
conceptual común a los siete estilos: todavía no implementa sus tipologías,
cubiertas, materiales ni aperturas particulares.

```bash
python3 -m lab.styled_habitat --style sacred_dome --radius 6 --segments 12 --output out/style.json
blender --background --python lab/blender_radial.py -- --input out/style.json --output out/style.blend --height 3 --report out/measurement.json
blender --background --python lab/tests/blender_smoke.py -- out/blender-smoke
```

La escena usa metros y conserva el JSON de origen en `source_parameters_json`.
El reporte mide área poligonal de huella y volumen de malla, verifica coordenadas
y comprueba cierre manifold. El área corresponde al polígono discretizado, no
al círculo ideal. La prueba Blender guarda y reabre los siete estilos, verifica
parámetros, altura, topología y volumen; requiere Blender instalado. La suite
unitaria se ejecuta por separado y no demuestra por sí sola integración Blender.
Los archivos existentes `.blend` no se sobrescriben. Usa una carpeta nueva al
repetir la prueba.
