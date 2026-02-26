"""
Mesh Exporter - Export organic models to standard 3D formats.
"""

import numpy as np
from typing import Dict, List


class MeshExporter:
    """Export meshes to various 3D file formats."""
    
    @staticmethod
    def to_obj(vertices: np.ndarray,
               faces: np.ndarray,
               filename: str,
               normals: np.ndarray = None):
        """
        Export mesh to Wavefront OBJ format.
        
        Args:
            vertices: Vertex array (N x 3)
            faces: Face array (M x 3 or M x 4)
            filename: Output filename
            normals: Optional vertex normals
        """
        with open(filename, 'w') as f:
            f.write("# Mamba Architecture - Organic Model\n")
            f.write(f"# Vertices: {len(vertices)}\n")
            f.write(f"# Faces: {len(faces)}\n\n")
            
            # Write vertices
            for v in vertices:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            
            # Write normals if provided
            if normals is not None:
                f.write("\n")
                for n in normals:
                    f.write(f"vn {n[0]:.6f} {n[1]:.6f} {n[2]:.6f}\n")
            
            # Write faces (OBJ indices start at 1)
            f.write("\n")
            for face in faces:
                if normals is not None:
                    face_str = " ".join([f"{v+1}//{v+1}" for v in face])
                else:
                    face_str = " ".join([str(v+1) for v in face])
                f.write(f"f {face_str}\n")
    
    @staticmethod
    def to_stl(vertices: np.ndarray,
               faces: np.ndarray,
               filename: str,
               binary: bool = False):
        """
        Export mesh to STL format (for 3D printing).
        
        Args:
            vertices: Vertex array (N x 3)
            faces: Face array (M x 3)
            filename: Output filename
            binary: Use binary format (more compact)
        """
        if binary:
            MeshExporter._to_stl_binary(vertices, faces, filename)
        else:
            MeshExporter._to_stl_ascii(vertices, faces, filename)
    
    @staticmethod
    def _to_stl_ascii(vertices: np.ndarray,
                     faces: np.ndarray,
                     filename: str):
        """Write ASCII STL file."""
        with open(filename, 'w') as f:
            f.write("solid MambaArchitecture\n")
            
            for face in faces:
                # Get face vertices
                v1, v2, v3 = vertices[face[:3]]
                
                # Calculate normal
                edge1 = v2 - v1
                edge2 = v3 - v1
                normal = np.cross(edge1, edge2)
                normal = normal / (np.linalg.norm(normal) + 1e-10)
                
                f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
                f.write("    outer loop\n")
                f.write(f"      vertex {v1[0]:.6f} {v1[1]:.6f} {v1[2]:.6f}\n")
                f.write(f"      vertex {v2[0]:.6f} {v2[1]:.6f} {v2[2]:.6f}\n")
                f.write(f"      vertex {v3[0]:.6f} {v3[1]:.6f} {v3[2]:.6f}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")
            
            f.write("endsolid MambaArchitecture\n")
    
    @staticmethod
    def _to_stl_binary(vertices: np.ndarray,
                      faces: np.ndarray,
                      filename: str):
        """Write binary STL file."""
        import struct
        
        with open(filename, 'wb') as f:
            # Header (80 bytes)
            header = b'Mamba Architecture Binary STL' + b'\x00' * 51
            f.write(header)
            
            # Number of triangles
            f.write(struct.pack('<I', len(faces)))
            
            for face in faces:
                # Get face vertices
                v1, v2, v3 = vertices[face[:3]]
                
                # Calculate normal
                edge1 = v2 - v1
                edge2 = v3 - v1
                normal = np.cross(edge1, edge2)
                normal = normal / (np.linalg.norm(normal) + 1e-10)
                
                # Write normal (3 floats)
                f.write(struct.pack('<3f', *normal))
                
                # Write vertices (9 floats)
                f.write(struct.pack('<3f', *v1))
                f.write(struct.pack('<3f', *v2))
                f.write(struct.pack('<3f', *v3))
                
                # Attribute byte count (2 bytes, usually 0)
                f.write(struct.pack('<H', 0))
    
    @staticmethod
    def to_gltf(vertices: np.ndarray,
                faces: np.ndarray,
                filename: str,
                normals: np.ndarray = None,
                colors: np.ndarray = None):
        """
        Export mesh to glTF format (for web visualization).
        
        Args:
            vertices: Vertex array (N x 3)
            faces: Face array (M x 3)
            filename: Output filename
            normals: Optional vertex normals
            colors: Optional vertex colors (N x 3, RGB 0-1)
        """
        import json
        import base64
        
        # Calculate normals if not provided
        if normals is None:
            normals = MeshExporter._calculate_vertex_normals(vertices, faces)
        
        # Prepare binary data
        vertex_data = vertices.astype(np.float32).tobytes()
        normal_data = normals.astype(np.float32).tobytes()
        index_data = faces.astype(np.uint32).tobytes()
        
        # Combine all binary data
        binary_data = vertex_data + normal_data + index_data
        
        # Create glTF JSON structure
        gltf = {
            "asset": {
                "version": "2.0",
                "generator": "Mamba Architecture"
            },
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [{
                "primitives": [{
                    "attributes": {
                        "POSITION": 0,
                        "NORMAL": 1
                    },
                    "indices": 2
                }]
            }],
            "buffers": [{
                "byteLength": len(binary_data),
                "uri": f"data:application/octet-stream;base64,{base64.b64encode(binary_data).decode()}"
            }],
            "bufferViews": [
                {
                    "buffer": 0,
                    "byteOffset": 0,
                    "byteLength": len(vertex_data),
                    "target": 34962
                },
                {
                    "buffer": 0,
                    "byteOffset": len(vertex_data),
                    "byteLength": len(normal_data),
                    "target": 34962
                },
                {
                    "buffer": 0,
                    "byteOffset": len(vertex_data) + len(normal_data),
                    "byteLength": len(index_data),
                    "target": 34963
                }
            ],
            "accessors": [
                {
                    "bufferView": 0,
                    "componentType": 5126,
                    "count": len(vertices),
                    "type": "VEC3",
                    "max": vertices.max(axis=0).tolist(),
                    "min": vertices.min(axis=0).tolist()
                },
                {
                    "bufferView": 1,
                    "componentType": 5126,
                    "count": len(normals),
                    "type": "VEC3"
                },
                {
                    "bufferView": 2,
                    "componentType": 5125,
                    "count": len(faces) * 3,
                    "type": "SCALAR"
                }
            ]
        }
        
        # Write JSON file
        with open(filename, 'w') as f:
            json.dump(gltf, f, indent=2)
    
    @staticmethod
    def _calculate_vertex_normals(vertices: np.ndarray,
                                  faces: np.ndarray) -> np.ndarray:
        """Calculate vertex normals from faces."""
        normals = np.zeros_like(vertices)
        
        for face in faces:
            v1, v2, v3 = vertices[face[:3]]
            edge1 = v2 - v1
            edge2 = v3 - v1
            face_normal = np.cross(edge1, edge2)
            
            # Add to vertex normals
            for vertex_idx in face[:3]:
                normals[vertex_idx] += face_normal
        
        # Normalize
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = normals / (norms + 1e-10)
        
        return normals
