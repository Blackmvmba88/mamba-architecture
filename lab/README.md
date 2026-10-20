# Laboratorio de hábitats P0

Generación de volúmenes 3D abstractos en JSON para siete presets. **No** produce archivos CAD, Blender ni diseños seguros para construir.

Ejecutar desde la raíz:

```bash
python3 -m lab.habitat --preset habitat_arctic --levels 3 --output out/habitat.json
python3 -m unittest discover -s lab/tests -v
```

El campo `center_m` y `size_m` define cajas alineadas a XYZ, unidades metros, Z vertical. Los offsets son estilísticos, sin cálculo de voladizo ni conexiones.
