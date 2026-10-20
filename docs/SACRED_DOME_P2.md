# Sacred Dome P2 — primer módulo arquitectónico detallado

## Objetivo
Extender la intención de masa (`sacred_dome`) con una cubierta paramétrica tridimensional compuesta por anillos y paños cuadrangulares. La sección de cubierta usa el perfil analítico `z = h_wall + h_roof × (1 − (r/R)²)`, truncado en un óculo central.

## Entregable actual
- Generador autónomo Python: `lab/sacred_dome_p2.py`.
- JSON: puntos XYZ (metros), caras cuadrangulares y metadatos de óculo y vano propuesto.
- Pruebas: conteos topológicos, radio de óculo, determinismo y entradas inválidas.

```sh
python3 -m lab.sacred_dome_p2 --radius 6 --segments 12 --oculus-ratio 0.18 --output out/sacred-dome-p2.json
python3 -m unittest discover -s lab/tests -v
```

## Restricciones y estado
- Superficie 3D abierta: el motor no acredita estanqueidad volumétrica. Óculo **sin vidrio modelado**.
- No se generan muros, puertas recortadas ni costillas sólidas; se registran como intención de diseño.
- Los materiales son etiquetas, no propiedades físicas.
- No existe cálculo de viento, nieve, sismo, cimentación, uniones ni comportamiento acústico.
- Ninguna de estas geometrías debe utilizarse como plano constructivo sin proyecto ejecutivo y cálculo profesional.

## Gate P2 a P3
Construir adaptador Blender para nueva geometría sin sobrescribir escenas, reabrir en proceso independiente y comparar cotas/topología con tolerancias declaradas. Añadir espesores y aperturas reales únicamente cuando haya verificación geométrica y revisión normativa.
