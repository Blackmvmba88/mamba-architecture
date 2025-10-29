# Mamba Architecture 🐍✨

**Proyecto experimental del Núcleo Mamba: Arte, Ciencia y Arquitectura Viva**

Arquitectura simbiótica inspirada en la geometría sagrada, biología fractal y flujos naturales. Diseñamos estructuras inteligentes que respiran con la luz, evolucionan con su entorno y expresan conciencia arquitectónica.

---

## 🌟 Visión

El Núcleo Mamba trasciende los límites tradicionales de la arquitectura, fusionando:

- **🎨 Arte**: Formas que evocan emoción y conexión espiritual
- **🔬 Ciencia**: Simulación computacional y biomimética
- **🏛️ Arquitectura Viva**: Estructuras que respiran, sienten y evolucionan

No construimos objetos estáticos. Creamos ecosistemas arquitectónicos conscientes.

---

## 📚 Documentación

### Fundamentos Filosóficos

- **[MANIFESTO.md](MANIFESTO.md)** - Visión, principios y metodología del proyecto
- **[docs/PHILOSOPHY.md](docs/PHILOSOPHY.md)** - Filosofía profunda y conceptos fundamentales

### Pilares Técnicos

1. **[docs/SACRED_GEOMETRY.md](docs/SACRED_GEOMETRY.md)** - Geometría sagrada y proporciones universales
2. **[docs/FRACTAL_BIOLOGY.md](docs/FRACTAL_BIOLOGY.md)** - Patrones fractales inspirados en la naturaleza
3. **[docs/NATURAL_FLOWS.md](docs/NATURAL_FLOWS.md)** - Flujos de aire, agua, luz y calor
4. **[docs/INTELLIGENT_MATERIALS.md](docs/INTELLIGENT_MATERIALS.md)** - Materiales que responden y adaptan

---

## 🛠️ Módulos del Proyecto

### 1. Sacred Geometry (`src/geometry/`)

Implementación de patrones geométricos universales:

- **Proporción Áurea (φ)** y Secuencia de Fibonacci
- **Espirales** (dorada, Fibonacci, Arquímedes)
- **Sólidos Platónicos** (tetraedro, cubo, octaedro, dodecaedro, icosaedro)
- **Flor de la Vida** y patrones de círculos sagrados
- **Phyllotaxis** (distribución de semillas tipo girasol)

```python
from geometry.sacred_geometry import SacredGeometry

# Generar espiral áurea
spiral = SacredGeometry.golden_spiral(turns=3, points_per_turn=100)

# Secuencia de Fibonacci
fib = SacredGeometry.fibonacci_sequence(15)

# Vértices de sólido platónico
icosahedron = SacredGeometry.platonic_solid_vertices('icosahedron')
```

### 2. Fractal Biology (`src/fractals/`)

Generación de patrones fractales biomiméticos:

- **Curva de Koch** (copo de nieve)
- **Triángulo de Sierpinski**
- **Sistemas L** (Lindenmayer) para crecimiento de plantas
- **Árboles fractales** ramificados
- **Curva del Dragón**
- **DLA** (Diffusion Limited Aggregation)
- **Helecho de Barnsley** (IFS)
- **Conjunto de Mandelbrot**

```python
from fractals.fractal_generator import FractalGenerator

# Árbol fractal para estructuras de soporte
tree = FractalGenerator.fractal_tree(iterations=5, angle=30)

# Crecimiento de planta con L-System
plant = FractalGenerator.plant_growth(iterations=4, angle=25)

# Helecho para ornamentación
fern = FractalGenerator.barnsley_fern(n_points=10000)
```

### 3. Natural Flows (`src/flows/`)

Simulación de flujos naturales en arquitectura:

#### Flujo de Aire
- Efecto chimenea (stack effect)
- Ventilación natural y cruzada
- Número de Reynolds (laminar vs turbulento)
- Presión del viento

#### Flujo de Agua
- Ecuación de Bernoulli
- Capilaridad
- Recolección de agua pluvial
- Drenaje

#### Flujo de Luz
- Factor de luz natural
- Penetración de luz diurna
- Reflexión y refracción
- Posición solar

#### Flujo de Calor
- Conducción, convección, radiación
- Masa térmica
- Enfriamiento evaporativo
- Valor U de muros

```python
from flows.natural_flows import FlowSimulator, WaterFlow, LightFlow, HeatFlow

# Calcular ventilación natural
pressure = FlowSimulator.chimney_effect_pressure(height=10, temp_inside=25, temp_outside=15, avg_temp=20)
flow_rate = FlowSimulator.natural_ventilation_flow_rate(pressure, opening_area=2.0)

# Recolección de agua de lluvia
water = WaterFlow.rainfall_catchment(area=100, rainfall=50)  # 100m², 50mm

# Factor de luz natural
df = LightFlow.daylight_factor(indoor_illuminance=500, outdoor_illuminance=10000)

# Enfriamiento evaporativo
cooling = HeatFlow.evaporative_cooling_potential(air_temp=35, relative_humidity=0.3)
```

---

## 🎯 Ejemplos Prácticos

### Ejecutar Ejemplos

```bash
# Espiral áurea para diseño de fachadas
python3 examples/golden_spiral_example.py

# Árbol fractal para estructuras de soporte
python3 examples/fractal_tree_example.py

# Calculadora de ventilación natural
python3 examples/ventilation_design_example.py
```

### Salida de Ejemplo: Golden Spiral

```
==============================================================
MAMBA ARCHITECTURE - Golden Spiral Example
==============================================================

📐 Golden Ratio and Spiral Properties
--------------------------------------------------------------
Golden Ratio (φ): 1.6180339887
Golden Angle: 137.507764°

🌀 Generating Golden Spiral...
Generated 150 points
Turns: 3
Resolution: 50 points per turn

🏛️  Architectural Applications:
--------------------------------------------------------------
  1. Spiral ramps in multi-story buildings
  2. Curved facade design with optimal proportions
  3. Decorative ceiling patterns
  4. Garden pathways and landscape design
  ...
```

---

## 📦 Instalación y Dependencias

### Requisitos

- Python 3.7+
- NumPy

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Blackmvmba88/mamba-architecture.git
cd mamba-architecture

# Instalar dependencias
pip install numpy

# Ejecutar módulos directamente
python3 src/geometry/sacred_geometry.py
python3 src/fractals/fractal_generator.py
python3 src/flows/natural_flows.py
```

---

## 🎨 Aplicaciones Arquitectónicas

### Geometría Sagrada
- Proporciones de espacios y fachadas
- Distribución de ventanas
- Patrones de pisos y mosaicos
- Diseño de cúpulas geodésicas

### Fractales
- Estructuras de soporte ramificadas (columnas, vigas)
- Fachadas verdes con crecimiento orgánico
- Sistemas de ventilación biomiméticos
- Patrones decorativos naturales

### Flujos Naturales
- Ventilación pasiva sin consumo energético
- Enfriamiento natural con evaporación
- Maximización de luz natural
- Gestión inteligente de agua pluvial

### Materiales Inteligentes
- Ventanas que se tintean con el sol
- Concreto auto-regenerable
- Materiales con memoria de forma
- Superficies fotocatalíticas que limpian el aire

---

## 🌍 Casos de Uso

1. **Torres de Enfriamiento**: Fractales para maximizar superficie de intercambio
2. **Sistemas de Soporte**: Columnas ramificadas que distribuyen carga como árboles
3. **Fachadas Respiratorias**: Piel permeable que regula luz, aire y temperatura
4. **Jardines Verticales**: Crecimiento basado en L-Systems
5. **Captación de Agua**: Redes fractales de recolección
6. **Iluminación Natural**: Geometría áurea para reflectores de luz

---

## 🤝 Contribuir

Este es un proyecto experimental abierto. Invitamos a:

- **Arquitectos** - Aportar experiencia en diseño y construcción
- **Científicos** - Mejorar simulaciones y modelos
- **Artistas** - Expandir la dimensión estética y simbólica
- **Ingenieros** - Implementar sistemas reales
- **Soñadores** - Imaginar nuevas posibilidades

### Áreas de Desarrollo

- [ ] Visualización 3D de patrones generados
- [ ] Simulación CFD completa
- [ ] Integración con software CAD (Rhino/Grasshopper)
- [ ] Base de datos de materiales inteligentes
- [ ] Casos de estudio de proyectos reales
- [ ] Optimización estructural con algoritmos genéticos

---

## 📖 Inspiraciones

### Naturaleza
- Nidos de termitas (climatización natural)
- Esqueletos de radiolarios (geometría microscópica)
- Redes miceliales de hongos
- Nautilus y espirales de caracoles

### Ciencia
- Teoría del caos y sistemas emergentes
- Morfogénesis de Alan Turing
- Estructuras disipativas de Ilya Prigogine
- Autopoiesis de Maturana y Varela

### Arte
- Escultura cinética de Theo Jansen
- Arte generativo de Casey Reas
- Instalaciones de luz de James Turrell
- Bio-arte de Eduardo Kac

---

## 📜 Licencia

Este proyecto se comparte con el espíritu de colaboración abierta. Consulta LICENSE para detalles.

---

## 🌈 Filosofía

> *"No construimos para la eternidad, construimos para el diálogo con el eterno presente"*

> *"La arquitectura no es un objeto, es una conversación con el tiempo y el espacio"*

> *"La materia no es inerte. Cuando aprendemos su lenguaje, descubrimos que todo está vivo"*

---

## 📞 Contacto

**Núcleo Mamba** - Donde el arte, la ciencia y la arquitectura se encuentran con la conciencia.

---

*Parte del ecosistema Mamba: equilibrio entre tecnología, naturaleza y espíritu* 🐍✨🌿
