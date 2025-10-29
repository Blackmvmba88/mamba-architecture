# Mamba Architecture - Examples

This folder contains demonstration scripts showcasing the capabilities of the Mamba Architecture framework.

## Available Examples

### 1. Sacred Geometry Demo (`sacred_geometry_demo.py`)

Demonstrates the sacred geometry module with visual examples:

- Golden spiral visualization
- Phyllotaxis (sunflower seed) pattern
- Fibonacci spiral with squares
- All five Platonic solids in 3D
- Flower of Life pattern
- Metatron's Cube

**Usage:**
```bash
python examples/sacred_geometry_demo.py
```

**Output:** PNG images saved to `examples/output/`

**Requirements:** matplotlib

---

### 2. Symbiotic Structure Demo (`symbiotic_structure_demo.py`)

Complete integration example showing all modules working together to design an adaptive pavilion:

**Features:**
- Sacred geometry foundation (Golden Ratio proportions)
- Parametric form generation (shell structure)
- Environmental analysis (solar, wind, thermal)
- Adaptive response system
- Growth simulation (phototropism)
- Equilibrium calculations

**Usage:**
```bash
python examples/symbiotic_structure_demo.py
```

**Output:** Console output with complete design analysis

**What it demonstrates:**
- Phase 1: Sacred geometry foundation
- Phase 2: Parametric form generation
- Phase 3: Environmental analysis (solar, wind, thermal)
- Phase 4: Adaptive response system
- Phase 5: Equilibrium calculations

**Sample Output:**
```
✓ Structure designed using sacred geometry (φ = 1.6180)
✓ Parametric form optimized for 5 support columns
✓ Environmental analysis complete for all conditions
✓ Adaptive response system operational with 3 subsystems
✓ Energy balance factor: 2.2%
✓ Overall comfort: 82.2%
✓ Sustainability index: 98.3%
```

---

## Running the Examples

### Prerequisites

Install required dependencies:
```bash
pip install -r requirements.txt
```

### Creating Output Directory

The sacred geometry demo will automatically create an `output/` directory for generated images.

### Modifying Examples

All examples are designed to be easily modified:

- Change location coordinates for different solar analysis
- Adjust golden ratio parameters
- Modify environmental conditions
- Experiment with different forms and structures

---

## Example Use Cases

### 1. Educational

Use these examples to:
- Learn about sacred geometry principles
- Understand parametric design workflows
- Study environmental simulation
- Explore adaptive architecture concepts

### 2. Research

Extend these examples for:
- Custom form optimization
- Climate-specific designs
- Comparative studies
- Performance analysis

### 3. Professional

Adapt these examples for:
- Client presentations
- Feasibility studies
- Design exploration
- Documentation

---

## Creating Your Own Examples

Template structure:
```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sacred_geometry import GoldenRatio
from src.parametric_design import FormGenerator
# ... import other modules as needed

def your_example():
    """Your example description."""
    # Your code here
    pass

if __name__ == '__main__':
    your_example()
```

---

## Tips

1. **Start Simple**: Begin with `sacred_geometry_demo.py` to understand basic concepts
2. **Visualize**: Use matplotlib to plot and understand results
3. **Experiment**: Modify parameters to see their effects
4. **Integrate**: Combine multiple modules like in `symbiotic_structure_demo.py`
5. **Document**: Add comments explaining your design decisions

---

## Advanced Examples (Coming Soon)

Planned future examples:
- **Genetic Form Evolution**: Evolve building forms over generations
- **Climate Responsive Design**: Adapt to specific climate zones
- **3D Visualization**: Interactive 3D models with Three.js
- **Real-time Adaptation**: Simulate daily/seasonal changes
- **Urban Integration**: Multi-building symbiotic systems

---

## Contributing Examples

Have a great example? Consider contributing:

1. Create a well-documented script
2. Follow the existing code style
3. Include clear output examples
4. Test thoroughly
5. Submit via pull request

---

## Support

For questions or issues:
- Check the main documentation in `/docs`
- Review the code comments
- Examine existing examples
- Experiment with different parameters

---

**"El Núcleo Mamba respira — la arquitectura evoluciona"**
