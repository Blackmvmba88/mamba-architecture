# Getting Started with Mamba Architecture

## Introducción Rápida

Bienvenido al Núcleo Mamba. Esta guía te ayudará a comenzar a explorar y utilizar las herramientas de diseño arquitectónico inspiradas en la naturaleza.

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Blackmvmba88/mamba-architecture.git
cd mamba-architecture
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Verificar instalación**:
```bash
python3 src/geometry/sacred_geometry.py
```

Si ves información sobre la proporción áurea y la secuencia de Fibonacci, ¡estás listo!

## Tu Primer Diseño

### Ejemplo 1: Generar una Espiral Áurea

```python
from geometry.sacred_geometry import SacredGeometry

# Crear espiral áurea
spiral_points = SacredGeometry.golden_spiral(turns=3, points_per_turn=100)

# Mostrar información
print(f"Generados {len(spiral_points)} puntos")
print(f"Proporción áurea: {SacredGeometry.PHI}")
```

### Ejemplo 2: Diseñar un Árbol Fractal

```python
from fractals.fractal_generator import FractalGenerator

# Generar estructura de árbol
tree_branches = FractalGenerator.fractal_tree(iterations=5, angle=25)

print(f"Estructura con {len(tree_branches)} ramas")
```

### Ejemplo 3: Calcular Ventilación Natural

```python
from flows.natural_flows import FlowSimulator

# Parámetros del edificio
height = 10  # metros
temp_inside = 28  # °C
temp_outside = 22  # °C
temp_avg = (temp_inside + temp_outside) / 2

# Calcular efecto chimenea
pressure = FlowSimulator.chimney_effect_pressure(
    height, temp_inside, temp_outside, temp_avg
)

print(f"Presión del efecto chimenea: {pressure:.2f} Pa")
```

## Explorar Ejemplos Completos

El proyecto incluye ejemplos detallados en la carpeta `examples/`:

```bash
# Espiral áurea
python3 examples/golden_spiral_example.py

# Árbol fractal
python3 examples/fractal_tree_example.py

# Ventilación natural
python3 examples/ventilation_design_example.py
```

## Conceptos Clave

### 1. Geometría Sagrada

La geometría sagrada utiliza proporciones universales encontradas en la naturaleza:

- **φ (Phi)**: La proporción áurea (≈1.618)
- **Fibonacci**: Secuencia donde cada número es la suma de los dos anteriores
- **Espiral Áurea**: Curva que crece por un factor φ en cada rotación

**Aplicaciones**:
- Proporciones de espacios arquitectónicos
- Diseño de fachadas y ventanas
- Patrones decorativos

### 2. Fractales

Los fractales son patrones que se repiten a diferentes escalas:

- **Autosimilitud**: Pequeñas partes se parecen al todo
- **Eficiencia**: Máxima superficie en mínimo espacio
- **Naturalidad**: Apariencia orgánica y atractiva

**Aplicaciones**:
- Estructuras de soporte ramificadas
- Sistemas de ventilación eficientes
- Decoración con patrones naturales

### 3. Flujos Naturales

El diseño trabaja con flujos de aire, agua, luz y calor:

- **Ventilación pasiva**: Sin consumo eléctrico
- **Iluminación natural**: Aprovechamiento de luz solar
- **Gestión de agua**: Recolección y drenaje inteligente
- **Control térmico**: Enfriamiento y calentamiento natural

**Aplicaciones**:
- Edificios de bajo consumo energético
- Espacios confortables sin climatización artificial
- Integración con el entorno

## Estructura del Proyecto

```
mamba-architecture/
├── src/                    # Código fuente
│   ├── geometry/          # Geometría sagrada
│   ├── fractals/          # Generadores de fractales
│   ├── flows/             # Simulación de flujos
│   └── materials/         # (Futuro) Materiales inteligentes
├── examples/              # Ejemplos prácticos
├── docs/                  # Documentación detallada
└── README.md              # Descripción general
```

## Próximos Pasos

1. **Explorar la Documentación**:
   - Lee [MANIFESTO.md](../MANIFESTO.md) para entender la filosofía
   - Estudia los documentos técnicos en `docs/`

2. **Experimentar con los Módulos**:
   - Modifica parámetros en los ejemplos
   - Crea tus propios diseños

3. **Aplicar a Proyectos Reales**:
   - Usa las herramientas en diseños arquitectónicos
   - Calcula ventilación para edificios reales
   - Genera patrones para fachadas

4. **Contribuir**:
   - Comparte tus diseños
   - Mejora el código
   - Añade nuevas funcionalidades

## Recursos Adicionales

- **[PHILOSOPHY.md](PHILOSOPHY.md)**: Fundamentos filosóficos
- **[SACRED_GEOMETRY.md](SACRED_GEOMETRY.md)**: Geometría en detalle
- **[FRACTAL_BIOLOGY.md](FRACTAL_BIOLOGY.md)**: Fractales y biomimética
- **[NATURAL_FLOWS.md](NATURAL_FLOWS.md)**: Flujos naturales
- **[INTELLIGENT_MATERIALS.md](INTELLIGENT_MATERIALS.md)**: Materiales avanzados

## Preguntas Frecuentes

### ¿Necesito ser arquitecto para usar esto?

No. El proyecto es útil para:
- Arquitectos y diseñadores
- Estudiantes de arquitectura
- Artistas digitales
- Entusiastas de la geometría
- Cualquiera interesado en diseño natural

### ¿Puedo usar esto en proyectos comerciales?

Consulta el archivo LICENSE. El espíritu del proyecto es la colaboración abierta.

### ¿Cómo puedo visualizar los resultados?

Los módulos generan datos numéricos. Puedes:
- Usar matplotlib para gráficos 2D
- Exportar a software CAD (Rhino, Grasshopper)
- Integrar con herramientas de visualización 3D

### ¿Hay soporte para diseño 3D?

Actualmente los módulos son principalmente 2D y cálculos. El desarrollo 3D está planificado.

## Obtener Ayuda

- **Issues**: Abre un issue en GitHub
- **Documentación**: Lee los archivos en `docs/`
- **Ejemplos**: Estudia el código en `examples/`

---

¡Bienvenido a la exploración de la arquitectura viva! 🐍✨

*"El primer paso para crear algo vivo es aprender el lenguaje de la vida"*
