"""
Fractal Generation Module for Mamba Architecture

This module implements various fractal patterns inspired by natural biological structures.
"""

import math
import numpy as np
from typing import List, Tuple, Callable, Dict
import random


class FractalGenerator:
    """Generate various fractal patterns found in nature."""
    
    @staticmethod
    def koch_curve(order: int = 4, length: float = 1.0) -> np.ndarray:
        """
        Generate Koch curve (snowflake boundary).
        
        Args:
            order: Recursion depth
            length: Initial segment length
            
        Returns:
            Array of (x, y) coordinates
        """
        def koch_segment(p1, p2, depth):
            if depth == 0:
                return [p1, p2]
            
            # Divide line into three parts
            dx, dy = (p2[0] - p1[0]) / 3, (p2[1] - p1[1]) / 3
            
            p1_new = p1
            p2_new = (p1[0] + dx, p1[1] + dy)
            p4_new = (p1[0] + 2*dx, p1[1] + 2*dy)
            p5_new = p2
            
            # Create peak point
            angle = math.pi / 3  # 60 degrees
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            p3_new = (
                p2_new[0] + dx * cos_a - dy * sin_a,
                p2_new[1] + dx * sin_a + dy * cos_a
            )
            
            # Recursively process each segment
            result = []
            result.extend(koch_segment(p1_new, p2_new, depth - 1)[:-1])
            result.extend(koch_segment(p2_new, p3_new, depth - 1)[:-1])
            result.extend(koch_segment(p3_new, p4_new, depth - 1)[:-1])
            result.extend(koch_segment(p4_new, p5_new, depth - 1))
            
            return result
        
        # Create three sides of snowflake
        points = []
        vertices = [
            (0, 0),
            (length, 0),
            (length/2, length * math.sqrt(3)/2),
            (0, 0)
        ]
        
        for i in range(len(vertices) - 1):
            segment = koch_segment(vertices[i], vertices[i+1], order)
            points.extend(segment[:-1])
        
        return np.array(points)
    
    @staticmethod
    def sierpinski_triangle(order: int = 5, size: float = 1.0) -> List[np.ndarray]:
        """
        Generate Sierpinski triangle.
        
        Args:
            order: Recursion depth
            size: Size of base triangle
            
        Returns:
            List of triangle vertices
        """
        def subdivide(vertices, depth):
            if depth == 0:
                return [vertices]
            
            # Calculate midpoints
            mid1 = [(vertices[0][i] + vertices[1][i]) / 2 for i in range(2)]
            mid2 = [(vertices[1][i] + vertices[2][i]) / 2 for i in range(2)]
            mid3 = [(vertices[2][i] + vertices[0][i]) / 2 for i in range(2)]
            
            # Recursively subdivide three corner triangles
            triangles = []
            triangles.extend(subdivide([vertices[0], mid1, mid3], depth - 1))
            triangles.extend(subdivide([mid1, vertices[1], mid2], depth - 1))
            triangles.extend(subdivide([mid3, mid2, vertices[2]], depth - 1))
            
            return triangles
        
        # Initial equilateral triangle
        height = size * math.sqrt(3) / 2
        initial = [
            (0, 0),
            (size, 0),
            (size/2, height)
        ]
        
        triangles = subdivide(initial, order)
        return [np.array(t) for t in triangles]
    
    @staticmethod
    def l_system(axiom: str, rules: Dict[str, str], iterations: int) -> str:
        """
        Generate L-system string.
        
        Args:
            axiom: Starting string
            rules: Production rules dictionary
            iterations: Number of iterations
            
        Returns:
            Generated string
        """
        current = axiom
        for _ in range(iterations):
            next_gen = ""
            for char in current:
                next_gen += rules.get(char, char)
            current = next_gen
        return current
    
    @staticmethod
    def l_system_to_turtle(l_string: str, angle: float = 25, step: float = 1.0,
                           start_pos: Tuple[float, float] = (0, 0),
                           start_angle: float = 90) -> List[Tuple[List[float], List[float]]]:
        """
        Convert L-system string to turtle graphics paths.
        
        Args:
            l_string: L-system string
            angle: Turn angle in degrees
            step: Step length
            start_pos: Starting position
            start_angle: Starting angle in degrees
            
        Returns:
            List of line segments [(x1, y1), (x2, y2)]
        """
        x, y = start_pos
        theta = start_angle
        stack = []
        lines = []
        
        for command in l_string:
            if command == 'F' or command == 'G':
                # Move forward and draw
                new_x = x + step * math.cos(math.radians(theta))
                new_y = y + step * math.sin(math.radians(theta))
                lines.append(([x, y], [new_x, new_y]))
                x, y = new_x, new_y
            elif command == 'f':
                # Move forward without drawing
                x += step * math.cos(math.radians(theta))
                y += step * math.sin(math.radians(theta))
            elif command == '+':
                theta += angle
            elif command == '-':
                theta -= angle
            elif command == '[':
                stack.append((x, y, theta))
            elif command == ']':
                x, y, theta = stack.pop()
        
        return lines
    
    @staticmethod
    def fractal_tree(iterations: int = 8, angle: float = 30, 
                     length_ratio: float = 0.7) -> List[Tuple[List[float], List[float]]]:
        """
        Generate fractal tree using L-system.
        
        Args:
            iterations: Number of iterations
            angle: Branching angle
            length_ratio: Length reduction ratio
            
        Returns:
            List of line segments
        """
        # Tree L-system
        axiom = "F"
        rules = {
            "F": "FF+[+F-F-F]-[-F+F+F]"
        }
        
        l_string = FractalGenerator.l_system(axiom, rules, iterations)
        return FractalGenerator.l_system_to_turtle(l_string, angle=angle, step=1.0)
    
    @staticmethod
    def plant_growth(iterations: int = 5, angle: float = 25) -> List[Tuple[List[float], List[float]]]:
        """
        Generate plant-like structure using L-system.
        
        Args:
            iterations: Growth stages
            angle: Branching angle
            
        Returns:
            List of line segments
        """
        # Plant L-system (Algae-like)
        axiom = "F"
        rules = {
            "F": "F[+F]F[-F]F"
        }
        
        l_string = FractalGenerator.l_system(axiom, rules, iterations)
        return FractalGenerator.l_system_to_turtle(l_string, angle=angle, step=2.0)
    
    @staticmethod
    def dragon_curve(order: int = 10) -> np.ndarray:
        """
        Generate dragon curve fractal.
        
        Args:
            order: Recursion depth
            
        Returns:
            Array of (x, y) coordinates
        """
        # Dragon curve L-system
        axiom = "FX"
        rules = {
            "X": "X+YF+",
            "Y": "-FX-Y"
        }
        
        l_string = FractalGenerator.l_system(axiom, rules, order)
        lines = FractalGenerator.l_system_to_turtle(l_string, angle=90, step=1.0, start_angle=0)
        
        # Extract points
        points = []
        if lines:
            points.append(lines[0][0])
            for line in lines:
                points.append(line[1])
        
        return np.array(points)
    
    @staticmethod
    def diffusion_limited_aggregation(n_particles: int = 1000, 
                                       grid_size: int = 200,
                                       stickiness: float = 1.0) -> List[Tuple[int, int]]:
        """
        Generate DLA (Diffusion Limited Aggregation) pattern.
        
        Args:
            n_particles: Number of particles to add
            grid_size: Size of simulation grid
            stickiness: Probability of sticking (0-1)
            
        Returns:
            List of particle positions
        """
        center = grid_size // 2
        cluster = {(center, center)}
        
        for _ in range(n_particles):
            # Start particle at random position on circle
            angle = random.uniform(0, 2 * math.pi)
            radius = grid_size // 4
            x = int(center + radius * math.cos(angle))
            y = int(center + radius * math.sin(angle))
            
            # Random walk until it sticks
            while True:
                # Check if adjacent to cluster
                neighbors = [
                    (x+1, y), (x-1, y), (x, y+1), (x, y-1),
                    (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
                ]
                
                if any(n in cluster for n in neighbors):
                    if random.random() < stickiness:
                        cluster.add((x, y))
                        break
                
                # Random walk
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                x, y = x + dx, y + dy
                
                # Boundary check - respawn if too far
                dist = math.sqrt((x - center)**2 + (y - center)**2)
                if dist > grid_size // 2:
                    angle = random.uniform(0, 2 * math.pi)
                    radius = grid_size // 4
                    x = int(center + radius * math.cos(angle))
                    y = int(center + radius * math.sin(angle))
        
        return list(cluster)
    
    @staticmethod
    def mandelbrot_set(width: int = 800, height: int = 600, 
                       max_iter: int = 100,
                       x_range: Tuple[float, float] = (-2.5, 1.0),
                       y_range: Tuple[float, float] = (-1.0, 1.0)) -> np.ndarray:
        """
        Generate Mandelbrot set.
        
        Args:
            width: Image width
            height: Image height
            max_iter: Maximum iterations
            x_range: Range of real axis
            y_range: Range of imaginary axis
            
        Returns:
            2D array of iteration counts
        """
        x_min, x_max = x_range
        y_min, y_max = y_range
        
        result = np.zeros((height, width))
        
        for py in range(height):
            for px in range(width):
                # Map pixel to complex plane
                x0 = x_min + (x_max - x_min) * px / width
                y0 = y_min + (y_max - y_min) * py / height
                
                x, y = 0, 0
                iteration = 0
                
                while x*x + y*y <= 4 and iteration < max_iter:
                    x_temp = x*x - y*y + x0
                    y = 2*x*y + y0
                    x = x_temp
                    iteration += 1
                
                result[py, px] = iteration
        
        return result
    
    @staticmethod
    def barnsley_fern(n_points: int = 10000) -> np.ndarray:
        """
        Generate Barnsley fern using IFS (Iterated Function System).
        
        Args:
            n_points: Number of points to generate
            
        Returns:
            Array of (x, y) coordinates
        """
        points = []
        x, y = 0, 0
        
        for _ in range(n_points):
            r = random.random()
            
            if r < 0.01:
                # Stem
                x_new = 0
                y_new = 0.16 * y
            elif r < 0.86:
                # Smaller leaflets
                x_new = 0.85 * x + 0.04 * y
                y_new = -0.04 * x + 0.85 * y + 1.6
            elif r < 0.93:
                # Largest left leaflet
                x_new = 0.20 * x - 0.26 * y
                y_new = 0.23 * x + 0.22 * y + 1.6
            else:
                # Largest right leaflet
                x_new = -0.15 * x + 0.28 * y
                y_new = 0.26 * x + 0.24 * y + 0.44
            
            x, y = x_new, y_new
            points.append([x, y])
        
        return np.array(points)


def main():
    """Demonstrate fractal generation."""
    print("Mamba Architecture - Fractal Generator Module")
    print("=" * 50)
    
    print("\n1. Koch Snowflake")
    koch = FractalGenerator.koch_curve(order=3)
    print(f"   Generated {len(koch)} points")
    
    print("\n2. Sierpinski Triangle")
    sierpinski = FractalGenerator.sierpinski_triangle(order=4)
    print(f"   Generated {len(sierpinski)} triangles")
    
    print("\n3. L-System Fractal Tree")
    tree = FractalGenerator.fractal_tree(iterations=4)
    print(f"   Generated {len(tree)} branches")
    
    print("\n4. Plant Growth Pattern")
    plant = FractalGenerator.plant_growth(iterations=4)
    print(f"   Generated {len(plant)} segments")
    
    print("\n5. Dragon Curve")
    dragon = FractalGenerator.dragon_curve(order=8)
    print(f"   Generated {len(dragon)} points")
    
    print("\n6. Barnsley Fern")
    fern = FractalGenerator.barnsley_fern(n_points=5000)
    print(f"   Generated {len(fern)} points")
    
    print("\n7. Diffusion Limited Aggregation")
    dla = FractalGenerator.diffusion_limited_aggregation(n_particles=100)
    print(f"   Generated cluster with {len(dla)} particles")
    
    print("\n" + "=" * 50)
    print("Use these fractals as inspiration for architectural patterns:")
    print("- Koch curve for facade edges and decorative elements")
    print("- Sierpinski for structural lattices")
    print("- L-systems for branching support structures")
    print("- DLA for organic growth patterns")
    print("- Barnsley fern for natural ornamentation")


if __name__ == "__main__":
    main()
