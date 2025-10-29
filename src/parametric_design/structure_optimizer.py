"""
Structure Optimizer - Optimize structures for efficiency and beauty.
"""

import numpy as np
from typing import List, Tuple, Dict
from scipy.optimize import minimize


class StructureOptimizer:
    """Optimize structural forms for various objectives."""
    
    @staticmethod
    def minimize_surface_area(volume: float, 
                             shape: str = 'sphere') -> Dict:
        """
        Find shape that minimizes surface area for given volume.
        
        Args:
            volume: Required volume
            shape: Type of shape to optimize
            
        Returns:
            Dictionary with optimal dimensions
        """
        if shape == 'sphere':
            # Sphere has minimum surface area for given volume
            radius = (3 * volume / (4 * np.pi)) ** (1/3)
            surface_area = 4 * np.pi * radius**2
            return {
                'shape': 'sphere',
                'radius': radius,
                'volume': volume,
                'surface_area': surface_area,
                'efficiency': volume / surface_area
            }
        
        elif shape == 'cube':
            side = volume ** (1/3)
            surface_area = 6 * side**2
            return {
                'shape': 'cube',
                'side': side,
                'volume': volume,
                'surface_area': surface_area,
                'efficiency': volume / surface_area
            }
    
    @staticmethod
    def optimize_column_spacing(span: float,
                               load: float,
                               max_columns: int = 10) -> List[float]:
        """
        Optimize column spacing for structural efficiency.
        
        Args:
            span: Total span length
            load: Total load to support
            max_columns: Maximum number of columns
            
        Returns:
            List of optimal column positions
        """
        def objective(positions):
            # Minimize maximum moment between columns
            positions = np.sort(positions)
            positions = np.concatenate([[0], positions, [span]])
            spans = np.diff(positions)
            moments = (load / len(spans)) * spans**2 / 8
            return np.max(moments)
        
        # Initial guess: evenly spaced
        n_cols = min(max_columns, int(span / 5) + 1)
        x0 = np.linspace(span/10, span*9/10, n_cols)
        
        # Bounds: columns must be within span
        bounds = [(0.1, span-0.1) for _ in range(n_cols)]
        
        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
        
        return sorted(result.x.tolist())
    
    @staticmethod
    def structural_topology_optimization(domain_size: Tuple[int, int],
                                        loads: List[Tuple[int, int, float]],
                                        supports: List[Tuple[int, int]],
                                        volume_fraction: float = 0.5,
                                        iterations: int = 50) -> np.ndarray:
        """
        Perform basic topology optimization (simplified SIMP method).
        
        Args:
            domain_size: Size of design domain (width, height)
            loads: List of (x, y, force) tuples
            supports: List of (x, y) support positions
            volume_fraction: Target material fraction
            iterations: Number of optimization iterations
            
        Returns:
            Density map (0=void, 1=solid)
        """
        width, height = domain_size
        
        # Initialize with uniform density
        density = np.ones((height, width)) * volume_fraction
        
        # Iterative optimization (simplified)
        for iteration in range(iterations):
            # Calculate compliance for each element
            compliance = np.zeros_like(density)
            
            for x, y, force in loads:
                # Simplified: higher density near loads and supports
                for sx, sy in supports:
                    dx = np.arange(width) - x
                    dy = np.arange(height)[:, np.newaxis] - y
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    sdx = np.arange(width) - sx
                    sdy = np.arange(height)[:, np.newaxis] - sy
                    support_dist = np.sqrt(sdx**2 + sdy**2)
                    
                    # Material should connect loads to supports
                    path_value = 1 / (distance + 1) + 1 / (support_dist + 1)
                    compliance += path_value * abs(force)
            
            # Normalize compliance
            compliance = compliance / np.max(compliance)
            
            # Update density based on compliance
            density = density + 0.1 * (compliance - volume_fraction)
            density = np.clip(density, 0.01, 1.0)
            
            # Volume constraint
            current_volume = np.mean(density)
            if current_volume > volume_fraction:
                density *= volume_fraction / current_volume
        
        # Threshold to binary
        threshold = np.percentile(density, (1 - volume_fraction) * 100)
        optimized = (density >= threshold).astype(float)
        
        return optimized
    
    @staticmethod
    def golden_ratio_proportions(base_dimension: float,
                                elements: int = 5) -> List[float]:
        """
        Generate dimensions following golden ratio for aesthetic optimization.
        
        Args:
            base_dimension: Starting dimension
            elements: Number of elements to generate
            
        Returns:
            List of dimensions in golden ratio proportion
        """
        phi = (1 + np.sqrt(5)) / 2
        dimensions = []
        
        current = base_dimension
        for _ in range(elements):
            dimensions.append(current)
            current = current / phi
        
        return dimensions
    
    @staticmethod
    def biomimetic_branching(trunk_radius: float,
                           branch_angle: float = 30.0,
                           levels: int = 4) -> Dict:
        """
        Optimize branching structure following natural patterns (Murray's Law).
        
        Args:
            trunk_radius: Main trunk radius
            branch_angle: Branching angle in degrees
            levels: Number of branching levels
            
        Returns:
            Dictionary with branch structure
        """
        # Murray's Law: r_parent^3 = r_child1^3 + r_child2^3
        branches = []
        
        def branch_recursive(radius, position, direction, level):
            if level >= levels:
                return
            
            # Calculate child branch radii using Murray's Law
            # For two equal branches: r_child = r_parent / (2^(1/3))
            child_radius = radius / (2 ** (1/3))
            
            # Branch left
            angle_rad = np.radians(branch_angle)
            left_dir = [
                direction[0] * np.cos(angle_rad) - direction[1] * np.sin(angle_rad),
                direction[0] * np.sin(angle_rad) + direction[1] * np.cos(angle_rad)
            ]
            left_pos = [position[0] + left_dir[0], position[1] + left_dir[1]]
            
            branches.append({
                'level': level,
                'position': left_pos,
                'radius': child_radius,
                'parent_position': position
            })
            
            branch_recursive(child_radius, left_pos, left_dir, level + 1)
            
            # Branch right
            right_dir = [
                direction[0] * np.cos(-angle_rad) - direction[1] * np.sin(-angle_rad),
                direction[0] * np.sin(-angle_rad) + direction[1] * np.cos(-angle_rad)
            ]
            right_pos = [position[0] + right_dir[0], position[1] + right_dir[1]]
            
            branches.append({
                'level': level,
                'position': right_pos,
                'radius': child_radius,
                'parent_position': position
            })
            
            branch_recursive(child_radius, right_pos, right_dir, level + 1)
        
        # Start branching
        branch_recursive(trunk_radius, [0, 0], [0, 1], 0)
        
        return {
            'trunk_radius': trunk_radius,
            'branches': branches,
            'branch_angle': branch_angle,
            'levels': levels
        }
