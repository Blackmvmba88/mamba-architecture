"""
Noise Generator - Perlin noise and procedural textures.
"""

import numpy as np
from typing import Tuple


class NoiseGenerator:
    """Generate various types of procedural noise."""
    
    @staticmethod
    def perlin_noise_2d(shape: Tuple[int, int],
                       scale: float = 10.0,
                       octaves: int = 6,
                       persistence: float = 0.5,
                       lacunarity: float = 2.0) -> np.ndarray:
        """
        Generate 2D Perlin-like noise using numpy.
        Simplified version using random interpolation.
        
        Args:
            shape: Output shape (height, width)
            scale: Scale of the noise
            octaves: Number of octaves
            persistence: Amplitude decay per octave
            lacunarity: Frequency increase per octave
            
        Returns:
            2D noise array
        """
        height, width = shape
        noise = np.zeros((height, width))
        
        for octave in range(octaves):
            freq = lacunarity ** octave
            amp = persistence ** octave
            
            # Generate random grid
            grid_size = (int(height / scale * freq) + 2, int(width / scale * freq) + 2)
            grid = np.random.rand(*grid_size)
            
            # Interpolate
            y = np.linspace(0, grid_size[0] - 1, height)
            x = np.linspace(0, grid_size[1] - 1, width)
            
            from scipy.interpolate import RectBivariateSpline
            interpolator = RectBivariateSpline(
                np.arange(grid_size[0]),
                np.arange(grid_size[1]),
                grid,
                kx=1, ky=1
            )
            
            octave_noise = interpolator(y, x)
            noise += octave_noise * amp
        
        # Normalize to [0, 1]
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-10)
        
        return noise
    
    @staticmethod
    def simplex_noise_3d(shape: Tuple[int, int, int],
                        scale: float = 10.0) -> np.ndarray:
        """
        Generate simplified 3D noise.
        
        Args:
            shape: Output shape (depth, height, width)
            scale: Scale of the noise
            
        Returns:
            3D noise array
        """
        depth, height, width = shape
        
        # Create coordinate grids
        z = np.linspace(0, scale, depth)
        y = np.linspace(0, scale, height)
        x = np.linspace(0, scale, width)
        
        Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
        
        # Combine sine waves for pseudo-noise
        noise = (np.sin(X * 0.5) * np.cos(Y * 0.3) * np.sin(Z * 0.7) +
                np.sin(X * 1.1) * np.sin(Y * 0.8) +
                np.cos(Z * 1.3) * np.sin(X * 0.6 + Y * 0.4))
        
        # Normalize
        noise = (noise - noise.min()) / (noise.max() - noise.min() + 1e-10)
        
        return noise
    
    @staticmethod
    def worley_noise_2d(shape: Tuple[int, int],
                       n_points: int = 20,
                       distance_type: str = 'euclidean') -> np.ndarray:
        """
        Generate 2D Worley (cellular) noise.
        
        Args:
            shape: Output shape (height, width)
            n_points: Number of seed points
            distance_type: 'euclidean', 'manhattan', or 'chebyshev'
            
        Returns:
            2D noise array
        """
        height, width = shape
        
        # Generate random points
        points = np.random.rand(n_points, 2)
        points[:, 0] *= width
        points[:, 1] *= height
        
        # Create coordinate grid
        y, x = np.mgrid[0:height, 0:width]
        
        # Calculate distances to nearest point
        distances = np.full((height, width), float('inf'))
        
        for point in points:
            if distance_type == 'euclidean':
                dist = np.sqrt((x - point[0])**2 + (y - point[1])**2)
            elif distance_type == 'manhattan':
                dist = abs(x - point[0]) + abs(y - point[1])
            elif distance_type == 'chebyshev':
                dist = np.maximum(abs(x - point[0]), abs(y - point[1]))
            else:
                dist = np.sqrt((x - point[0])**2 + (y - point[1])**2)
            
            distances = np.minimum(distances, dist)
        
        # Normalize
        distances = (distances - distances.min()) / (distances.max() - distances.min() + 1e-10)
        
        return distances
    
    @staticmethod
    def fractal_brownian_motion(shape: Tuple[int, int],
                                octaves: int = 6,
                                persistence: float = 0.5) -> np.ndarray:
        """
        Generate Fractal Brownian Motion (fBm).
        
        Args:
            shape: Output shape (height, width)
            octaves: Number of octaves
            persistence: Amplitude decay
            
        Returns:
            2D fBm array
        """
        return NoiseGenerator.perlin_noise_2d(
            shape,
            scale=10.0,
            octaves=octaves,
            persistence=persistence
        )
    
    @staticmethod
    def turbulence(shape: Tuple[int, int],
                  octaves: int = 6,
                  persistence: float = 0.5) -> np.ndarray:
        """
        Generate turbulence pattern (absolute value of fBm).
        
        Args:
            shape: Output shape (height, width)
            octaves: Number of octaves
            persistence: Amplitude decay
            
        Returns:
            2D turbulence array
        """
        noise = NoiseGenerator.perlin_noise_2d(shape, octaves=octaves, persistence=persistence)
        # Apply turbulence transformation
        return np.abs(noise - 0.5) * 2
    
    @staticmethod
    def ridged_multifractal(shape: Tuple[int, int],
                           octaves: int = 6,
                           persistence: float = 0.5) -> np.ndarray:
        """
        Generate ridged multifractal noise (for mountains/terrain).
        
        Args:
            shape: Output shape (height, width)
            octaves: Number of octaves
            persistence: Amplitude decay
            
        Returns:
            2D ridged noise array
        """
        noise = NoiseGenerator.perlin_noise_2d(shape, octaves=octaves, persistence=persistence)
        # Ridged transformation
        return 1 - np.abs(noise - 0.5) * 2
