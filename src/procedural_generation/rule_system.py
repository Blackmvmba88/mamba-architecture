"""
Rule-Based Generator - Generate structures using production rules.
"""

import numpy as np
from typing import Dict, List, Tuple


class RuleBasedGenerator:
    """Generate structures using rule systems."""
    
    @staticmethod
    def l_system_generate(axiom: str,
                         rules: Dict[str, str],
                         iterations: int) -> str:
        """
        Generate L-System string.
        
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
    def shape_grammar_2d(initial_shape: str,
                        rules: Dict[str, List[str]],
                        iterations: int) -> List[str]:
        """
        Apply shape grammar rules.
        
        Args:
            initial_shape: Starting shape
            rules: Shape transformation rules
            iterations: Number of iterations
            
        Returns:
            List of shapes
        """
        shapes = [initial_shape]
        
        for _ in range(iterations):
            new_shapes = []
            for shape in shapes:
                if shape in rules and rules[shape]:
                    # Replace with rule application
                    replacements = rules[shape]
                    if isinstance(replacements, list):
                        new_shapes.extend(replacements)
                    else:
                        new_shapes.append(replacements)
                else:
                    new_shapes.append(shape)
            shapes = new_shapes
        
        return shapes
    
    @staticmethod
    def cellular_automaton_1d(initial_state: np.ndarray,
                             rule_number: int,
                             steps: int) -> np.ndarray:
        """
        Generate 1D cellular automaton (Wolfram rules).
        
        Args:
            initial_state: Initial binary state array
            rule_number: Rule number (0-255)
            steps: Number of steps to simulate
            
        Returns:
            2D array of states (steps x width)
        """
        width = len(initial_state)
        states = np.zeros((steps, width), dtype=int)
        states[0] = initial_state
        
        # Convert rule number to binary lookup table
        rule_binary = format(rule_number, '08b')
        lookup = {format(i, '03b'): int(rule_binary[7-i]) for i in range(8)}
        
        for step in range(1, steps):
            for i in range(width):
                left = states[step-1, (i-1) % width]
                center = states[step-1, i]
                right = states[step-1, (i+1) % width]
                
                neighborhood = f"{left}{center}{right}"
                states[step, i] = lookup[neighborhood]
        
        return states
    
    @staticmethod
    def cellular_automaton_2d(initial_state: np.ndarray,
                             steps: int,
                             rule: str = 'game_of_life') -> np.ndarray:
        """
        Generate 2D cellular automaton.
        
        Args:
            initial_state: Initial binary state (height x width)
            steps: Number of steps
            rule: Rule name ('game_of_life', 'seeds', 'maze')
            
        Returns:
            3D array of states (steps x height x width)
        """
        height, width = initial_state.shape
        states = np.zeros((steps, height, width), dtype=int)
        states[0] = initial_state
        
        for step in range(1, steps):
            current = states[step-1]
            new_state = np.zeros_like(current)
            
            for i in range(height):
                for j in range(width):
                    # Count neighbors (Moore neighborhood)
                    neighbors = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = (i + di) % height, (j + dj) % width
                            neighbors += current[ni, nj]
                    
                    # Apply rule
                    if rule == 'game_of_life':
                        if current[i, j] == 1:
                            new_state[i, j] = 1 if neighbors in [2, 3] else 0
                        else:
                            new_state[i, j] = 1 if neighbors == 3 else 0
                    
                    elif rule == 'seeds':
                        new_state[i, j] = 1 if neighbors == 2 else 0
                    
                    elif rule == 'maze':
                        if current[i, j] == 1:
                            new_state[i, j] = 1 if neighbors in [1, 2, 3, 4, 5] else 0
                        else:
                            new_state[i, j] = 1 if neighbors == 3 else 0
            
            states[step] = new_state
        
        return states
    
    @staticmethod
    def subdivision_surface(vertices: np.ndarray,
                           faces: np.ndarray,
                           iterations: int = 1) -> Dict:
        """
        Apply Catmull-Clark subdivision.
        
        Args:
            vertices: Initial vertices
            faces: Initial faces
            iterations: Number of subdivision iterations
            
        Returns:
            Dictionary with subdivided mesh
        """
        for _ in range(iterations):
            new_vertices = list(vertices)
            new_faces = []
            
            # Calculate face points
            face_points = {}
            for i, face in enumerate(faces):
                face_verts = vertices[face]
                face_point = np.mean(face_verts, axis=0)
                face_points[i] = len(new_vertices)
                new_vertices.append(face_point)
            
            # Calculate edge points (simplified)
            edge_points = {}
            for face_idx, face in enumerate(faces):
                n = len(face)
                for i in range(n):
                    v1, v2 = face[i], face[(i+1) % n]
                    edge = tuple(sorted([v1, v2]))
                    
                    if edge not in edge_points:
                        edge_point = (vertices[v1] + vertices[v2]) / 2
                        edge_points[edge] = len(new_vertices)
                        new_vertices.append(edge_point)
            
            # Create new faces (simplified quad subdivision)
            for face_idx, face in enumerate(faces):
                fp = face_points[face_idx]
                n = len(face)
                
                for i in range(n):
                    v = face[i]
                    e1 = tuple(sorted([face[i], face[(i+1) % n]]))
                    e2 = tuple(sorted([face[i], face[(i-1) % n]]))
                    
                    new_face = [v, edge_points[e1], fp, edge_points[e2]]
                    new_faces.append(new_face)
            
            vertices = np.array(new_vertices)
            faces = np.array(new_faces)
        
        return {
            'vertices': vertices,
            'faces': faces
        }
