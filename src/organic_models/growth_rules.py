"""
Growth Rules - Biological growth patterns for architecture.
"""

import numpy as np
from typing import Dict, List, Tuple, Callable


class GrowthRules:
    """Implement natural growth rules for organic structures."""
    
    @staticmethod
    def phototropism(current_direction: np.ndarray,
                    light_direction: np.ndarray,
                    strength: float = 0.3) -> np.ndarray:
        """
        Simulate phototropism (growth toward light).
        
        Args:
            current_direction: Current growth direction vector
            light_direction: Direction of light source
            strength: Response strength (0-1)
            
        Returns:
            New growth direction
        """
        # Normalize vectors
        current = current_direction / np.linalg.norm(current_direction)
        light = light_direction / np.linalg.norm(light_direction)
        
        # Blend current direction with light direction
        new_direction = (1 - strength) * current + strength * light
        new_direction = new_direction / np.linalg.norm(new_direction)
        
        return new_direction
    
    @staticmethod
    def gravitropism(current_direction: np.ndarray,
                    strength: float = 0.2,
                    positive: bool = False) -> np.ndarray:
        """
        Simulate gravitropism (response to gravity).
        
        Args:
            current_direction: Current growth direction vector
            strength: Response strength (0-1)
            positive: True for upward growth, False for downward
            
        Returns:
            New growth direction
        """
        gravity = np.array([0, 0, 1 if positive else -1])
        
        current = current_direction / np.linalg.norm(current_direction)
        new_direction = (1 - strength) * current + strength * gravity
        new_direction = new_direction / np.linalg.norm(new_direction)
        
        return new_direction
    
    @staticmethod
    def branching_condition(age: int,
                           energy: float,
                           branch_age_threshold: int = 5,
                           branch_energy_threshold: float = 0.7) -> bool:
        """
        Determine if branching should occur.
        
        Args:
            age: Age of segment
            energy: Available energy (0-1)
            branch_age_threshold: Minimum age for branching
            branch_energy_threshold: Minimum energy for branching
            
        Returns:
            True if branching should occur
        """
        return age >= branch_age_threshold and energy >= branch_energy_threshold
    
    @staticmethod
    def resource_distribution(parent_resource: float,
                            num_children: int,
                            distribution: str = 'equal') -> List[float]:
        """
        Distribute resources among branches.
        
        Args:
            parent_resource: Total available resource
            num_children: Number of child branches
            distribution: 'equal', 'dominant', or 'fibonacci'
            
        Returns:
            List of resource allocations
        """
        if distribution == 'equal':
            # Equal distribution
            child_resource = parent_resource / num_children
            return [child_resource] * num_children
        
        elif distribution == 'dominant':
            # One dominant branch
            resources = [parent_resource * 0.6]  # Dominant
            remaining = parent_resource * 0.4
            for _ in range(num_children - 1):
                resources.append(remaining / (num_children - 1))
            return resources
        
        elif distribution == 'fibonacci':
            # Fibonacci-based distribution
            from ..sacred_geometry import FibonacciSequence
            fib = FibonacciSequence.generate(num_children + 2)[2:]
            total = sum(fib)
            return [(f / total) * parent_resource for f in fib]
        
        return [parent_resource / num_children] * num_children
    
    @staticmethod
    def apical_dominance(branches: List[Dict],
                        main_branch_idx: int = 0,
                        suppression_factor: float = 0.5) -> List[Dict]:
        """
        Apply apical dominance (main branch suppresses side branches).
        
        Args:
            branches: List of branch dictionaries
            main_branch_idx: Index of main (apical) branch
            suppression_factor: How much to suppress other branches (0-1)
            
        Returns:
            Modified list of branches
        """
        modified_branches = []
        
        for i, branch in enumerate(branches):
            if i == main_branch_idx:
                # Main branch grows normally
                modified_branches.append(branch.copy())
            else:
                # Side branches are suppressed
                suppressed_branch = branch.copy()
                suppressed_branch['growth_rate'] = branch.get('growth_rate', 1.0) * (1 - suppression_factor)
                suppressed_branch['energy'] = branch.get('energy', 1.0) * (1 - suppression_factor)
                modified_branches.append(suppressed_branch)
        
        return modified_branches
    
    @staticmethod
    def thigmotropism(current_direction: np.ndarray,
                     obstacle_position: np.ndarray,
                     current_position: np.ndarray,
                     avoidance_distance: float = 2.0) -> np.ndarray:
        """
        Simulate thigmotropism (response to touch/obstacles).
        
        Args:
            current_direction: Current growth direction
            obstacle_position: Position of obstacle
            current_position: Current position
            avoidance_distance: Distance at which to start avoiding
            
        Returns:
            Modified growth direction
        """
        # Vector to obstacle
        to_obstacle = obstacle_position - current_position
        distance = np.linalg.norm(to_obstacle)
        
        if distance > avoidance_distance:
            return current_direction
        
        # Calculate avoidance direction (perpendicular to obstacle direction)
        obstacle_dir = to_obstacle / distance
        
        # Find perpendicular direction in the plane
        perp = np.cross(current_direction, obstacle_dir)
        if np.linalg.norm(perp) < 1e-6:
            return current_direction
        
        perp = perp / np.linalg.norm(perp)
        avoid_dir = np.cross(perp, obstacle_dir)
        avoid_dir = avoid_dir / np.linalg.norm(avoid_dir)
        
        # Blend based on distance
        strength = max(0, 1 - distance / avoidance_distance)
        new_direction = (1 - strength) * current_direction + strength * avoid_dir
        new_direction = new_direction / np.linalg.norm(new_direction)
        
        return new_direction
    
    @staticmethod
    def growth_iteration(segments: List[Dict],
                        light_sources: List[np.ndarray],
                        obstacles: List[np.ndarray],
                        energy_decay: float = 0.95) -> List[Dict]:
        """
        Perform one iteration of growth simulation.
        
        Args:
            segments: List of segment dictionaries
            light_sources: List of light source positions
            obstacles: List of obstacle positions
            energy_decay: Energy decay per iteration
            
        Returns:
            Updated list of segments
        """
        new_segments = []
        
        for segment in segments:
            # Skip if energy too low
            if segment.get('energy', 1.0) < 0.1:
                new_segments.append(segment)
                continue
            
            # Update age
            segment['age'] = segment.get('age', 0) + 1
            
            # Calculate net light direction
            position = segment.get('position', np.array([0, 0, 0]))
            direction = segment.get('direction', np.array([0, 0, 1]))
            
            light_direction = np.zeros(3)
            for light_pos in light_sources:
                to_light = light_pos - position
                light_direction += to_light / (np.linalg.norm(to_light) + 1)
            
            if np.linalg.norm(light_direction) > 1e-6:
                light_direction = light_direction / np.linalg.norm(light_direction)
                
                # Apply phototropism
                direction = GrowthRules.phototropism(direction, light_direction, 0.2)
            
            # Apply gravitropism (slight upward bias)
            direction = GrowthRules.gravitropism(direction, 0.1, positive=True)
            
            # Avoid obstacles
            for obstacle_pos in obstacles:
                direction = GrowthRules.thigmotropism(
                    direction, obstacle_pos, position, avoidance_distance=2.0
                )
            
            # Update position
            growth_rate = segment.get('growth_rate', 1.0)
            new_position = position + direction * growth_rate
            
            # Update energy
            energy = segment.get('energy', 1.0) * energy_decay
            
            # Create new segment
            new_segment = {
                'position': new_position,
                'direction': direction,
                'energy': energy,
                'age': segment['age'],
                'growth_rate': growth_rate,
                'parent_id': segment.get('id', -1)
            }
            
            new_segments.append(new_segment)
            
            # Check for branching
            if GrowthRules.branching_condition(segment['age'], energy):
                # Create branch
                branch_angle = np.radians(30)
                rotation_axis = np.array([1, 0, 0])  # Simplified
                
                # Rotate direction for branch
                cos_a = np.cos(branch_angle)
                sin_a = np.sin(branch_angle)
                # Simplified rotation
                branch_direction = direction.copy()
                branch_direction[0] += sin_a
                branch_direction = branch_direction / np.linalg.norm(branch_direction)
                
                branch_segment = {
                    'position': new_position,
                    'direction': branch_direction,
                    'energy': energy * 0.6,
                    'age': 0,
                    'growth_rate': growth_rate * 0.8,
                    'parent_id': segment.get('id', -1)
                }
                new_segments.append(branch_segment)
        
        return new_segments
