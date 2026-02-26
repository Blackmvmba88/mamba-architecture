"""
Golden Ratio implementation for sacred geometry.
The golden ratio (φ) appears in nature and classical architecture.
"""

import numpy as np
from typing import Tuple, List


class GoldenRatio:
    """Calculate and apply golden ratio proportions."""
    
    PHI = (1 + np.sqrt(5)) / 2  # Golden ratio constant ≈ 1.618
    
    @classmethod
    def get_phi(cls) -> float:
        """Return the golden ratio constant."""
        return cls.PHI
    
    @classmethod
    def divide_segment(cls, length: float) -> Tuple[float, float]:
        """
        Divide a segment according to golden ratio.
        
        Args:
            length: Total length to divide
            
        Returns:
            Tuple of (longer_part, shorter_part)
        """
        longer = length / cls.PHI
        shorter = length - longer
        return (longer, shorter)
    
    @classmethod
    def golden_rectangle(cls, width: float) -> float:
        """
        Calculate height of golden rectangle from width.
        
        Args:
            width: Width of rectangle
            
        Returns:
            Height that creates golden ratio
        """
        return width / cls.PHI
    
    @classmethod
    def golden_spiral_points(cls, num_turns: int = 4, points_per_turn: int = 100) -> np.ndarray:
        """
        Generate points for a golden spiral.
        
        Args:
            num_turns: Number of spiral turns
            points_per_turn: Points per complete turn
            
        Returns:
            Array of (x, y) coordinates
        """
        theta = np.linspace(0, num_turns * 2 * np.pi, num_turns * points_per_turn)
        r = np.exp(theta / (2 * np.pi) * np.log(cls.PHI))
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return np.column_stack([x, y])
    
    @classmethod
    def golden_angle(cls) -> float:
        """
        Calculate golden angle in radians.
        Used in phyllotaxis (plant spiral patterns).
        
        Returns:
            Golden angle ≈ 2.399 radians (137.5°)
        """
        return 2 * np.pi * (1 - 1 / cls.PHI)
    
    @classmethod
    def phyllotaxis_pattern(cls, n_points: int = 500, scale: float = 1.0) -> np.ndarray:
        """
        Generate phyllotaxis pattern (sunflower seed arrangement).
        
        Args:
            n_points: Number of points to generate
            scale: Scaling factor
            
        Returns:
            Array of (x, y) coordinates
        """
        golden_angle = cls.golden_angle()
        points = []
        
        for i in range(n_points):
            theta = i * golden_angle
            r = scale * np.sqrt(i)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            points.append([x, y])
        
        return np.array(points)
