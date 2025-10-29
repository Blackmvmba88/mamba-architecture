#!/usr/bin/env python3
"""
Sacred Geometry Demo - Examples of sacred geometric patterns.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from src.sacred_geometry import GoldenRatio, FibonacciSequence, PlatonicSolids, SacredPatterns


def demo_golden_spiral():
    """Demonstrate golden spiral."""
    print("=== Golden Spiral ===")
    
    # Generate golden spiral points
    points = GoldenRatio.golden_spiral_points(num_turns=4, points_per_turn=100)
    
    # Plot
    plt.figure(figsize=(8, 8))
    plt.plot(points[:, 0], points[:, 1], 'b-', linewidth=2)
    plt.scatter(points[0, 0], points[0, 1], c='r', s=100, zorder=5, label='Start')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.title('Golden Spiral (φ = 1.618...)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('examples/output/golden_spiral.png', dpi=150)
    print("Saved: examples/output/golden_spiral.png")
    plt.close()


def demo_phyllotaxis():
    """Demonstrate phyllotaxis pattern."""
    print("\n=== Phyllotaxis Pattern ===")
    
    # Generate phyllotaxis (sunflower) pattern
    points = GoldenRatio.phyllotaxis_pattern(n_points=500, scale=1.0)
    
    # Plot
    plt.figure(figsize=(8, 8))
    colors = np.arange(len(points))
    plt.scatter(points[:, 0], points[:, 1], c=colors, cmap='viridis', s=20, alpha=0.6)
    plt.axis('equal')
    plt.title('Phyllotaxis Pattern (Sunflower Seeds)')
    plt.colorbar(label='Sequence')
    plt.tight_layout()
    plt.savefig('examples/output/phyllotaxis.png', dpi=150)
    print("Saved: examples/output/phyllotaxis.png")
    plt.close()


def demo_fibonacci_spiral_squares():
    """Demonstrate Fibonacci spiral with squares."""
    print("\n=== Fibonacci Spiral Squares ===")
    
    # Generate Fibonacci numbers
    fib = FibonacciSequence.generate(10)
    print(f"Fibonacci sequence: {fib}")
    
    # Generate squares
    squares = FibonacciSequence.fibonacci_spiral_squares(8)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for sq in squares:
        rect = plt.Rectangle((sq['x'], sq['y']), sq['size'], sq['size'],
                            fill=False, edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        ax.text(sq['x'] + sq['size']/2, sq['y'] + sq['size']/2, 
               str(sq['size']), ha='center', va='center', fontsize=12)
    
    ax.set_aspect('equal')
    ax.autoscale()
    ax.grid(True, alpha=0.3)
    ax.set_title('Fibonacci Spiral Squares')
    plt.tight_layout()
    plt.savefig('examples/output/fibonacci_squares.png', dpi=150)
    print("Saved: examples/output/fibonacci_squares.png")
    plt.close()


def demo_platonic_solids():
    """Demonstrate Platonic solids."""
    print("\n=== Platonic Solids ===")
    
    solids = PlatonicSolids.all_solids()
    
    fig = plt.figure(figsize=(15, 10))
    
    for idx, solid in enumerate(solids):
        ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
        
        vertices = solid['vertices']
        faces = solid['faces']
        
        # Plot vertices
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                  c='blue', s=50, alpha=0.6)
        
        # Plot edges (connect face vertices)
        for face in faces:
            face_verts = vertices[face]
            # Close the face
            face_verts = np.vstack([face_verts, face_verts[0]])
            ax.plot(face_verts[:, 0], face_verts[:, 1], face_verts[:, 2], 
                   'b-', linewidth=1, alpha=0.6)
        
        ax.set_title(f"{solid['name']}\n({solid['element']})")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Equal aspect ratio
        max_range = 1.5
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
    
    plt.tight_layout()
    plt.savefig('examples/output/platonic_solids.png', dpi=150)
    print("Saved: examples/output/platonic_solids.png")
    plt.close()


def demo_flower_of_life():
    """Demonstrate Flower of Life pattern."""
    print("\n=== Flower of Life ===")
    
    # Generate pattern
    centers = SacredPatterns.flower_of_life(radius=1.0, rings=3)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for center in centers:
        circle = plt.Circle(center, 1.0, fill=False, edgecolor='blue', linewidth=1.5)
        ax.add_patch(circle)
    
    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, alpha=0.3)
    ax.set_title('Flower of Life Pattern')
    plt.tight_layout()
    plt.savefig('examples/output/flower_of_life.png', dpi=150)
    print("Saved: examples/output/flower_of_life.png")
    plt.close()


def demo_metatrons_cube():
    """Demonstrate Metatron's Cube."""
    print("\n=== Metatron's Cube ===")
    
    # Generate pattern
    cube = SacredPatterns.metatrons_cube(radius=1.0)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    
    vertices = cube['vertices']
    connections = cube['connections']
    
    # Draw connections
    for conn in connections:
        v1, v2 = vertices[conn[0]], vertices[conn[1]]
        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], 'b-', linewidth=0.5, alpha=0.6)
    
    # Draw vertices
    for v in vertices:
        ax.plot(v[0], v[1], 'ro', markersize=8)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title("Metatron's Cube")
    plt.tight_layout()
    plt.savefig('examples/output/metatrons_cube.png', dpi=150)
    print("Saved: examples/output/metatrons_cube.png")
    plt.close()


def main():
    """Run all demonstrations."""
    print("Mamba Architecture - Sacred Geometry Demo\n")
    print("=" * 50)
    
    # Create output directory
    os.makedirs('examples/output', exist_ok=True)
    
    # Run demonstrations
    demo_golden_spiral()
    demo_phyllotaxis()
    demo_fibonacci_spiral_squares()
    demo_platonic_solids()
    demo_flower_of_life()
    demo_metatrons_cube()
    
    print("\n" + "=" * 50)
    print("All demonstrations complete!")
    print("Check examples/output/ for generated images.")


if __name__ == '__main__':
    main()
