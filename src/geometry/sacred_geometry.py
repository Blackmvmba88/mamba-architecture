"""
Sacred Geometry Module for Mamba Architecture

This module implements mathematical functions and generators for sacred geometry
patterns used in architectural design.
"""

import math
import numpy as np
from typing import List, Tuple, Optional


class SacredGeometry:
    """Collection of sacred geometry constants and functions."""
    
    # Constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio: 1.618033988749895
    GOLDEN_ANGLE = 360 / (PHI ** 2)  # 137.5077640500378 degrees
    PI = math.pi
    
    @staticmethod
    def fibonacci(n: int) -> int:
        """
        Generate the nth Fibonacci number.
        
        Args:
            n: Position in Fibonacci sequence (0-indexed)
            
        Returns:
            The nth Fibonacci number
        """
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def fibonacci_sequence(n: int) -> List[int]:
        """
        Generate Fibonacci sequence up to n terms.
        
        Args:
            n: Number of terms to generate
            
        Returns:
            List of Fibonacci numbers
        """
        if n <= 0:
            return []
        if n == 1:
            return [0]
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        return sequence
    
    @staticmethod
    def golden_spiral(turns: float = 3, points_per_turn: int = 100) -> np.ndarray:
        """
        Generate points along a golden spiral (logarithmic spiral).
        
        Args:
            turns: Number of full rotations
            points_per_turn: Resolution of the spiral
            
        Returns:
            Array of (x, y) coordinates
        """
        theta = np.linspace(0, turns * 2 * math.pi, int(turns * points_per_turn))
        # Golden spiral growth rate
        b = math.log(SacredGeometry.PHI) / (math.pi / 2)
        r = np.exp(b * theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack([x, y])
    
    @staticmethod
    def fibonacci_spiral(max_size: int = 13) -> List[Tuple[float, float, float]]:
        """
        Generate Fibonacci spiral as sequence of quarter-circle arcs.
        
        Args:
            max_size: Maximum Fibonacci number to use
            
        Returns:
            List of (center_x, center_y, radius) for each arc
        """
        fib = SacredGeometry.fibonacci_sequence(max_size)
        arcs = []
        x, y = 0, 0
        
        # Direction: 0=right, 1=up, 2=left, 3=down
        direction = 0
        
        for i in range(2, len(fib)):
            radius = fib[i]
            
            # Determine arc center based on direction
            if direction == 0:  # Right
                cx, cy = x + fib[i-1], y
            elif direction == 1:  # Up
                cx, cy = x, y + fib[i-1]
            elif direction == 2:  # Left
                cx, cy = x - fib[i-1], y
            else:  # Down
                cx, cy = x, y - fib[i-1]
            
            arcs.append((cx, cy, radius))
            
            # Update position for next square
            if direction == 0:
                x += fib[i]
            elif direction == 1:
                y += fib[i]
            elif direction == 2:
                x -= fib[i]
            else:
                y -= fib[i]
            
            direction = (direction + 1) % 4
        
        return arcs
    
    @staticmethod
    def golden_rectangle_subdivisions(width: float, height: float, 
                                       iterations: int = 5) -> List[Tuple[float, float, float, float]]:
        """
        Subdivide a rectangle using golden ratio.
        
        Args:
            width: Initial width
            height: Initial height
            iterations: Number of subdivisions
            
        Returns:
            List of (x, y, w, h) rectangles
        """
        rectangles = [(0, 0, width, height)]
        
        for _ in range(iterations):
            x, y, w, h = rectangles[-1]
            if w > h:
                # Subdivide horizontally
                new_w = h * SacredGeometry.PHI
                if new_w <= w:
                    rectangles.append((x, y, new_w, h))
                else:
                    break
            else:
                # Subdivide vertically
                new_h = w * SacredGeometry.PHI
                if new_h <= h:
                    rectangles.append((x, y, w, new_h))
                else:
                    break
        
        return rectangles
    
    @staticmethod
    def platonic_solid_vertices(solid_type: str) -> np.ndarray:
        """
        Get vertices of Platonic solids.
        
        Args:
            solid_type: One of 'tetrahedron', 'cube', 'octahedron', 
                       'dodecahedron', 'icosahedron'
            
        Returns:
            Array of vertex coordinates
        """
        phi = SacredGeometry.PHI
        
        if solid_type == 'tetrahedron':
            return np.array([
                [1, 1, 1],
                [1, -1, -1],
                [-1, 1, -1],
                [-1, -1, 1]
            ]) / math.sqrt(3)
        
        elif solid_type == 'cube':
            return np.array([
                [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
                [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1]
            ]) / math.sqrt(3)
        
        elif solid_type == 'octahedron':
            return np.array([
                [1, 0, 0], [-1, 0, 0],
                [0, 1, 0], [0, -1, 0],
                [0, 0, 1], [0, 0, -1]
            ])
        
        elif solid_type == 'dodecahedron':
            vertices = []
            # Cube vertices
            for i in [-1, 1]:
                for j in [-1, 1]:
                    for k in [-1, 1]:
                        vertices.append([i, j, k])
            # Rectangle vertices
            for i in [-phi, phi]:
                for j in [-1/phi, 1/phi]:
                    vertices.append([0, i, j])
                    vertices.append([i, j, 0])
                    vertices.append([j, 0, i])
            return np.array(vertices) / math.sqrt(3)
        
        elif solid_type == 'icosahedron':
            vertices = []
            for i in [-1, 1]:
                for j in [-phi, phi]:
                    vertices.append([0, i, j])
                    vertices.append([i, j, 0])
                    vertices.append([j, 0, i])
            return np.array(vertices) / math.sqrt(1 + phi**2)
        
        else:
            raise ValueError(f"Unknown solid type: {solid_type}")
    
    @staticmethod
    def flower_of_life(radius: float = 1.0, generations: int = 3) -> List[Tuple[float, float, float]]:
        """
        Generate circles for Flower of Life pattern.
        
        Args:
            radius: Radius of each circle
            generations: Number of generations to generate
            
        Returns:
            List of (center_x, center_y, radius) for each circle
        """
        circles = [(0.0, 0.0, radius)]  # Central circle
        
        if generations < 1:
            return circles
        
        # First ring: 6 circles around center
        for i in range(6):
            angle = i * math.pi / 3
            x = radius * 2 * math.cos(angle)
            y = radius * 2 * math.sin(angle)
            circles.append((x, y, radius))
        
        if generations < 2:
            return circles
        
        # Subsequent rings
        for gen in range(2, generations + 1):
            new_circles = []
            for circle in circles[1:]:  # Skip central circle
                cx, cy, _ = circle
                # Add circles around each existing circle
                for i in range(6):
                    angle = i * math.pi / 3
                    x = cx + radius * 2 * math.cos(angle)
                    y = cy + radius * 2 * math.sin(angle)
                    # Check if circle already exists
                    is_new = True
                    for existing in circles + new_circles:
                        ex, ey, _ = existing
                        if abs(x - ex) < 0.1 and abs(y - ey) < 0.1:
                            is_new = False
                            break
                    if is_new:
                        new_circles.append((x, y, radius))
            circles.extend(new_circles)
        
        return circles
    
    @staticmethod
    def vesica_piscis(radius: float = 1.0, separation: Optional[float] = None) -> Tuple:
        """
        Generate two circles forming Vesica Piscis.
        
        Args:
            radius: Radius of each circle
            separation: Distance between centers (default: radius for traditional VP)
            
        Returns:
            Tuple of ((x1, y1, r1), (x2, y2, r2))
        """
        if separation is None:
            separation = radius
        
        return (
            (-separation/2, 0, radius),
            (separation/2, 0, radius)
        )
    
    @staticmethod
    def spiral_phyllotaxis(n: int = 500, scale: float = 1.0) -> np.ndarray:
        """
        Generate points using Vogel's method (sunflower seed pattern).
        
        Args:
            n: Number of points
            scale: Scaling factor
            
        Returns:
            Array of (x, y) coordinates
        """
        golden_angle_rad = SacredGeometry.GOLDEN_ANGLE * math.pi / 180
        
        points = []
        for i in range(n):
            theta = i * golden_angle_rad
            r = scale * math.sqrt(i)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.append([x, y])
        
        return np.array(points)


def main():
    """Demonstrate sacred geometry functions."""
    print("Mamba Architecture - Sacred Geometry Module")
    print("=" * 50)
    
    print(f"\nGolden Ratio (φ): {SacredGeometry.PHI}")
    print(f"Golden Angle: {SacredGeometry.GOLDEN_ANGLE}°")
    
    print("\nFibonacci Sequence (first 15 terms):")
    fib = SacredGeometry.fibonacci_sequence(15)
    print(fib)
    
    print("\nRatios approaching φ:")
    for i in range(2, min(len(fib), 12)):
        ratio = fib[i] / fib[i-1]
        print(f"F({i})/F({i-1}) = {fib[i]}/{fib[i-1]} = {ratio:.6f}")
    
    print("\nPlatonic Solids:")
    for solid in ['tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron']:
        vertices = SacredGeometry.platonic_solid_vertices(solid)
        print(f"{solid.capitalize()}: {len(vertices)} vertices")
    
    print("\n" + "=" * 50)
    print("Use this module to generate sacred geometry patterns")
    print("for architectural design in Mamba projects.")


if __name__ == "__main__":
    main()
