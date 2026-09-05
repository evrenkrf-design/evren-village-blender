#!/usr/bin/env python3
"""
Evren Village Blender Utilities

Common helper functions for procedural generation, scene setup, and asset management.

Usage (in Blender Python Console):
    import sys
    sys.path.append('/path/to/scripts')
    from utils import *
    create_evren_scene()
"""

import bpy
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

DEBUG = True
PROJECT_ROOT = Path(bpy.data.filepath).parent.parent if bpy.data.filepath else Path.cwd()
ASSET_PATH = PROJECT_ROOT / "assets"
RENDER_OUTPUT = PROJECT_ROOT / "renders"

# Evren Village Master Plan Dimensions (meters, 2px = 1m scale)
VILLAGE_WIDTH = 600  # meters
VILLAGE_HEIGHT = 500  # meters
VILLAGE_AREA = 300000  # m²

# ============================================================================
# LOGGING
# ============================================================================

def log(msg: str, level: str = "INFO"):
    """Print formatted log message."""
    prefix = f"[Evren {level}]"
    print(f"{prefix} {msg}")
    if DEBUG:
        print(f"  → {msg}")

def log_success(msg: str):
    log(f"✓ {msg}", "SUCCESS")

def log_error(msg: str):
    log(f"✗ {msg}", "ERROR")

def log_warning(msg: str):
    log(f"⚠ {msg}", "WARNING")

# ============================================================================
# SCENE MANAGEMENT
# ============================================================================

def clear_scene(keep_camera=True, keep_lights=True):
    """Clear all mesh objects from scene."""
    log("Clearing scene...")
    
    for obj in bpy.data.objects:
        # Keep camera and lights if specified
        if keep_camera and obj.type == 'CAMERA':
            continue
        if keep_lights and obj.type in ('LIGHT', 'SUN'):
            continue
        
        bpy.data.objects.remove(obj, do_unlink=True)
    
    log_success("Scene cleared")

def create_evren_scene():
    """Initialize Evren Village master scene with default setup."""
    log("Creating Evren Village scene...")
    
    # Clear existing
    clear_scene(keep_camera=True, keep_lights=True)
    
    # Set units to meters
    bpy.context.scene.unit_settings.length_unit = 'METERS'
    
    # Create master collection
    master_col = bpy.data.collections.new("Master Plan")
    bpy.context.scene.collection.children.link(master_col)
    
    # Create subcollections
    subcollections = [
        "Terrain",
        "Roads",
        "Zones",
        "Plots",
        "Facilities",
        "Water Systems",
        "Waste Systems",
        "Vegetation",
        "Aura Centre",
    ]
    
    for sub_name in subcollections:
        sub_col = bpy.data.collections.new(sub_name)
        master_col.children.link(sub_col)
    
    log_success(f"Scene created with {len(subcollections)} subcollections")
    return master_col

def get_collection(name: str, parent=None) -> bpy.types.Collection:
    """Get or create a collection by name."""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    
    col = bpy.data.collections.new(name)
    if parent:
        parent.children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    
    return col

# ============================================================================
# MATERIALS & TEXTURES
# ============================================================================

def create_material(name: str, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)) -> bpy.types.Material:
    """Create a simple material with specified color."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.7
    
    return mat

def assign_material(obj: bpy.types.Object, material: bpy.types.Material):
    """Assign material to object."""
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

# ============================================================================
# GEOMETRY CREATION
# ============================================================================

def create_plane(name: str, size: float = 1.0, location: Tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
    """Create a basic plane mesh."""
    bpy.ops.mesh.primitive_plane_add(
        size=size,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_cube(name: str, size: float = 1.0, location: Tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
    """Create a basic cube mesh."""
    bpy.ops.mesh.primitive_cube_add(
        size=size,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_circle(name: str, radius: float = 1.0, vertices: int = 32, location: Tuple[float, float, float] = (0, 0, 0)) -> bpy.types.Object:
    """Create a circle curve."""
    bpy.ops.curve.primitive_circle_add(
        radius=radius,
        location=location,
        vertices=vertices
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_curve_path(name: str, points: List[Tuple[float, float, float]]) -> bpy.types.Object:
    """Create a Bézier curve from list of points."""
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'
    
    polyline = curve_data.splines.new(type='BEZIER')
    polyline.points.add(len(points) - 1)
    
    for i, point in enumerate(points):
        x, y, z = point
        polyline.points[i].co = (x, y, z, 1)
    
    # Smooth curve
    polyline.resolution_u = 12
    polyline.use_smooth = True
    
    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    
    return obj

# ============================================================================
# TRANSFORMATIONS
# ============================================================================

def move_object(obj: bpy.types.Object, location: Tuple[float, float, float]):
    """Move object to specified location."""
    obj.location = location

def rotate_object(obj: bpy.types.Object, rotation: Tuple[float, float, float]):
    """Rotate object (in radians)."""
    obj.rotation_euler = rotation

def scale_object(obj: bpy.types.Object, scale: float | Tuple[float, float, float]):
    """Scale object uniformly or per-axis."""
    if isinstance(scale, (int, float)):
        obj.scale = (scale, scale, scale)
    else:
        obj.scale = scale

def get_object_bounds(obj: bpy.types.Object) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """Get bounding box min and max corners."""
    if not obj.data or not hasattr(obj.data, 'vertices'):
        return ((0, 0, 0), (0, 0, 0))
    
    coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
    x = [c.x for c in coords]
    y = [c.y for c in coords]
    z = [c.z for c in coords]
    
    return ((min(x), min(y), min(z)), (max(x), max(y), max(z)))

# ============================================================================
# CAMERA SETUP
# ============================================================================

def setup_camera(location: Tuple[float, float, float] = (300, 300, 250), target: Tuple[float, float, float] = (300, 250, 0)):
    """Setup camera looking at target."""
    # Create camera
    camera_data = bpy.data.cameras.new("Camera")
    camera_data.lens = 35  # mm
    camera_data.sensor_width = 36
    camera_data.sensor_height = 24
    
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    bpy.context.scene.camera = camera
    
    # Position and aim
    camera.location = location
    
    # Look at target
    direction = (
        target[0] - location[0],
        target[1] - location[1],
        target[2] - location[2]
    )
    
    rot_x = math.atan2(direction[2], math.sqrt(direction[0]**2 + direction[1]**2))
    rot_z = math.atan2(direction[1], direction[0])
    
    camera.rotation_euler = (rot_x, 0, rot_z + math.pi/2)
    
    log_success(f"Camera positioned at {location}")
    return camera

# ============================================================================
# LIGHTING SETUP
# ============================================================================

def setup_lighting(sun_energy: float = 2.0, use_hdri: bool = False):
    """Setup default 3-point lighting."""
    
    # Sun light (key light)
    sun_data = bpy.data.lights.new("Sun", type='SUN')
    sun_data.energy = sun_energy
    sun = bpy.data.objects.new("Sun", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.location = (300, -500, 400)
    sun.rotation_euler = (math.radians(45), math.radians(45), 0)
    
    # Sky
    world = bpy.context.scene.world
    world.use_nodes = True
    
    bg_node = world.node_tree.nodes["Background"]
    env_texture = world.node_tree.nodes.new(type='ShaderNodeTexSky')
    env_texture.sky_type = 'HOSEK_WILKIE'
    env_texture.sun_rotation = math.radians(180)
    env_texture.turbidity = 2.0
    
    world.node_tree.links.new(env_texture.outputs['Color'], bg_node.inputs['Background'])
    
    log_success(f"Lighting setup (sun energy: {sun_energy})")
    return sun

# ============================================================================
# RENDER SETUP
# ============================================================================

def configure_render_settings(engine: str = 'CYCLES', samples: int = 128, resolution: Tuple[int, int] = (1920, 1080)):
    """Configure render engine and output settings."""
    scene = bpy.context.scene
    
    # Engine
    scene.render.engine = engine
    
    # Resolution
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100
    
    # Samples
    if engine == 'CYCLES':
        scene.cycles.samples = samples
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = 'OPTIX' if 'OPTIX' in bpy.context.preferences.addons else 'OPENIMAGEDENOISE'
    elif engine == 'EEVEE':
        scene.eevee.taa_render_samples = samples
    
    # Output
    output_dir = RENDER_OUTPUT / "stills"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    scene.render.filepath = str(output_dir / "render_####.png")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    
    log_success(f"Render configured: {engine} {samples}s {resolution}")

# ============================================================================
# EXPORT UTILITIES
# ============================================================================

def export_fbx(filepath: str, selection_only: bool = False):
    """Export scene or selection as FBX."""
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=selection_only,
        use_mesh_modifiers=True,
        add_leaf_bones=False
    )
    log_success(f"Exported FBX: {filepath}")

def export_gltf(filepath: str, selection_only: bool = False):
    """Export scene or selection as glTF."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=selection_only,
        use_draco_compression=True
    )
    log_success(f"Exported glTF: {filepath}")

# ============================================================================
# DATA LOADING
# ============================================================================

def load_json(filepath: str) -> Dict:
    """Load JSON data file."""
    path = Path(filepath)
    if not path.exists():
        log_error(f"File not found: {filepath}")
        return {}
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    log_success(f"Loaded JSON: {filepath}")
    return data

def save_json(data: Dict, filepath: str):
    """Save data as JSON."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    
    log_success(f"Saved JSON: {filepath}")

# ============================================================================
# MAIN INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    log("Evren Village Blender Utilities loaded", "INIT")
    log(f"Project root: {PROJECT_ROOT}", "INIT")
    log(f"Asset path: {ASSET_PATH}", "INIT")
    log(f"Render output: {RENDER_OUTPUT}", "INIT")
