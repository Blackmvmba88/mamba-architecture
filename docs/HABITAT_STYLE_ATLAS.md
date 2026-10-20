# Atlas paramétrico de hábitats v0.1

Las familias son **presets conceptuales**, no tipologías estructuralmente verificadas.

| ID | Familia | Geometría | Envolvente | Ambiente | Riesgo a estudiar |
|---|---|---|---|---|---|
| habitat_arctic | Hábitat ártico | módulos apilados | aislante, vidrio | nieve | nieve, puentes térmicos, voladizos |
| capsule_living | Cápsula confortable | prismas redondeados | paneles y vidrio | urbano | ventilación y evacuación |
| bioshell | BioShell | esfera/cascarón | envolvente curva | bosque | uniones e impermeabilización |
| forest_tower | Torre orgánica | cilindros apilados | terrazas vegetales | bosque | cargas húmedas, raíces, viento |
| stone_water | Piedra y agua | terrazas escalonadas | mampostería conceptual | ladera/canal | estabilidad geotécnica y humedad |
| canal_district | Barrio de canal | unidades angostas | piedra/madera | tejido urbano | crecidas y accesibilidad |
| sacred_pavilion | Pabellón contemplativo | anillos | estructura ligera | agua/paisaje | apoyos, inundación, viento |

## Contrato de modelo
`schema_version`, `preset`, `units`, `module` (width_m,depth_m,height_m), `levels`, `offsets_m`, `modules` (bounds), `assumptions`, `validation`.

El motor inicial genera **cajas abstractas**. Ninguna es un elemento portante calculado. Estilos artísticos, ornamentos, techos, sistemas MEP y simulaciones quedan fuera de P0.

## Hoja de ruta para generadores avanzados
- Generación de mallas editables Blender mediante adaptador sin alterar el generador residencial.
- Voladizos y envolventes curvas solo con advertencias y análisis posterior.
- Presets separados de validadores; nunca declarar aprobado por lucir físicamente plausible.
