"""
Sacred Patterns - Geometric patterns found in nature and spiritual traditions.
Includes Flower of Life, Metatron's Cube, Seed of Life, etc.
"""

import numpy as np
from typing import List, Tuple


class SacredPatterns:
    """Generate sacred geometric patterns."""
    
    @staticmethod
    def seed_of_life(radius: float = 1.0) -> List[Tuple[float, float]]:
        """
        Generate Seed of Life pattern (7 circles).
        
        Args:
            radius: Radius of each circle
            
        Returns:
            List of (x, y) center coordinates
        """
        centers = [(0, 0)]  # Central circle
        
        # Six circles around center
        for i in range(6):
            angle = i * np.pi / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            centers.append((x, y))
        
        return centers
    
    @staticmethod
    def flower_of_life(radius: float = 1.0, rings: int = 3) -> List[Tuple[float, float]]:
        """
        Generate Flower of Life pattern (expanding circles).
        
        Args:
            radius: Radius of each circle
            rings: Number of rings to generate
            
        Returns:
            List of (x, y) center coordinates
        """
        centers = [(0, 0)]
        visited = {(0, 0)}
        
        for ring in range(rings):
            new_centers = []
            for cx, cy in centers:
                for i in range(6):
                    angle = i * np.pi / 3
                    x = cx + radius * np.cos(angle)
                    y = cy + radius * np.sin(angle)
                    
                    # Round to avoid floating point duplicates
                    pos = (round(x, 6), round(y, 6))
                    if pos not in visited:
                        visited.add(pos)
                        new_centers.append(pos)
            
            centers.extend(new_centers)
        
        return list(centers)
    
    @staticmethod
    def metatrons_cube(radius: float = 1.0) -> dict:
        """
        Generate Metatron's Cube from Fruit of Life.
        Contains all 5 Platonic solids within its structure.
        
        Args:
            radius: Radius scale
            
        Returns:
            Dictionary with vertices and connections
        """
        # 13 circles of Fruit of Life
        centers = [(0, 0)]  # Center
        
        # Inner ring (6 circles)
        for i in range(6):
            angle = i * np.pi / 3
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            centers.append((x, y))
        
        # Outer ring (6 circles)
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x = 2 * radius * np.cos(angle)
            y = 2 * radius * np.sin(angle)
            centers.append((x, y))
        
        # Connect all points to create Metatron's Cube
        connections = []
        n = len(centers)
        for i in range(n):
            for j in range(i + 1, n):
                connections.append((i, j))
        
        return {
            'vertices': centers,
            'connections': connections,
            'name': 'Metatrons Cube'
        }
    
    @staticmethod
    def vesica_piscis(radius: float = 1.0, separation: float = None) -> dict:
        """
        Generate Vesica Piscis (intersection of two circles).
        Symbol of creation and divine proportion.
        
        Args:
            radius: Radius of each circle
            separation: Distance between centers (default: radius for perfect vesica)
            
        Returns:
            Dictionary with circle centers and intersection points
        """
        if separation is None:
            separation = radius
        
        center1 = (-separation / 2, 0)
        center2 = (separation / 2, 0)
        
        # Calculate intersection points
        if separation < 2 * radius:
            # Circles intersect
            a = separation / 2
            h = np.sqrt(radius**2 - a**2)
            intersection1 = (0, h)
            intersection2 = (0, -h)
        else:
            intersection1 = None
            intersection2 = None
        
        return {
            'circle1_center': center1,
            'circle2_center': center2,
            'radius': radius,
            'intersection_top': intersection1,
            'intersection_bottom': intersection2,
            'name': 'Vesica Piscis'
        }
    
    @staticmethod
    def sri_yantra_triangles(scale: float = 1.0) -> List[np.ndarray]:
        """
        Generate simplified Sri Yantra pattern (9 interlocking triangles).
        Ancient sacred geometry representing the cosmos.
        
        Args:
            scale: Scale factor
            
        Returns:
            List of triangle vertex arrays
        """
        triangles = []
        
        # 5 downward pointing triangles (Shakti)
        for i in range(5):
            angle_offset = i * 2 * np.pi / 5
            size = scale * (1 - i * 0.15)
            triangle = np.array([
                [0, size],
                [-size * np.sin(np.pi/3), -size * np.cos(np.pi/3)],
                [size * np.sin(np.pi/3), -size * np.cos(np.pi/3)]
            ])
            # Rotate
            cos_a = np.cos(angle_offset)
            sin_a = np.sin(angle_offset)
            rotation = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            triangle = triangle @ rotation.T
            triangles.append(triangle)
        
        # 4 upward pointing triangles (Shiva)
        for i in range(4):
            angle_offset = i * 2 * np.pi / 4 + np.pi / 4
            size = scale * (0.8 - i * 0.15)
            triangle = np.array([
                [0, -size],
                [-size * np.sin(np.pi/3), size * np.cos(np.pi/3)],
                [size * np.sin(np.pi/3), size * np.cos(np.pi/3)]
            ])
            # Rotate
            cos_a = np.cos(angle_offset)
            sin_a = np.sin(angle_offset)
            rotation = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            triangle = triangle @ rotation.T
            triangles.append(triangle)
        
        return triangles
