"""
Organic Morphology - Natural form generation and transformation.
"""

import numpy as np
from typing import List, Dict, Tuple, Callable


class OrganicMorphology:
    """Generate and transform organic forms."""
    
    @staticmethod
    def blob_surface(center: np.ndarray,
                    radius: float,
                    irregularity: float = 0.2,
                    resolution: int = 20) -> np.ndarray:
        """
        Generate organic blob surface.
        
        Args:
            center: Center position [x, y, z]
            radius: Base radius
            irregularity: Amount of irregular deformation (0-1)
            resolution: Mesh resolution
            
        Returns:
            Array of vertices
        """
        u = np.linspace(0, 2*np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        U, V = np.meshgrid(u, v)
        
        # Add Perlin-like noise for irregularity
        noise = np.random.randn(resolution, resolution) * irregularity
        r = radius * (1 + noise)
        
        # Spherical coordinates with noise
        x = center[0] + r * np.sin(V) * np.cos(U)
        y = center[1] + r * np.sin(V) * np.sin(U)
        z = center[2] + r * np.cos(V)
        
        vertices = np.stack([x, y, z], axis=-1)
        return vertices
    
    @staticmethod
    def spine_curve(start: np.ndarray,
                   end: np.ndarray,
                   control_points: List[np.ndarray],
                   segments: int = 50) -> np.ndarray:
        """
        Generate smooth spine curve using Catmull-Rom spline.
        
        Args:
            start: Start point
            end: End point
            control_points: Intermediate control points
            segments: Number of segments
            
        Returns:
            Array of curve points
        """
        # Create point list
        points = [start] + control_points + [end]
        n_points = len(points)
        
        if n_points < 2:
            return np.array([start])
        
        # Generate curve
        curve_points = []
        for i in range(n_points - 1):
            t = np.linspace(0, 1, segments // (n_points - 1))
            
            p0 = points[max(0, i - 1)]
            p1 = points[i]
            p2 = points[i + 1]
            p3 = points[min(n_points - 1, i + 2)]
            
            for t_val in t:
                # Catmull-Rom spline
                point = 0.5 * (
                    (2 * p1) +
                    (-p0 + p2) * t_val +
                    (2*p0 - 5*p1 + 4*p2 - p3) * t_val**2 +
                    (-p0 + 3*p1 - 3*p2 + p3) * t_val**3
                )
                curve_points.append(point)
        
        return np.array(curve_points)
    
    @staticmethod
    def skin_surface(spine: np.ndarray,
                    radius_function: Callable[[float], float],
                    cross_section_points: int = 16) -> Dict:
        """
        Generate skin surface around a spine curve.
        
        Args:
            spine: Spine curve points (N x 3)
            radius_function: Function that returns radius at parameter t (0-1)
            cross_section_points: Number of points in cross-section
            
        Returns:
            Dictionary with vertices and faces
        """
        n_spine = len(spine)
        vertices = []
        
        # Generate cross-sections along spine
        for i, point in enumerate(spine):
            t = i / (n_spine - 1)
            radius = radius_function(t)
            
            # Calculate local coordinate system
            if i < n_spine - 1:
                tangent = spine[i + 1] - spine[i]
            else:
                tangent = spine[i] - spine[i - 1]
            
            tangent = tangent / np.linalg.norm(tangent)
            
            # Find perpendicular vectors
            if abs(tangent[2]) < 0.9:
                up = np.array([0, 0, 1])
            else:
                up = np.array([1, 0, 0])
            
            right = np.cross(tangent, up)
            right = right / np.linalg.norm(right)
            up = np.cross(right, tangent)
            
            # Generate circle of vertices
            for j in range(cross_section_points):
                angle = 2 * np.pi * j / cross_section_points
                offset = radius * (np.cos(angle) * right + np.sin(angle) * up)
                vertex = point + offset
                vertices.append(vertex)
        
        vertices = np.array(vertices)
        
        # Generate faces
        faces = []
        for i in range(n_spine - 1):
            for j in range(cross_section_points):
                j_next = (j + 1) % cross_section_points
                
                v1 = i * cross_section_points + j
                v2 = i * cross_section_points + j_next
                v3 = (i + 1) * cross_section_points + j_next
                v4 = (i + 1) * cross_section_points + j
                
                faces.append([v1, v2, v3])
                faces.append([v1, v3, v4])
        
        return {
            'vertices': vertices,
            'faces': np.array(faces)
        }
    
    @staticmethod
    def parametric_deformation(vertices: np.ndarray,
                              deformation_func: Callable,
                              strength: float = 1.0) -> np.ndarray:
        """
        Apply parametric deformation to vertices.
        
        Args:
            vertices: Input vertices (N x 3)
            deformation_func: Function that takes (x, y, z) and returns offset
            strength: Deformation strength
            
        Returns:
            Deformed vertices
        """
        deformed = vertices.copy()
        
        for i, vertex in enumerate(vertices):
            offset = deformation_func(vertex[0], vertex[1], vertex[2])
            deformed[i] += np.array(offset) * strength
        
        return deformed
    
    @staticmethod
    def metamorphosis(shape_a: np.ndarray,
                     shape_b: np.ndarray,
                     t: float) -> np.ndarray:
        """
        Morph between two shapes.
        
        Args:
            shape_a: First shape vertices
            shape_b: Second shape vertices
            t: Interpolation parameter (0-1)
            
        Returns:
            Interpolated shape
        """
        if shape_a.shape != shape_b.shape:
            raise ValueError("Shapes must have same number of vertices")
        
        return (1 - t) * shape_a + t * shape_b
    
    @staticmethod
    def fractal_subdivision(vertices: np.ndarray,
                           faces: np.ndarray,
                           displacement_factor: float = 0.1) -> Dict:
        """
        Subdivide mesh with fractal displacement.
        
        Args:
            vertices: Initial vertices
            faces: Initial faces
            displacement_factor: Amount of random displacement
            
        Returns:
            Dictionary with subdivided mesh
        """
        new_vertices = list(vertices)
        new_faces = []
        edge_midpoints = {}
        
        def get_midpoint(v1, v2):
            edge = tuple(sorted([v1, v2]))
            if edge not in edge_midpoints:
                midpoint = (vertices[v1] + vertices[v2]) / 2
                # Add random displacement
                displacement = np.random.randn(3) * displacement_factor
                midpoint += displacement
                edge_midpoints[edge] = len(new_vertices)
                new_vertices.append(midpoint)
            return edge_midpoints[edge]
        
        # Subdivide each face
        for face in faces:
            v1, v2, v3 = face[:3]
            
            # Get midpoints
            m12 = get_midpoint(v1, v2)
            m23 = get_midpoint(v2, v3)
            m31 = get_midpoint(v3, v1)
            
            # Create 4 new faces
            new_faces.append([v1, m12, m31])
            new_faces.append([m12, v2, m23])
            new_faces.append([m31, m23, v3])
            new_faces.append([m12, m23, m31])
        
        return {
            'vertices': np.array(new_vertices),
            'faces': np.array(new_faces)
        }
    
    @staticmethod
    def cellular_structure(bounds: Tuple[float, float, float],
                          n_cells: int = 20,
                          min_cell_size: float = 0.5) -> List[Dict]:
        """
        Generate organic cellular structure.
        
        Args:
            bounds: Bounding box (width, height, depth)
            n_cells: Number of cells
            min_cell_size: Minimum cell size
            
        Returns:
            List of cell dictionaries
        """
        from scipy.spatial import Voronoi
        
        # Generate random seed points
        points = np.random.rand(n_cells, 3) * np.array(bounds)
        
        # Create 3D Voronoi
        vor = Voronoi(points)
        
        cells = []
        for region_idx, region in enumerate(vor.regions):
            if len(region) > 0 and -1 not in region:
                cell_vertices = vor.vertices[region]
                
                # Calculate cell properties
                center = np.mean(cell_vertices, axis=0)
                size = np.std(cell_vertices, axis=0).mean()
                
                if size >= min_cell_size:
                    cells.append({
                        'center': center,
                        'vertices': cell_vertices,
                        'size': size,
                        'region_idx': region_idx
                    })
        
        return cells
