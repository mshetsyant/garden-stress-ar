#!/usr/bin/env python3
"""
Generate sparse point cloud for garden stress monitoring.
Real coordinates: 40.33105186237493, 44.59644202143014 (Bulgaria)
Creates 12 sample points with stress detection.
"""

import numpy as np
import json
from pathlib import Path

try:
    import trimesh
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "trimesh"])
    import trimesh

def generate_garden_point_cloud(lat=40.33105186237493, lon=44.59644202143014, n_points=12):
    """
    Generate sparse garden sensor points (12 key monitoring locations).

    Returns:
        dict with points and metadata
    """
    np.random.seed(42)

    # Strategically placed monitoring points in 10m x 10m garden
    x = np.array([1.0, 2.5, 4.0, 5.0, 6.5, 8.0, 9.0,
                  1.5, 3.0, 5.5, 7.5, 8.5])
    y = np.array([1.0, 2.0, 1.5, 5.0, 3.0, 7.0, 8.5,
                  7.5, 8.0, 9.0, 5.5, 2.5])
    z = np.ones(n_points) * 0.5  # Ground level

    # Health index (NDRE)
    ndre = np.array([0.52, 0.48, 0.55, 0.18, 0.51, 0.49, 0.54,
                     0.50, 0.53, 0.15, 0.47, 0.56])

    stress_mask = ndre < 0.30

    data = {
        'coordinates': {
            'latitude': lat,
            'longitude': lon,
            'reference_point': 'Garden center'
        },
        'points': {
            'x': x.tolist(),
            'y': y.tolist(),
            'z': z.tolist(),
            'ndre': ndre.tolist(),
            'stress': stress_mask.tolist()
        },
        'stress_zone': {
            'count': int(np.sum(stress_mask)),
            'healthy_count': int(np.sum(~stress_mask))
        },
        'garden': {
            'width': 10.0,
            'length': 10.0
        }
    }

    return data

def create_point_cloud_glb(data):
    """
    Create minimal GLB with small spheres for each monitoring point.
    """
    x = np.array(data['points']['x'])
    y = np.array(data['points']['y'])
    z = np.array(data['points']['z'])
    ndre = np.array(data['points']['ndre'])

    # Create mesh with tiny spheres
    all_vertices = []
    all_faces = []
    all_colors = []

    vertex_offset = 0
    sphere_radius = 0.08

    for i in range(len(x)):
        sphere = trimesh.creation.icosphere(subdivisions=0, radius=sphere_radius)

        sphere.vertices[:, 0] += x[i]
        sphere.vertices[:, 1] += y[i]
        sphere.vertices[:, 2] += z[i]

        # Color gradient based on NDRE (green to red)
        if ndre[i] < 0.30:
            color = np.array([255, 60, 60, 255])  # Red - stressed
        elif ndre[i] < 0.40:
            color = np.array([255, 180, 60, 255])  # Orange - warning
        else:
            color = np.array([100, 220, 100, 255])  # Green - healthy

        all_vertices.append(sphere.vertices)
        all_faces.append(sphere.faces + vertex_offset)
        all_colors.extend([color] * len(sphere.vertices))

        vertex_offset += len(sphere.vertices)

    vertices = np.vstack(all_vertices)
    faces = np.vstack(all_faces)
    colors = np.array(all_colors, dtype=np.uint8)

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.visual.vertex_colors = colors

    return mesh

def main():
    print("-" * 60)
    print("Garden Point Cloud Generator")
    print("-" * 60)

    print("\n[1/3] Generating point cloud from garden coordinates...")
    data = generate_garden_point_cloud()
    print(f"  [OK] Generated {len(data['points']['x'])} points")
    print(f"  [OK] Latitude: {data['coordinates']['latitude']}")
    print(f"  [OK] Longitude: {data['coordinates']['longitude']}")
    print(f"  [OK] Stress points detected: {data['stress_zone']['count']}")

    print("\n[2/3] Creating 3D point cloud mesh...")
    mesh = create_point_cloud_glb(data)
    print(f"  [OK] Created mesh with {len(mesh.vertices)} vertices")

    print("\n[3/3] Exporting as GLB...")
    mesh.export('pointcloud.glb')
    print(f"  [OK] Exported to: pointcloud.glb")

    # Save metadata
    with open('pointcloud_metadata.json', 'w') as f:
        json.dump({
            'coordinates': data['coordinates'],
            'stress_zone': data['stress_zone'],
            'garden': data['garden'],
            'total_points': len(data['points']['x'])
        }, f, indent=2)

    print("\n" + "-" * 60)
    print("Ready for deployment!")
    print("-" * 60)

if __name__ == '__main__':
    main()
