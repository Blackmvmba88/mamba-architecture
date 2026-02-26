"""
Form Generator - Parametric form generation algorithms.
Creates 3D forms based on mathematical parameters.
"""

import numpy as np
from typing import Tuple, Dict, List, Callable


class FormGenerator:
    """Generate parametric 3D forms."""
    
    @staticmethod
    def parametric_surface(u_range: Tuple[float, float],
                          v_range: Tuple[float, float],
                          func: Callable,
                          resolution: int = 50) -> np.ndarray:
        """
        Generate parametric surface from function.
        
        Args:
            u_range: Range for u parameter (start, end)
            v_range: Range for v parameter (start, end)
            func: Function that takes (u, v) and returns (x, y, z)
            resolution: Number of points per dimension
            
        Returns:
            Array of vertices (resolution x resolution x 3)
        """
        u = np.linspace(u_range[0], u_range[1], resolution)
        v = np.linspace(v_range[0], v_range[1], resolution)
        
        vertices = np.zeros((resolution, resolution, 3))
        
        for i, u_val in enumerate(u):
            for j, v_val in enumerate(v):
                vertices[i, j] = func(u_val, v_val)
        
        return vertices
    
    @staticmethod
    def torus(major_radius: float = 2.0,
              minor_radius: float = 0.5,
              resolution: int = 50) -> np.ndarray:
        """
        Generate torus (donut shape).
        
        Args:
            major_radius: Distance from center to tube center
            minor_radius: Radius of tube
            resolution: Number of points
            
        Returns:
            Array of vertices
        """
        def torus_func(u, v):
            x = (major_radius + minor_radius * np.cos(v)) * np.cos(u)
            y = (major_radius + minor_radius * np.cos(v)) * np.sin(u)
            z = minor_radius * np.sin(v)
            return np.array([x, y, z])
        
        return FormGenerator.parametric_surface(
            (0, 2*np.pi), (0, 2*np.pi),
            torus_func, resolution
        )
    
    @staticmethod
    def mobius_strip(width: float = 1.0,
                     resolution: int = 50) -> np.ndarray:
        """
        Generate Möbius strip (single-sided surface).
        
        Args:
            width: Width of the strip
            resolution: Number of points
            
        Returns:
            Array of vertices
        """
        def mobius_func(u, v):
            x = (1 + v/2 * np.cos(u/2)) * np.cos(u)
            y = (1 + v/2 * np.cos(u/2)) * np.sin(u)
            z = v/2 * np.sin(u/2)
            return np.array([x * width, y * width, z * width])
        
        return FormGenerator.parametric_surface(
            (0, 2*np.pi), (-1, 1),
            mobius_func, resolution
        )
    
    @staticmethod
    def klein_bottle(scale: float = 1.0,
                     resolution: int = 50) -> np.ndarray:
        """
        Generate Klein bottle (4D object projected to 3D).
        
        Args:
            scale: Scaling factor
            resolution: Number of points
            
        Returns:
            Array of vertices
        """
        def klein_func(u, v):
            r = 4 * (1 - np.cos(u) / 2)
            if u < np.pi:
                x = 6 * np.cos(u) * (1 + np.sin(u)) + r * np.cos(u) * np.cos(v)
                y = 16 * np.sin(u) + r * np.sin(u) * np.cos(v)
            else:
                x = 6 * np.cos(u) * (1 + np.sin(u)) + r * np.cos(v + np.pi)
                y = 16 * np.sin(u)
            z = r * np.sin(v)
            return np.array([x * scale, y * scale, z * scale])
        
        return FormGenerator.parametric_surface(
            (0, 2*np.pi), (0, 2*np.pi),
            klein_func, resolution
        )
    
    @staticmethod
    def shell_spiral(a: float = 0.2,
                    b: float = 0.5,
                    turns: int = 3,
                    resolution: int = 100) -> np.ndarray:
        """
        Generate logarithmic spiral shell (like nautilus).
        
        Args:
            a: Spiral growth rate
            b: Vertical growth rate
            turns: Number of spiral turns
            resolution: Number of points
            
        Returns:
            Array of vertices
        """
        theta = np.linspace(0, turns * 2 * np.pi, resolution)
        r = a * np.exp(b * theta)
        
        vertices = []
        for t, radius in zip(theta, r):
            x = radius * np.cos(t)
            y = radius * np.sin(t)
            z = b * t
            vertices.append([x, y, z])
        
        return np.array(vertices)
    
    @staticmethod
    def voronoi_structure_3d(points: np.ndarray,
                            bounds: Tuple[Tuple[float, float], ...],
                            scale: float = 1.0) -> Dict:
        """
        Generate 3D Voronoi structure (organic cellular pattern).
        
        Args:
            points: Seed points for Voronoi cells
            bounds: Bounding box ((xmin, xmax), (ymin, ymax), (zmin, zmax))
            scale: Scaling factor
            
        Returns:
            Dictionary with cell information
        """
        from scipy.spatial import Voronoi
        
        # Create Voronoi diagram
        vor = Voronoi(points)
        
        cells = []
        for region_idx, region in enumerate(vor.regions):
            if len(region) > 0 and -1 not in region:
                cell_vertices = vor.vertices[region] * scale
                cells.append({
                    'vertices': cell_vertices,
                    'region_idx': region_idx
                })
        
        return {
            'cells': cells,
            'points': points * scale,
            'vertices': vor.vertices * scale
        }
    
    @staticmethod
    def l_system_3d(axiom: str,
                   rules: Dict[str, str],
                   iterations: int,
                   angle: float = 25.0,
                   step_size: float = 1.0) -> np.ndarray:
        """
        Generate 3D L-System (Lindenmayer system) for organic growth patterns.
        
        Args:
            axiom: Starting string
            rules: Production rules
            iterations: Number of iterations
            angle: Rotation angle in degrees
            step_size: Step size for forward movement
            
        Returns:
            Array of line segments
        """
        # Generate L-System string
        current = axiom
        for _ in range(iterations):
            next_gen = ""
            for char in current:
                next_gen += rules.get(char, char)
            current = next_gen
        
        # Interpret string as 3D turtle graphics
        position = np.array([0.0, 0.0, 0.0])
        direction = np.array([0.0, 1.0, 0.0])  # Up
        angle_rad = np.radians(angle)
        
        stack = []
        segments = []
        
        for char in current:
            if char == 'F':  # Forward
                new_position = position + direction * step_size
                segments.append([position.copy(), new_position.copy()])
                position = new_position
            elif char == '+':  # Rotate right
                cos_a = np.cos(angle_rad)
                sin_a = np.sin(angle_rad)
                rotation = np.array([
                    [cos_a, 0, sin_a],
                    [0, 1, 0],
                    [-sin_a, 0, cos_a]
                ])
                direction = rotation @ direction
            elif char == '-':  # Rotate left
                cos_a = np.cos(-angle_rad)
                sin_a = np.sin(-angle_rad)
                rotation = np.array([
                    [cos_a, 0, sin_a],
                    [0, 1, 0],
                    [-sin_a, 0, cos_a]
                ])
                direction = rotation @ direction
            elif char == '[':  # Push state
                stack.append((position.copy(), direction.copy()))
            elif char == ']':  # Pop state
                if stack:
                    position, direction = stack.pop()
        
        return np.array(segments) if segments else np.array([])
