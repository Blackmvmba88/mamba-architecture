#!/usr/bin/env python3
"""
Example: Golden Spiral Generation for Architectural Design

This example demonstrates how to generate a golden spiral pattern
that can be used for designing curved facades, ramps, or decorative elements.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from geometry.sacred_geometry import SacredGeometry
import math


def main():
    print("=" * 60)
    print("MAMBA ARCHITECTURE - Golden Spiral Example")
    print("=" * 60)
    
    print("\n📐 Golden Ratio and Spiral Properties")
    print("-" * 60)
    print(f"Golden Ratio (φ): {SacredGeometry.PHI:.10f}")
    print(f"Golden Angle: {SacredGeometry.GOLDEN_ANGLE:.6f}°")
    print(f"φ² = {SacredGeometry.PHI**2:.10f}")
    print(f"φ - 1 = 1/φ = {1/SacredGeometry.PHI:.10f}")
    
    # Generate golden spiral
    print("\n🌀 Generating Golden Spiral...")
    turns = 3
    points_per_turn = 50
    spiral_points = SacredGeometry.golden_spiral(turns=turns, points_per_turn=points_per_turn)
    
    print(f"Generated {len(spiral_points)} points")
    print(f"Turns: {turns}")
    print(f"Resolution: {points_per_turn} points per turn")
    
    # Analyze spiral properties
    print("\n📊 Spiral Analysis:")
    
    # Calculate distances at key points
    distances = []
    angles = [0, 90, 180, 270, 360]  # degrees
    for angle in angles:
        idx = int((angle / 360) * points_per_turn)
        if idx < len(spiral_points):
            x, y = spiral_points[idx]
            r = math.sqrt(x**2 + y**2)
            distances.append(r)
            print(f"  At {angle:3d}°: radius = {r:.6f}")
    
    # Verify golden ratio growth
    if len(distances) >= 2:
        print(f"\n✓ Growth verification:")
        for i in range(1, len(distances)):
            if distances[i-1] > 0:
                ratio = distances[i] / distances[i-1]
                print(f"  r({angles[i]}°) / r({angles[i-1]}°) = {ratio:.6f} "
                      f"(expected φ^{(angles[i]-angles[i-1])/90} = "
                      f"{SacredGeometry.PHI**((angles[i]-angles[i-1])/90):.6f})")
    
    # Architectural applications
    print("\n🏛️  Architectural Applications:")
    print("-" * 60)
    applications = [
        "Spiral ramps in multi-story buildings",
        "Curved facade design with optimal proportions",
        "Decorative ceiling patterns",
        "Garden pathways and landscape design",
        "Amphitheater seating arrangements",
        "Water feature spirals and fountains",
        "Lighting fixture designs",
        "Floor tile patterns"
    ]
    
    for i, app in enumerate(applications, 1):
        print(f"  {i}. {app}")
    
    # Example: Scale for building design
    print("\n📏 Practical Scaling Examples:")
    print("-" * 60)
    
    scales = [
        ("Small decorative element", 0.1, "10 cm"),
        ("Interior design feature", 1.0, "1 m"),
        ("Architectural element", 5.0, "5 m"),
        ("Building scale", 20.0, "20 m")
    ]
    
    for name, scale, description in scales:
        final_radius = spiral_points[-1]
        r = math.sqrt(final_radius[0]**2 + final_radius[1]**2) * scale
        print(f"  {name:.<30} {description}")
        print(f"    Final radius: {r:.2f} m")
    
    # Generate Fibonacci spiral for comparison
    print("\n🔄 Fibonacci Spiral (discrete approximation):")
    print("-" * 60)
    fib_arcs = SacredGeometry.fibonacci_spiral(max_size=10)
    print(f"Generated {len(fib_arcs)} quarter-circle arcs")
    
    for i, (cx, cy, radius) in enumerate(fib_arcs[:8], 1):
        fib_num = SacredGeometry.fibonacci(i+1)
        print(f"  Arc {i}: center=({cx:5.1f}, {cy:5.1f}), radius={radius:4} "
              f"(F_{i+1} = {fib_num})")
    
    print("\n" + "=" * 60)
    print("💡 Design Tips:")
    print("   - Use golden spirals for smooth, organic curves")
    print("   - Fibonacci spirals work well for discrete, modular designs")
    print("   - Both create aesthetically pleasing proportions")
    print("   - Scale freely - the ratio remains constant")
    print("=" * 60)


if __name__ == "__main__":
    main()
