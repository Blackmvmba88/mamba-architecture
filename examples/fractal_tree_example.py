#!/usr/bin/env python3
"""
Example: Fractal Tree Structure for Architectural Support Systems

This example demonstrates how to generate fractal tree patterns
that can be used for designing efficient branching support structures.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fractals.fractal_generator import FractalGenerator


def main():
    print("=" * 60)
    print("MAMBA ARCHITECTURE - Fractal Tree Example")
    print("=" * 60)
    
    print("\n🌳 Generating Fractal Tree Structure")
    print("-" * 60)
    
    # Generate tree at different depths
    iterations = [2, 3, 4, 5]
    
    for iter_depth in iterations:
        tree = FractalGenerator.fractal_tree(iterations=iter_depth, angle=25)
        print(f"\nIteration {iter_depth}:")
        print(f"  Branches: {len(tree)}")
        print(f"  Complexity: {'█' * min(len(tree) // 10, 50)}")
    
    # Detailed analysis for depth 4
    print("\n" + "=" * 60)
    print("📊 Detailed Analysis (Depth 4)")
    print("=" * 60)
    
    tree = FractalGenerator.fractal_tree(iterations=4, angle=25)
    
    # Calculate total length
    total_length = 0
    min_y = float('inf')
    max_y = float('-inf')
    
    for (x1, y1), (x2, y2) in tree:
        length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        total_length += length
        min_y = min(min_y, y1, y2)
        max_y = max(max_y, y1, y2)
    
    height = max_y - min_y
    
    print(f"Total branches: {len(tree)}")
    print(f"Total length: {total_length:.2f} units")
    print(f"Tree height: {height:.2f} units")
    print(f"Efficiency ratio: {total_length / height:.2f}")
    
    # Architectural applications
    print("\n🏛️  Architectural Applications")
    print("-" * 60)
    
    applications = [
        ("Column Support System", 
         "Branching columns that distribute load like tree trunks",
         "Reduces material while maintaining strength"),
        
        ("Roof Structure", 
         "Fractal truss system for large spans",
         "Efficient load distribution with minimal weight"),
        
        ("Facade Framework",
         "Organic branching pattern for green walls",
         "Natural appearance with structural function"),
        
        ("Ventilation Network",
         "Biomimetic air distribution system",
         "Maximizes air flow with minimal ductwork"),
        
        ("Lightning Rod System",
         "Fractal antenna for expanded coverage",
         "Increased surface area for charge dissipation"),
        
        ("Drainage System",
         "Tree-like water collection network",
         "Efficient gathering from multiple points")
    ]
    
    for i, (name, description, benefit) in enumerate(applications, 1):
        print(f"\n{i}. {name}")
        print(f"   Description: {description}")
        print(f"   Benefit: {benefit}")
    
    # Scaling examples
    print("\n" + "=" * 60)
    print("📏 Scaling for Real-World Implementation")
    print("=" * 60)
    
    scales = [
        ("Interior column", 3.5, "m"),
        ("Building facade element", 10, "m"),
        ("Structural roof support", 25, "m"),
        ("Monument/sculpture", 50, "m")
    ]
    
    base_height = height
    for name, target_height, unit in scales:
        scale_factor = target_height / base_height
        scaled_total = total_length * scale_factor
        
        print(f"\n{name}:")
        print(f"  Target height: {target_height} {unit}")
        print(f"  Scale factor: {scale_factor:.2f}x")
        print(f"  Total branch length: {scaled_total:.2f} {unit}")
        print(f"  Material efficiency: {scaled_total / target_height:.2f}x height")
    
    # Comparison with different branching angles
    print("\n" + "=" * 60)
    print("🔄 Effect of Branching Angle")
    print("=" * 60)
    
    angles = [15, 20, 25, 30, 35, 40]
    
    print(f"{'Angle':<8} {'Branches':<10} {'Compactness'}")
    print("-" * 40)
    
    for angle in angles:
        tree_a = FractalGenerator.fractal_tree(iterations=4, angle=angle)
        
        # Calculate spread
        x_coords = []
        for (x1, y1), (x2, y2) in tree_a:
            x_coords.extend([x1, x2])
        
        spread = max(x_coords) - min(x_coords) if x_coords else 0
        compactness = "Narrow" if spread < 50 else "Medium" if spread < 100 else "Wide"
        
        print(f"{angle:>4}°    {len(tree_a):<10} {compactness}")
    
    print("\n💡 Design Guidelines:")
    print("   - Smaller angles (15-25°): Tall, narrow structures")
    print("   - Medium angles (25-35°): Balanced distribution")
    print("   - Larger angles (35-45°): Wide, spreading canopy")
    
    # L-System used
    print("\n" + "=" * 60)
    print("🧬 L-System Grammar")
    print("=" * 60)
    print("Axiom: F")
    print("Rule:  F → FF+[+F-F-F]-[-F+F+F]")
    print("\nSymbol meanings:")
    print("  F : Move forward and draw")
    print("  + : Turn right by angle")
    print("  - : Turn left by angle")
    print("  [ : Push position (branch start)")
    print("  ] : Pop position (return to branch point)")
    
    print("\n" + "=" * 60)
    print("🌿 Biomimetic Inspiration")
    print("-" * 60)
    print("This fractal pattern mimics:")
    print("  • Tree branching (optimize light capture)")
    print("  • River deltas (efficient drainage)")
    print("  • Blood vessels (maximize distribution)")
    print("  • Lightning paths (minimize resistance)")
    print("  • Root systems (explore and anchor)")
    print("\nNature uses these patterns for efficiency!")
    print("=" * 60)


if __name__ == "__main__":
    main()
