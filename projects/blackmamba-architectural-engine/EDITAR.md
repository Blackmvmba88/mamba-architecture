# Mover y editar la escena en Blender

Abre `house.blend`. Todo es geometría editable; los renders PNG son imágenes fijas.

## Explorar

- Rueda del ratón: acercar o alejar.
- Botón central y arrastrar: girar alrededor de la escena.
- Shift + botón central: desplazar la vista.
- Teclado numérico 0: ver desde la cámara del cartel.
- Home: encuadrar todos los objetos. Punto del teclado numérico: encuadrar la selección.

## Mover elementos completos

En el panel de objetos de la derecha busca los controles:

- `MOVER CASA COMPLETA`: mueve casa, carpinterías y decoración de la casa. Jardines, terreno y luces ambientales tienen grupos separados.
- `MOVER Arbol 91`, `92`, `93`: mueve cada árbol completo.
- `MOVER Auto rojo` y `MOVER Camioneta`: mueve cada vehículo completo.

Selecciona el control y pulsa G para mover, R para girar o S para escalar. Después puedes pulsar X, Y o Z para limitar a ese eje, escribir una cantidad y confirmar con Enter. Esc cancela. Ctrl + Z deshace.

Ejemplo: selecciona `MOVER Auto rojo`, pulsa G, X, 2 y Enter para desplazarlo 2 metros en X.

Para una pieza individual, selecciónala directamente. Algunas mallas de follaje comparten datos para ahorrar memoria: antes de cambiar su forma hazla de usuario único desde Object > Relations > Make Single User > Object & Data. Mover o escalar una instancia individual no cambia las otras.

## Cambiar día y noche

Usa el selector de escena en la barra superior: `winter_day` o `christmas_night`. La arquitectura y sus movimientos se comparten; la iluminación y guirnaldas tienen configuraciones separadas. Activa Material Preview para trabajar ágilmente o Rendered para revisar la luz. F12 genera un render de la escena actual.

## Guardar tus ajustes

Usa Save As y crea `mi_version.blend`. Los scripts reconstruyen el archivo generado y sustituyen sus entregables; no recuperan cambios manuales. Para cambios repetibles, modifica `parameters.json`, `build.py` o `enhance.py` y vuelve a generar. La distribución interior y las dimensiones siguen siendo hipótesis.
