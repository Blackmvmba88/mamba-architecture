# Getting Started - Mamba Architecture

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Blackmvmba88/mamba-architecture.git
cd mamba-architecture
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Test the installation:
```bash
python examples/sacred_geometry_demo.py
```

---

## Quick Start Guide

### 1. Sacred Geometry

Create geometric patterns with sacred proportions:

```python
from src.sacred_geometry import GoldenRatio, FibonacciSequence, PlatonicSolids

# Golden spiral
spiral_points = GoldenRatio.golden_spiral_points(num_turns=4)

# Fibonacci sequence
fib_numbers = FibonacciSequence.generate(10)

# Platonic solids
tetrahedron = PlatonicSolids.tetrahedron()
```

### 2. Parametric Design

Generate organic forms algorithmically:

```python
from src.parametric_design import FormGenerator, SurfaceGenerator

# Create a torus
torus = FormGenerator.torus(major_radius=2.0, minor_radius=0.5)

# Generate minimal surface
gyroid = SurfaceGenerator.gyroid_surface(resolution=50)
```

### 3. Environmental Simulation

Analyze environmental conditions:

```python
from src.environmental_simulation import SolarCalculator, LightAnalysis
from datetime import datetime

# Calculate sun position
solar_calc = SolarCalculator()
position = solar_calc.solar_position(
    latitude=40.7128,
    longitude=-74.0060,
    date_time=datetime.now()
)

# Analyze solar irradiance
irradiance = LightAnalysis.calculate_irradiance(
    altitude=position['altitude'],
    azimuth=position['azimuth'],
    surface_normal=[0, 0, 1]
)
```

### 4. Organic Models

Create models that grow and evolve:

```python
from src.organic_models import GrowthRules, OrganicMorphology

# Simulate phototropism
new_direction = GrowthRules.phototropism(
    current_direction=[0, 1, 0],
    light_direction=[1, 1, 1],
    strength=0.3
)

# Generate organic blob
blob = OrganicMorphology.blob_surface(
    center=[0, 0, 0],
    radius=1.0,
    irregularity=0.2
)
```

### 5. Procedural Generation

Generate structures procedurally:

```python
from src.procedural_generation import GeneticFormOptimizer, NoiseGenerator

# Optimize form with genetic algorithm
def fitness_func(genome):
    # Define your fitness criteria
    return sum(genome)

optimizer = GeneticFormOptimizer(population_size=50)
result = optimizer.optimize(
    genome_length=10,
    fitness_func=fitness_func,
    generations=100
)

# Generate Perlin noise
noise = NoiseGenerator.perlin_noise_2d(shape=(256, 256))
```

### 6. Symbiotic Structures

Create adaptive, responsive structures:

```python
from src.symbiotic_structures import AdaptiveSystem, EquilibriumCalculator

# Create adaptive system
adaptive = AdaptiveSystem()

# Respond to environmental conditions
environmental_state = {
    'temperature': 28,
    'target_temp': 22,
    'thermal_mass': 1.5,
    'illuminance': 800,
    'target_illuminance': 500,
    'sun_altitude': 45
}

adaptations = adaptive.integrated_adaptation(environmental_state)

# Calculate energy balance
balance = EquilibriumCalculator.energy_balance(
    solar_gain=500,
    internal_gain=200,
    heat_loss=600,
    target_temp=22,
    current_temp=24
)
```

---

## Examples

### Run Example Demonstrations

```bash
# Sacred geometry visualization
python examples/sacred_geometry_demo.py

# Check output in examples/output/
```

### Export 3D Models

```python
from src.organic_models import MeshExporter
import numpy as np

# Create simple mesh
vertices = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]])
faces = np.array([[0,1,2], [0,1,3], [0,2,3], [1,2,3]])

# Export to OBJ
MeshExporter.to_obj(vertices, faces, 'model.obj')

# Export to STL
MeshExporter.to_stl(vertices, faces, 'model.stl')

# Export to glTF
MeshExporter.to_gltf(vertices, faces, 'model.gltf')
```

---

## Module Overview

### Sacred Geometry (`src/sacred_geometry/`)
- **golden_ratio.py**: Golden ratio calculations and spirals
- **fibonacci.py**: Fibonacci sequence and ratios
- **platonic_solids.py**: The five Platonic solids
- **sacred_patterns.py**: Flower of Life, Metatron's Cube, etc.

### Parametric Design (`src/parametric_design/`)
- **form_generator.py**: Parametric form generation
- **surface_generator.py**: Advanced surface algorithms
- **structure_optimizer.py**: Structural optimization

### Environmental Simulation (`src/environmental_simulation/`)
- **solar_calculator.py**: Sun position and trajectory
- **light_analysis.py**: Natural light analysis
- **wind_simulation.py**: Wind flow simulation
- **thermal_analysis.py**: Thermal behavior analysis

### Organic Models (`src/organic_models/`)
- **growth_rules.py**: Biological growth patterns
- **morphology.py**: Organic form generation
- **mesh_export.py**: 3D file format export

### Procedural Generation (`src/procedural_generation/`)
- **genetic_algorithm.py**: Evolutionary optimization
- **noise_generator.py**: Perlin and Worley noise
- **rule_system.py**: L-systems and cellular automata

### Symbiotic Structures (`src/symbiotic_structures/`)
- **adaptive_system.py**: Environmental adaptation
- **equilibrium.py**: Balance and stability
- **response_behavior.py**: Behavioral responses

---

## Next Steps

1. **Explore Examples**: Run the example scripts to see the system in action
2. **Read Documentation**: Check the `docs/` folder for detailed guides
3. **Experiment**: Modify parameters and create your own designs
4. **Contribute**: Share your creations and improvements

---

## Resources

- [ROADMAP.md](../ROADMAP.md) - Development roadmap
- [README.md](../README.md) - Project overview
- Examples folder - Working code examples

---

**"El Núcleo Mamba respira — la arquitectura evoluciona"**
