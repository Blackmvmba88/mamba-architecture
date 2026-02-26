"""
Surface Generator - Advanced parametric surface algorithms.
"""

import numpy as np
from typing import Tuple, Callable


class SurfaceGenerator:
    """Generate complex parametric surfaces."""
    
    @staticmethod
    def minimal_surface_schwarz(resolution: int = 50, scale: float = 1.0) -> np.ndarray:
        """
        Generate Schwarz P minimal surface (soap bubble geometry).
        
        Args:
            resolution: Number of points per dimension
            scale: Scaling factor
            
        Returns:
            Array of vertices
        """
        u = np.linspace(-np.pi, np.pi, resolution)
        v = np.linspace(-np.pi, np.pi, resolution)
        u, v = np.meshgrid(u, v)
        
        x = scale * np.cos(u)
        y = scale * np.cos(v)
        z = scale * (np.cos(u) + np.cos(v))
        
        vertices = np.stack([x, y, z], axis=-1)
        return vertices
    
    @staticmethod
    def gyroid_surface(resolution: int = 50, scale: float = 1.0) -> np.ndarray:
        """
        Generate gyroid minimal surface (found in butterfly wings and sea creatures).
        
        Args:
            resolution: Number of points per dimension
            scale: Scaling factor
            
        Returns:
            Array of vertices
        """
        x = np.linspace(-np.pi, np.pi, resolution)
        y = np.linspace(-np.pi, np.pi, resolution)
        z = np.linspace(-np.pi, np.pi, resolution)
        
        X, Y, Z = np.meshgrid(x, y, z)
        
        # Gyroid equation: sin(X)cos(Y) + sin(Y)cos(Z) + sin(Z)cos(X) = 0
        gyroid = (np.sin(X) * np.cos(Y) + 
                 np.sin(Y) * np.cos(Z) + 
                 np.sin(Z) * np.cos(X))
        
        # Extract isosurface at level 0
        vertices = []
        threshold = 0.1
        for i in range(resolution):
            for j in range(resolution):
                for k in range(resolution):
                    if abs(gyroid[i, j, k]) < threshold:
                        vertices.append([X[i, j, k] * scale, 
                                       Y[i, j, k] * scale, 
                                       Z[i, j, k] * scale])
        
        return np.array(vertices) if vertices else np.array([])
    
    @staticmethod
    def hyperboloid(height: float = 2.0, 
                   radius: float = 1.0,
                   waist: float = 0.5,
                   resolution: int = 50) -> np.ndarray:
        """
        Generate hyperboloid of revolution (cooling tower shape).
        
        Args:
            height: Total height
            radius: Base/top radius
            waist: Minimum radius at middle
            resolution: Number of points
            
        Returns:
            Array of vertices
        """
        u = np.linspace(0, 2*np.pi, resolution)
        v = np.linspace(-height/2, height/2, resolution)
        u, v = np.meshgrid(u, v)
        
        r = waist * np.sqrt(1 + (v / (height/4))**2)
        
        x = r * np.cos(u)
        y = r * np.sin(u)
        z = v
        
        vertices = np.stack([x, y, z], axis=-1)
        return vertices
    
    @staticmethod
    def catenary_arch(span: float = 10.0,
                     height: float = 5.0,
                     resolution: int = 100) -> np.ndarray:
        """
        Generate catenary curve (natural hanging chain shape).
        Used in optimal arch design.
        
        Args:
            span: Width of arch
            height: Height of arch
            resolution: Number of points
            
        Returns:
            Array of 2D points (x, y)
        """
        x = np.linspace(-span/2, span/2, resolution)
        
        # Catenary: y = a * cosh(x/a) - a
        a = span / (2 * np.arccosh(1 + height / (span/4)))
        y = a * np.cosh(x / a) - a
        
        # Flip to make arch
        y = np.max(y) - y
        
        return np.column_stack([x, y])
    
    @staticmethod
    def tensile_surface(anchor_points: np.ndarray,
                       resolution: int = 50) -> np.ndarray:
        """
        Generate minimal surface between anchor points (tent/sail shape).
        
        Args:
            anchor_points: Array of anchor point coordinates
            resolution: Grid resolution
            
        Returns:
            Array of surface vertices
        """
        # Simple approximation using harmonic interpolation
        bounds = np.array([
            [anchor_points[:, 0].min(), anchor_points[:, 0].max()],
            [anchor_points[:, 1].min(), anchor_points[:, 1].max()]
        ])
        
        x = np.linspace(bounds[0, 0], bounds[0, 1], resolution)
        y = np.linspace(bounds[1, 0], bounds[1, 1], resolution)
        X, Y = np.meshgrid(x, y)
        
        # Initialize Z with interpolation from anchor points
        Z = np.zeros_like(X)
        
        for ax, ay, az in anchor_points:
            distance = np.sqrt((X - ax)**2 + (Y - ay)**2)
            weight = 1 / (distance + 0.1)
            Z += weight * az
        
        # Normalize
        weight_sum = np.zeros_like(X)
        for ax, ay, az in anchor_points:
            distance = np.sqrt((X - ax)**2 + (Y - ay)**2)
            weight_sum += 1 / (distance + 0.1)
        
        Z = Z / weight_sum
        
        vertices = np.stack([X, Y, Z], axis=-1)
        return vertices
