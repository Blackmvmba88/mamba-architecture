#!/usr/bin/env python3
"""
Quick Demo - Mamba Architecture

A rapid demonstration of all major features of the Mamba Architecture framework.
Run this to verify installation and see basic functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from geometry.sacred_geometry import SacredGeometry
from fractals.fractal_generator import FractalGenerator
from flows.natural_flows import FlowSimulator, WaterFlow, LightFlow, HeatFlow


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_sacred_geometry():
    """Demonstrate sacred geometry features."""
    print_section("1. SACRED GEOMETRY")
    
    print(f"\n✨ Golden Ratio (φ): {SacredGeometry.PHI:.10f}")
    print(f"   Golden Angle: {SacredGeometry.GOLDEN_ANGLE:.4f}°")
    
    # Fibonacci
    fib = SacredGeometry.fibonacci_sequence(10)
    print(f"\n📐 Fibonacci sequence: {fib}")
    
    # Golden spiral
    spiral = SacredGeometry.golden_spiral(turns=2, points_per_turn=50)
    print(f"   Golden spiral: {len(spiral)} points generated")
    
    # Platonic solids
    print(f"\n🔷 Platonic Solids:")
    for solid in ['tetrahedron', 'cube', 'octahedron']:
        vertices = SacredGeometry.platonic_solid_vertices(solid)
        print(f"   - {solid.capitalize()}: {len(vertices)} vertices")
    
    # Flower of Life
    circles = SacredGeometry.flower_of_life(radius=1.0, generations=2)
    print(f"\n🌸 Flower of Life: {len(circles)} circles (2 generations)")
    
    print("\n💡 Use these patterns for architectural proportions and design")


def demo_fractals():
    """Demonstrate fractal generation."""
    print_section("2. FRACTAL PATTERNS")
    
    # Koch curve
    koch = FractalGenerator.koch_curve(order=3)
    print(f"\n❄️  Koch Snowflake: {len(koch)} points")
    
    # Sierpinski
    sierpinski = FractalGenerator.sierpinski_triangle(order=4)
    print(f"△  Sierpinski Triangle: {len(sierpinski)} triangles")
    
    # Fractal tree
    tree = FractalGenerator.fractal_tree(iterations=4, angle=25)
    print(f"🌳 Fractal Tree: {len(tree)} branches")
    
    # Plant growth
    plant = FractalGenerator.plant_growth(iterations=3)
    print(f"🌿 Plant Pattern: {len(plant)} segments")
    
    # Barnsley fern
    fern = FractalGenerator.barnsley_fern(n_points=1000)
    print(f"🍃 Barnsley Fern: {len(fern)} points")
    
    print("\n💡 Use fractals for structural efficiency and natural aesthetics")


def demo_natural_flows():
    """Demonstrate natural flow calculations."""
    print_section("3. NATURAL FLOWS")
    
    # Airflow
    print("\n🌬️  Air Flow:")
    height, temp_in, temp_out = 10, 28, 20
    temp_avg = (temp_in + temp_out) / 2
    pressure = FlowSimulator.chimney_effect_pressure(height, temp_in, temp_out, temp_avg)
    flow = FlowSimulator.natural_ventilation_flow_rate(pressure, opening_area=2.0)
    print(f"   Stack effect pressure: {pressure:.2f} Pa")
    print(f"   Natural ventilation: {flow:.2f} m³/s")
    
    # Water
    print("\n💧 Water Flow:")
    collected = WaterFlow.rainfall_catchment(area=100, rainfall=50)
    print(f"   Rainfall collection (100m², 50mm): {collected:.0f} liters")
    
    capillary = WaterFlow.capillary_rise(0.073, 0, 0.001)
    print(f"   Capillary rise (1mm tube): {capillary*1000:.1f} mm")
    
    # Light
    print("\n☀️  Light:")
    df = LightFlow.daylight_factor(500, 10000)
    print(f"   Daylight factor: {df:.1f}%")
    
    penetration = LightFlow.penetration_depth(window_height=2.0)
    print(f"   Light penetration (2m window): {penetration:.1f} m")
    
    altitude = LightFlow.solar_altitude(latitude=40, day_of_year=172, hour=12)
    print(f"   Solar altitude (noon, summer): {altitude:.1f}°")
    
    # Heat
    print("\n🔥 Heat Transfer:")
    cooling = HeatFlow.evaporative_cooling_potential(35, 0.3)
    print(f"   Evaporative cooling (35°C, 30% RH): {cooling:.1f}°C reduction")
    
    u_value = HeatFlow.u_value([0.01, 0.10, 0.01], [0.5, 0.04, 0.5])
    print(f"   Wall U-value (insulated): {u_value:.3f} W/(m²·K)")
    
    print("\n💡 Design passive buildings with natural climate control")


def demo_applications():
    """Show practical applications."""
    print_section("4. ARCHITECTURAL APPLICATIONS")
    
    applications = [
        ("🏛️  Structural", [
            "Fractal columns that distribute load efficiently",
            "Branching roof trusses with minimal material",
            "Golden ratio proportions for aesthetic balance"
        ]),
        ("🌱 Living Facades", [
            "L-system patterns for plant growth paths",
            "Fractal irrigation networks",
            "Natural ventilation through porous design"
        ]),
        ("☀️  Climate Control", [
            "Stack effect for natural ventilation",
            "Evaporative cooling with water features",
            "Daylight optimization using golden proportions"
        ]),
        ("💧 Water Management", [
            "Fractal collection networks",
            "Capillary irrigation systems",
            "Rainwater harvesting calculations"
        ])
    ]
    
    for category, items in applications:
        print(f"\n{category}")
        for item in items:
            print(f"  • {item}")


def main():
    """Run complete demonstration."""
    print("\n" + "█" * 70)
    print("  MAMBA ARCHITECTURE - Quick Demo")
    print("  Art • Science • Living Architecture")
    print("█" * 70)
    
    try:
        demo_sacred_geometry()
        demo_fractals()
        demo_natural_flows()
        demo_applications()
        
        print_section("✅ DEMO COMPLETE")
        print("\nAll modules working correctly!")
        print("\nNext steps:")
        print("  1. Explore detailed examples in examples/")
        print("  2. Read documentation in docs/")
        print("  3. Import modules in your own projects")
        print("  4. Create beautiful, living architecture! 🐍✨")
        print("\n" + "█" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check installation and dependencies.")
        return 1


if __name__ == "__main__":
    exit(main())
