"""
Platonic Solids - The five perfect 3D forms in sacred geometry.
Represents the building blocks of the universe in sacred traditions.
"""

import numpy as np
from typing import Tuple, Dict, List


class PlatonicSolids:
    """Generate vertices, edges, and faces for the five Platonic solids."""
    
    @staticmethod
    def tetrahedron() -> Dict[str, np.ndarray]:
        """
        Generate tetrahedron (4 faces, represents Fire).
        
        Returns:
            Dictionary with vertices, edges, faces
        """
        vertices = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1]
        ], dtype=float)
        
        # Normalize to unit sphere
        vertices = vertices / np.linalg.norm(vertices[0])
        
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        
        return {
            'name': 'Tetrahedron',
            'element': 'Fire',
            'vertices': vertices,
            'faces': faces,
            'num_vertices': 4,
            'num_faces': 4,
            'num_edges': 6
        }
    
    @staticmethod
    def cube() -> Dict[str, np.ndarray]:
        """
        Generate cube/hexahedron (6 faces, represents Earth).
        
        Returns:
            Dictionary with vertices, edges, faces
        """
        vertices = np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]
        ], dtype=float) / np.sqrt(3)
        
        faces = np.array([
            [0, 1, 2, 3],  # bottom
            [4, 5, 6, 7],  # top
            [0, 1, 5, 4],  # front
            [2, 3, 7, 6],  # back
            [0, 3, 7, 4],  # left
            [1, 2, 6, 5]   # right
        ])
        
        return {
            'name': 'Cube',
            'element': 'Earth',
            'vertices': vertices,
            'faces': faces,
            'num_vertices': 8,
            'num_faces': 6,
            'num_edges': 12
        }
    
    @staticmethod
    def octahedron() -> Dict[str, np.ndarray]:
        """
        Generate octahedron (8 faces, represents Air).
        
        Returns:
            Dictionary with vertices, edges, faces
        """
        vertices = np.array([
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
            [0, 0, 1],
            [0, 0, -1]
        ], dtype=float)
        
        faces = np.array([
            [0, 2, 4],
            [0, 4, 3],
            [0, 3, 5],
            [0, 5, 2],
            [1, 2, 5],
            [1, 5, 3],
            [1, 3, 4],
            [1, 4, 2]
        ])
        
        return {
            'name': 'Octahedron',
            'element': 'Air',
            'vertices': vertices,
            'faces': faces,
            'num_vertices': 6,
            'num_faces': 8,
            'num_edges': 12
        }
    
    @staticmethod
    def dodecahedron() -> Dict[str, np.ndarray]:
        """
        Generate dodecahedron (12 faces, represents Ether/Universe).
        
        Returns:
            Dictionary with vertices, edges, faces
        """
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        vertices = np.array([
            # Cube vertices
            [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
            [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
            # Rectangle vertices using golden ratio
            [0, phi, 1/phi], [0, phi, -1/phi], [0, -phi, 1/phi], [0, -phi, -1/phi],
            [1/phi, 0, phi], [1/phi, 0, -phi], [-1/phi, 0, phi], [-1/phi, 0, -phi],
            [phi, 1/phi, 0], [phi, -1/phi, 0], [-phi, 1/phi, 0], [-phi, -1/phi, 0]
        ], dtype=float)
        
        # Normalize to unit sphere
        vertices = vertices / np.linalg.norm(vertices[0])
        
        faces = np.array([
            [0, 16, 17, 2, 12],
            [0, 12, 14, 4, 8],
            [0, 8, 9, 1, 16],
            [1, 9, 5, 15, 13],
            [1, 13, 3, 17, 16],
            [2, 17, 3, 11, 10],
            [2, 10, 6, 14, 12],
            [3, 13, 15, 7, 11],
            [4, 14, 6, 19, 18],
            [4, 18, 5, 9, 8],
            [5, 18, 19, 7, 15],
            [6, 10, 11, 7, 19]
        ])
        
        return {
            'name': 'Dodecahedron',
            'element': 'Ether',
            'vertices': vertices,
            'faces': faces,
            'num_vertices': 20,
            'num_faces': 12,
            'num_edges': 30
        }
    
    @staticmethod
    def icosahedron() -> Dict[str, np.ndarray]:
        """
        Generate icosahedron (20 faces, represents Water).
        
        Returns:
            Dictionary with vertices, edges, faces
        """
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        vertices = np.array([
            [0, 1, phi],
            [0, 1, -phi],
            [0, -1, phi],
            [0, -1, -phi],
            [1, phi, 0],
            [1, -phi, 0],
            [-1, phi, 0],
            [-1, -phi, 0],
            [phi, 0, 1],
            [phi, 0, -1],
            [-phi, 0, 1],
            [-phi, 0, -1]
        ], dtype=float)
        
        # Normalize to unit sphere
        vertices = vertices / np.linalg.norm(vertices[0])
        
        faces = np.array([
            [0, 2, 8], [0, 8, 4], [0, 4, 6], [0, 6, 10], [0, 10, 2],
            [2, 10, 7], [2, 7, 5], [2, 5, 8], [8, 5, 9], [8, 9, 4],
            [4, 9, 1], [4, 1, 6], [6, 1, 11], [6, 11, 10], [10, 11, 7],
            [3, 9, 5], [3, 5, 7], [3, 7, 11], [3, 11, 1], [3, 1, 9]
        ])
        
        return {
            'name': 'Icosahedron',
            'element': 'Water',
            'vertices': vertices,
            'faces': faces,
            'num_vertices': 12,
            'num_faces': 20,
            'num_edges': 30
        }
    
    @classmethod
    def all_solids(cls) -> List[Dict]:
        """
        Get all five Platonic solids.
        
        Returns:
            List of all Platonic solid dictionaries
        """
        return [
            cls.tetrahedron(),
            cls.cube(),
            cls.octahedron(),
            cls.dodecahedron(),
            cls.icosahedron()
        ]
