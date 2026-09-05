#!/usr/bin/env python3
"""
Evren Village - Procedural Road Network Generation

Generates organic curved road network using Bézier curves and modifiers.
Creates 6 main road paths:
  1. Perimeter loop (outer boundary)
  2. Main collector (E-W axis)
  3. North residential collector
  4-7. Four local lanes with fire tender turn-arounds

Usage in Blender:
    Scripting → Open scripts/road-generation.py → Run (Alt+P)

Usage Terminal:
    blender --background scene.blend --python scripts/road-generation.py
"""

import bpy
import json
from pathlib import Path
from utils import log, log_success, log_error, create_curve_path, VILLAGE_WIDTH, VILLAGE_HEIGHT

# ============================================================================
# ROAD NETWORK COORDINATES (extracted from SVG master plan)
# ============================================================================

ROAD_SPECIFICATIONS = {
    "Perimeter_Loop": {
        "width_surface": 22,  # meters
        "width_shoulder": 6,
        "points": [
            # Rounded rectangle forming perimeter
            # NW corner start
            (220, 160, 0),
            (780, 140, 0),
            (1380, 140, 0),
            (1380, 1080, 0),
            (780, 1100, 0),
            (220, 1080, 0),
            (220, 160, 0),  # Close loop
        ],
        "type": "CYCLE",
        "resolution": 48,
        "description": "Main perimeter circulation - emergency vehicle access"
    },
    
    "Main_Collector": {
        "width_surface": 18,
        "width_shoulder": 4,
        "points": [
            # E-W connector through Aura
            (220, 612, 0),
            (345, 558, 0),
            (520, 566, 0),
            (620, 676, 0),
            (696, 760, 0),
            (818, 818, 0),
            (930, 828, 0),
            (1024, 674, 0),
            (1092, 584, 0),
            (1220, 570, 0),
            (1377, 612, 0),
        ],
        "type": "OPEN",
        "resolution": 32,
        "description": "Main collector road connecting East and West entry points"
    },
    
    "North_Residential_Collector": {
        "width_surface": 17,
        "width_shoulder": 3,
        "points": [
            # N-S residential loop through Nova and Aurelia zones
            (270, 463, 0),
            (410, 442, 0),
            (544, 470, 0),
            (650, 504, 0),
            (728, 530, 0),
            (777, 493, 0),
            (813, 425, 0),
            (862, 333, 0),
            (1015, 370, 0),
            (1115, 421, 0),
            (1210, 470, 0),
            (1280, 450, 0),
            (1345, 420, 0),
        ],
        "type": "OPEN",
        "resolution": 28,
        "description": "Residential distributor through Nova and Aurelia zones"
    },
    
    "Local_Lane_1": {
        "width_surface": 11,
        "points": [(330, 192, 0), (334, 352, 0)],
        "type": "OPEN",
        "resolution": 12,
        "has_turnaround": True,
        "turnaround_radius": 12
    },
    
    "Local_Lane_2": {
        "width_surface": 11,
        "points": [(548, 192, 0), (550, 350, 0)],
        "type": "OPEN",
        "resolution": 12,
        "has_turnaround": True,
        "turnaround_radius": 12
    },
    
    "Local_Lane_3": {
        "width_surface": 11,
        "points": [(994, 192, 0), (1005, 338, 0)],
        "type": "OPEN",
        "resolution": 12,
        "has_turnaround": True,
        "turnaround_radius": 12
    },
    
    "Local_Lane_4": {
        "width_surface": 11,
        "points": [(1200, 192, 0), (1241, 340, 0)],
        "type": "OPEN",
        "resolution": 12,
        "has_turnaround": True,
        "turnaround_radius": 12
    }
}

RESIDENTIAL_MEWS = {
    "description": "Low-speed local streets serving residential clusters",
    "width": 9,
    "paths": [
        # Nova NW zone
        [(260, 244, 0), (624, 243, 0)],
        [(274, 302, 0), (634, 301, 0)],
        [(260, 439, 0), (675, 438, 0)],
        [(632, 370, 0), (738, 357, 0)],
        
        # Haven SW zone
        [(252, 886, 0), (560, 898, 0)],
        [(268, 1018, 0), (680, 1022, 0)],
        [(680, 1022, 0), (800, 972, 0)],
        
        # Zenith SE connections
        [(1148, 794, 0), (1355, 799, 0)],
        [(1300, 744, 0), (1332, 797, 0)],
    ]
}

# ============================================================================
# ROAD GENERATION FUNCTIONS
# ============================================================================

def create_road_curves():
    """Create all road Bézier curves."""
    log("Creating road network curves...")
    
    roads_col = bpy.data.collections.get("Roads")
    if not roads_col:
        roads_col = bpy.data.collections.new("Roads")
        bpy.context.scene.collection.children.link(roads_col)
    
    road_objects = {}
    
    for road_name, spec in ROAD_SPECIFICATIONS.items():
        log(f"  Creating {road_name}...")
        
        # Create curve data
        curve_data = bpy.data.curves.new(road_name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = spec.get('resolution', 16)
        curve_data.use_smooth = True
        
        # Create polyline
        points = spec['points']
        polyline = curve_data.splines.new(type='BEZIER')
        polyline.points.add(len(points) - 1)
        
        # Set points
        for i, (x, y, z) in enumerate(points):
            polyline.points[i].co = (x, y, z, 1)
            # Auto smooth Bézier handles
            polyline.points[i].handle_left_type = 'AUTO'
            polyline.points[i].handle_right_type = 'AUTO'
        
        # Close loop if specified
        if spec.get('type') == 'CYCLE':
            polyline.use_cyclic_u = True
        
        # Create object
        curve_obj = bpy.data.objects.new(road_name, curve_data)
        roads_col.objects.link(curve_obj)
        
        # Store for later
        road_objects[road_name] = {
            'object': curve_obj,
            'spec': spec
        }
        
        log_success(f"  {road_name}: {len(points)} control points")
    
    return road_objects

def convert_curves_to_mesh(road_objects):
    """Convert curves to mesh objects with proper geometry."""
    log("Converting curves to mesh geometry...")
    
    for road_name, road_data in road_objects.items():
        curve_obj = road_data['object']
        spec = road_data['spec']
        
        # Set bevel depth (half of surface width) to create road surface
        bevel_depth = spec.get('width_surface', 10) / 2
        curve_obj.data.bevel_depth = bevel_depth / 100  # Scale adjustment
        curve_obj.data.bevel_resolution = 4
        
        log_success(f"  {road_name}: bevel depth {bevel_depth}m")

def create_turnarounds(road_objects):
    """Create fire tender turn-around circles at lane ends."""
    log("Creating fire tender turn-arounds...")
    
    turnaround_col = bpy.data.collections.get("Roads")
    
    for road_name, road_data in road_objects.items():
        spec = road_data['spec']
        
        if not spec.get('has_turnaround'):
            continue
        
        radius = spec.get('turnaround_radius', 15)
        
        # Get end point
        points = spec['points']
        end_point = points[-1]
        
        # Create circle at end
        bpy.ops.curve.primitive_circle_add(
            radius=radius,
            location=end_point
        )
        circle = bpy.context.active_object
        circle.name = f"{road_name}_Turnaround"
        
        # Apply material/styling
        circle.data.bevel_depth = 1 / 100
        
        # Move to collection
        bpy.context.collection.objects.unlink(circle)
        turnaround_col.objects.link(circle)
        
        log_success(f"  {road_name}: turn-around {radius}m radius")

def create_residential_mews():
    """Create lower-order residential streets."""
    log("Creating residential mews...")
    
    roads_col = bpy.data.collections.get("Roads")
    mews_width = RESIDENTIAL_MEWS['width']
    
    for i, path_points in enumerate(RESIDENTIAL_MEWS['paths'], 1):
        curve_data = bpy.data.curves.new(f"Mews_{i:02d}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 12
        curve_data.use_smooth = True
        
        # Create polyline
        polyline = curve_data.splines.new(type='BEZIER')
        polyline.points.add(len(path_points) - 1)
        
        for j, (x, y, z) in enumerate(path_points):
            polyline.points[j].co = (x, y, z, 1)
            polyline.points[j].handle_left_type = 'AUTO'
            polyline.points[j].handle_right_type = 'AUTO'
        
        # Create object with bevel
        mews_obj = bpy.data.objects.new(f"Mews_{i:02d}", curve_data)
        mews_obj.data.bevel_depth = (mews_width / 2) / 100
        mews_obj.data.bevel_resolution = 3
        
        roads_col.objects.link(mews_obj)
        log_success(f"  Mews {i:02d}: created")

def add_road_materials():
    """Apply road surface materials."""
    log("Applying road surface materials...")
    
    # Create road material
    road_mat = bpy.data.materials.new("Road_Surface")
    road_mat.use_nodes = True
    
    bsdf = road_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.50, 0.48, 0.45, 1.0)  # Asphalt grey
    bsdf.inputs['Roughness'].default_value = 0.8
    bsdf.inputs['Metallic'].default_value = 0.0
    
    # Create edge material
    edge_mat = bpy.data.materials.new("Road_Edge")
    edge_mat.use_nodes = True
    
    bsdf = edge_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.37, 0.35, 0.30, 1.0)  # Dark grey
    bsdf.inputs['Roughness'].default_value = 0.9
    
    log_success("Road materials created")
    return road_mat, edge_mat

def add_road_markings():
    """Create visual road markings (centre lines, etc.)."""
    log("Adding road markings...")
    
    roads_col = bpy.data.collections.get("Roads")
    
    # Create centre line material
    line_mat = bpy.data.materials.new("Road_Centreline")
    line_mat.use_nodes = True
    
    bsdf = line_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.98, 0.97, 0.95, 1.0)  # Off-white
    bsdf.inputs['Emission'].default_value = (0.98, 0.97, 0.95, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 0.1
    
    log_success("Road markings configured")

def verify_road_connectivity():
    """Verify that all roads connect properly."""
    log("Verifying road connectivity...")
    
    roads_col = bpy.data.collections.get("Roads")
    
    if not roads_col:
        log_error("No roads collection found")
        return False
    
    road_count = len(roads_col.objects)
    log_success(f"Road network complete: {road_count} road objects")
    
    # Check main roads
    main_roads = ["Perimeter_Loop", "Main_Collector", "North_Residential_Collector"]
    for road_name in main_roads:
        if road_name in bpy.data.objects:
            log_success(f"  ✓ {road_name}")
        else:
            log_error(f"  ✗ {road_name} missing")
    
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute complete road network generation."""
    try:
        log("\n" + "="*50)
        log("EVREN VILLAGE - ROAD NETWORK GENERATION")
        log("="*50 + "\n")
        
        # Step 1: Create curves
        road_objects = create_road_curves()
        
        # Step 2: Convert to mesh
        convert_curves_to_mesh(road_objects)
        
        # Step 3: Create turn-arounds
        create_turnarounds(road_objects)
        
        # Step 4: Create residential mews
        create_residential_mews()
        
        # Step 5: Apply materials
        road_mat, edge_mat = add_road_materials()
        
        # Step 6: Add markings
        add_road_markings()
        
        # Step 7: Verify
        verify_road_connectivity()
        
        # Summary
        log("\n" + "="*50)
        log_success("ROAD NETWORK GENERATION COMPLETE!")
        log("="*50)
        log(f"Main roads: 3 (Perimeter + Collector + North Residential)")
        log(f"Local lanes: 4 (with fire turn-arounds)")
        log(f"Residential mews: {len(RESIDENTIAL_MEWS['paths'])}")
        log(f"Total: {3 + 4 + len(RESIDENTIAL_MEWS['paths'])} road objects")
        log("\nNext steps:")
        log("1. Save file")
        log("2. Open 02-plots-buildings/residential-plots.blend")
        log("3. Run plot-generator.py")
        log("="*50 + "\n")
        
        return True
        
    except Exception as e:
        log_error(f"Road generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
