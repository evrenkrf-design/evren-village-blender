# PRODUCTION WORKFLOW — Evren Village 3D Blender

**8-Week Timeline • Phase-based development • Incremental complexity**

---

## OVERVIEW

This document outlines the complete production pipeline from empty scene to final 4K renders and interactive exports.

### Timeline
```
Week 1 → Terrain & Roads
Week 2 → Residential Plots & Buildings
Week 3 → Aura Centre & Community Spaces
Week 4 → Facilities & Services
Week 5 → Water & Waste Systems
Week 6 → Vegetation & Materials
Week 7 → Lighting & Atmosphere
Week 8 → Animation & Final Renders
```

### Key Milestones
- **End Week 1**: Navigable terrain with road network
- **End Week 2**: All 50 residential plots with building templates
- **End Week 3**: Central Aura space with community nodes
- **End Week 4**: All facilities positioned and basic models in place
- **End Week 5**: Water & waste systems simulated and visible
- **End Week 6**: Full landscape with seasonal variations
- **End Week 7**: Multiple lighting scenarios (day/night/monsoon)
- **End Week 8**: 4K renders + interactive exports + video sequences

---

## PHASE 1: TERRAIN & ROADS (Week 1)

### Objectives
✅ Import master plan from SVG  
✅ Generate organic terrain with elevation  
✅ Create smooth road network with traffic calming  
✅ Define zone boundaries  
✅ Setup reference grids  

### Files & Scripts
```
00-base-plan/evren-masterplan-base.blend    ← Start here
scripts/setup.py                             ← Run first (initialization)
01-terrain-roads/terrain-heightmap.blend    ← Work file
scripts/road-generation.py                   ← Procedural roads
```

### Daily Breakdown

**Monday: SVG Import & Terrain Base**
```bash
1. Open 00-base-plan/evren-masterplan-base.blend
2. Scripting → Open scripts/setup.py → Run (Alt+P)
3. Verify: Terrain plane, 4 zones, Aura centre, camera, lighting
4. Save file
```

**Tuesday: Terrain Elevation & Heightmap**
```bash
1. Open 01-terrain-roads/terrain-heightmap.blend
2. Add Displace modifier to terrain
3. Create grayscale heightmap (Photoshop/GIMP):
   - White = high elevation
   - Black = low elevation
   - Gray = neutral
4. Apply heightmap texture to terrain mesh
5. Adjust scaling for realistic slopes (max 15° for walkability)
```

**Wednesday-Thursday: Road Network Generation**
```bash
1. Study SVG coordinates (reference file)
2. Open scripts/road-generation.py
3. Understand Bézier curve system
4. Generate 6 road paths:
   - Perimeter loop (main circulation)
   - Main collector (E-W)
   - North residential collector
   - 4 local lanes with turn-arounds
5. Test script: Blender → Scripting → Open road-generation.py → Run
6. Verify: Roads appear as curves in viewport
```

**Friday: Road Details & Refinement**
```bash
1. Convert curves to mesh (road surfaces)
2. Add shoulders and edge details (modifiers)
3. Create road markings (white centre line)
4. Add intersection markers and roundabouts
5. Testing: Drive camera along roads (smooth flow)
6. Save and backup
```

### Expected Output
- Terrain heightmap with realistic slopes
- 6 road paths with Bézier smoothing
- Zone color coding visible from above
- Aura centre marked at 600m radius
- Camera positioned for aerial view

### Success Criteria
✅ Terrain loads without artifacts  
✅ Roads are smooth organic curves  
✅ Zones are clearly demarcated  
✅ Camera view shows entire village  
✅ Scene renders in <1 minute (Eevee)  

---

## PHASE 2: RESIDENTIAL PLOTS & BUILDINGS (Week 2)

### Objectives
✅ Generate all 50 plots with variations  
✅ Create building templates (H/M/L/V types)  
✅ Assign building to random plots  
✅ Add architectural details (doors, windows, roofs)  
✅ Setup material variations  

### Files & Scripts
```
02-plots-buildings/residential-plots.blend  ← Main work file
scripts/plot-generator.py                    ← Procedural plot creation
building-types/small-house.blend             ← Template models
building-types/medium-house.blend
building-types/large-house.blend
building-types/villa.blend
```

### Daily Breakdown

**Monday: Plot Generation Script**
```bash
1. Open 02-plots-buildings/residential-plots.blend
2. Load plot-coordinates.json data
3. Run scripts/plot-generator.py
4. Verify: 50 rectangular plots appear in correct zones
   H plots (25): 8m × 5m
   M plots (10): 10m × 7m
   L plots (10): 12m × 12m
   V plots (5): 15m × 14m
5. Each plot should have unique ID (H01, M01, etc.)
```

**Tuesday-Wednesday: Building Templates**
```bash
1. Open building-types/small-house.blend
2. Model basic house (low-poly, optimized):
   - Simple rectangular footprint
   - Pitched roof (45° angle)
   - Door on front
   - 2-3 windows per side
   - Basic landscaping (small garden, fence)
3. Repeat for M, L, V types (increasing detail)
4. Create material presets:
   - Exterior walls (stucco, painted)
   - Roof tiles (red/brown/grey)
   - Wood/metal trim
   - Glass windows
5. Save each as template
```

**Thursday: Plot-to-Building Assignment**
```bash
1. Run assignment script:
   - Randomly place building types across plots
   - Ensure 70% H, 20% M, 7% L, 3% V distribution
   - Vary orientation (±5° rotation per plot)
2. Add setback details:
   - Front setback: 2-4m (based on plot size)
   - Side setback: 1-2m
   - Add small front fences/gates
3. Visual check: Fly camera through zones
```

**Friday: Materials & Variations**
```bash
1. Create color variation system:
   - 5 exterior color options per building type
   - Random assignment (weighted)
2. Add roof variations (3-4 colors)
3. Add landscaping variety:
   - Front gardens (different plant density)
   - Back courtyards (fenced areas)
4. Add small details:
   - Clotheslines
   - Potted plants
   - Parked bikes/scooters
5. Final render test
```

### Expected Output
- 50 placed residential plots with unique IDs
- 50 buildings (distributed H/M/L/V)
- Varied architectural styles and colors
- Setbacks and boundary fencing
- Small landscaping details

### Success Criteria
✅ All 50 plots have buildings  
✅ No overlapping structures  
✅ Buildings fit within plot boundaries  
✅ Visible variation in colors/styles  
✅ Scene renders in <2 minutes (Cycles/256s)  

---

## PHASE 3: AURA CENTRE & COMMUNITY SPACES (Week 3)

### Objectives
✅ Model Great Banyan tree (procedural)  
✅ Create walking & cycling paths  
✅ Build 4 community plaza nodes  
✅ Add street furniture (seating, lighting, water features)  
✅ Design green buffer zones  

### Files & Scripts
```
03-aura-centre/aura-complete.blend          ← Main work file
scripts/procedural-trees.py                  ← Banyan tree generation
walking-paths.blend
cycling-tracks.blend
community-nodes/quiet-garden.blend
community-nodes/arrival-plaza.blend
community-nodes/market-plaza.blend
community-nodes/activity-plaza.blend
```

### Key Details

**Banyan Tree (Great Banyan)**
- Trunk diameter: 5-8m
- Canopy spread: 30-40m
- Height: 20-25m
- Aerial roots (curved branches going down)
- Understory vegetation

**Aura Paths**
- Pedestrian walking path: 2.5m wide
- Cycle track: 3m wide
- Permeable paving (light colored)
- Green buffer: 0.5m on each side
- 8km total length

**4 Community Nodes**
1. **Quiet Garden** (NW): Meeting space, shade, seating
2. **Arrival Plaza** (W): Parking entry, orientation signage
3. **Market Plaza** (E): Chai tapri, market stalls, gathering
4. **Activity Plaza** (S): School connection, playground interface

Each node includes:
- Seating clusters (benches/steps)
- Shade structures (trees/pergolas)
- Drinking water station
- Solar pathway lighting
- Accessible design (step-free)

### Expected Output
- Detailed Banyan tree model
- 8km walking/cycling network with proper width
- 4 furnished community plazas
- Lighting infrastructure
- Vegetated buffer zones

### Success Criteria
✅ Banyan tree is recognizable and anatomically correct  
✅ Paths are smooth and properly scaled  
✅ 4 plazas have distinct character  
✅ All plazas have furniture/amenities  
✅ Scene renders in <3 minutes (Cycles)  

---

## PHASE 4: FACILITIES & SERVICES (Week 4)

### Objectives
✅ Model all 10+ facility buildings  
✅ Create parking areas with lane markings  
✅ Add vehicle circulation paths  
✅ Model infrastructure blocks  
✅ Setup service access routes  

### Facilities to Model
```
1. Hospital (2,500 m²) - Haven SW
2. School (3,000 m²) - Haven SW
3. Petrol Pump (500 m²) - West Entry
4. Market (1,200 m²) - East
5. Chai Tapri (300 m²) - East
6. Parking Area (2,000 m²) - West
7. Playground (1,500 m²) - Haven SW
8. Stable (800 m²) - Zenith SE
9. Farmhouse (1,000 m²) - Zenith SE
10. Infrastructure/Utility (600 m²) - South
11. Waste Service (400 m²) - South
```

### Each Facility Model Includes
- Building footprint
- Roof structure (pitched/flat)
- Windows & doors
- Entrance areas
- Parking spaces (marked)
- Service gates
- Outdoor areas (courtyards, gardens)
- Landscaping

### Expected Output
- 11 facility buildings with architectural detail
- 80+ parking spaces (P1 area)
- Service road network
- Hospital ambulance bay
- School drop-off area
- Market stall layout
- Waste service routes

### Success Criteria
✅ All facilities positioned correctly  
✅ Vehicle circulation is logical  
✅ Parking is clearly marked  
✅ Service areas are segregated  
✅ Scene still renders in acceptable time  

---

## PHASE 5: WATER & WASTE SYSTEMS (Week 5)

### Objectives
✅ Model bioswales and rain gardens  
✅ Create roof rainwater harvesting points  
✅ Simulate greywater reuse paths  
✅ Model recharge pits  
✅ Create waste collection points (3-bin system)  
✅ Visualize biomedical waste route  

### Water Features
- **Bioswales**: Vegetated drainage channels (8 locations)
- **Rain Gardens**: Planted depressions (3 major sites)
- **Recharge Pits**: Circular infiltration features
- **Harvesting Points**: Marked at facility roofs
- **Greywater Route**: Animated flow visualization
- **Filtration Buffer**: 15m perimeter zone (north)

### Waste Points
- **3-Bin Collection Points**: 5 per zone (20 total)
  - Green: Organic/compost
  - Yellow: Recyclables
  - Gray: Residual
- **Material Recovery Area**: Infrastructure block
- **Biomedical Route**: Hospital to authorized facility
- **Compost Center**: Waste service area

### Visualizations
- Water flow direction (arrows/curves)
- Waste collection schedule (animated markers)
- Seasonal variations (wet season emphasis)
- Animation simulation (flowing water)

### Expected Output
- Detailed water management infrastructure
- 3-bin waste collection visible at all zones
- Flow paths animated and color-coded
- Sustainable systems clearly communicable
- Educational overlay possible

### Success Criteria
✅ All water features modeled and positioned  
✅ Waste collection points complete  
✅ Flow visualizations are clear  
✅ Systems are independently toggleable  
✅ Supports educational animation  

---

## PHASE 6: VEGETATION & MATERIALS (Week 6)

### Objectives
✅ Create tree library (procedural generation)  
✅ Populate vegetation across village  
✅ Apply realistic materials to all surfaces  
✅ Create seasonal variations  
✅ Add atmospheric effects  

### Vegetation Elements
- **Trees**: 500+ instances, 10 species
- **Understory Shrubs**: Random placement
- **Ground Cover**: Grass, mulch, permeable paving
- **Rooftop Gardens**: Green roofs on some buildings
- **Orchards**: West farms area with fruit trees
- **Seasonal Colors**: Dry/monsoon/winter variants

### Material Types
1. **Paving**: Permeable pavers, brick, natural stone
2. **Walls**: Stucco, painted brick, stone cladding
3. **Roofs**: Tile (red/brown/grey), metal sheets, green
4. **Water**: Caustics, ripples, flow visualization
5. **Natural**: Rock, earth, mulch, grass
6. **Vegetation**: Leaf color variations, wind animation

### Shader Library
```
08-materials-lighting/materials-library.blend
├── Permeable Paver (PBR textures)
├── Stucco Wall (with color variations)
├── Tile Roof (weathered options)
├── Natural Stone
├── Wood & Metal
├── Water (animated)
├── Vegetation (seasonal)
└── Asphalt/Concrete
```

### Seasonal Variations
1. **Dry Season**: Dust, tan grass, less foliage
2. **Monsoon**: Lush green, water features active
3. **Winter**: Leafless deciduous trees, dry state
4. **Year-Round**: Evergreen elements (coconut palms, etc.)

### Expected Output
- Photorealistic material library
- 500+ trees with variation
- Seasonal scene variations
- Wind-animated vegetation
- Detailed surface textures

### Success Criteria
✅ All materials are PBR compliant  
✅ Texture resolution 4K minimum  
✅ Vegetation population is dense but performant  
✅ Seasonal variants are distinct  
✅ Scene supports multiple render passes  

---

## PHASE 7: LIGHTING & ATMOSPHERE (Week 7)

### Objectives
✅ Setup sun position tracking (time-of-day animation)  
✅ Create multiple lighting scenarios  
✅ Add atmospheric effects (fog, haze, particles)  
✅ Configure post-processing nodes  
✅ Test different camera paths  

### Lighting Scenarios
1. **Golden Hour (Sunrise/Sunset)**
   - Low sun angle (15-30°)
   - Warm color temperature (3000K)
   - Long shadows, dramatic lighting
   - Clear sky with orange/pink hues

2. **Bright Noon**
   - High sun angle (70-80°)
   - Cool color temperature (6500K)
   - Short shadows, even lighting
   - Clear blue sky

3. **Blue Hour (Dusk/Dawn)**
   - Sun below horizon
   - Cool blue sky (5000K)
   - Artificial lights beginning to show
   - Long silhouettes

4. **Night**
   - No direct sunlight
   - Artificial pathway lighting active
   - Building lights warm (2700K)
   - Dark blue sky with stars

5. **Monsoon Overcast**
   - Diffuse grey sky
   - No distinct shadows
   - Cooler color temperature
   - Potential rain particle effects

### HDRI Lighting
- Use high-resolution HDRI maps (4K+)
- Different environment maps per time-of-day
- Seasonal sky variations
- Realistic light falloff and bounce

### Atmospheric Effects
- **Volumetric Fog**: Morning/evening mist
- **Dust Particles**: Afternoon sunbeams
- **Rain Particles**: Monsoon scenes
- **Cloud Shadows**: Moving shadow patterns
- **Bloom/Glow**: Lights at night

### Expected Output
- 5+ distinct lighting scenarios
- Smooth time-of-day animation (24-hour cycle)
- Atmospheric depth and mood
- Post-processing ready (color grading, exposure)
- Multiple HDRI environments

### Success Criteria
✅ Each lighting scenario is distinct  
✅ Transitions are smooth (no popping)  
✅ Night lighting is photorealistic  
✅ Atmospheric effects enhance mood  
✅ Performance remains acceptable  

---

## PHASE 8: ANIMATION & FINAL RENDERS (Week 8)

### Objectives
✅ Create camera flight paths  
✅ Setup animation keyframes  
✅ Configure batch render settings  
✅ Export to multiple formats (FBX, glTF, MP4)  
✅ Generate 4K final renders  

### Camera Sequences
1. **Drone Approach** (60 sec)
   - Start: High altitude, approaching from North
   - Path: Spiraling descent
   - End: Hover above Aura centre

2. **Ground Level Walkthrough** (120 sec)
   - Start: Arrival plaza (visitor POV)
   - Path: Through zones, past facilities
   - End: Aura centre from ground level

3. **Aura Tour** (90 sec)
   - Circling Banyan tree at various heights
   - Close-up of community nodes
   - Details of paths and features

4. **Zone Showcase** (30 sec per zone)
   - Individual zone highlights
   - Showcase residential character
   - Show facility integration

5. **Day Cycle Animation** (60 sec)
   - Static camera position
   - 24-hour lighting cycle
   - Shows seasonal changes

### Render Queue
```
Sequence 1: Drone Approach
  - 24 fps × 60 sec = 1,440 frames
  - Resolution: 3840×2160 (4K)
  - Engine: Cycles, 512 samples
  - Estimated time: 24-48 hours
  - Format: PNG sequence + ProRes MOV

Sequence 2: Ground Walkthrough
  - 24 fps × 120 sec = 2,880 frames
  - Resolution: 3840×2160
  - Time: 48-96 hours

Sequence 3: Aura Tour
  - 24 fps × 90 sec = 2,160 frames
  - Time: 36-72 hours

Still Renders:
  - 20× hero shots (4K)
  - Multiple angles, times of day
  - Time: 2-4 hours
```

### Export Formats

**1. Video (Cinema Delivery)**
- ProRes 422 HQ (.mov) - color grading pipeline
- H.264 MP4 - web distribution
- 4K UHD (3840×2160)
- 24fps (cinema standard)

**2. Interactive (Game Engines)**
- FBX (.fbx) - Unreal Engine 5
- glTF 2.0 (.glb) - WebGL viewer
- Textured models with materials
- Optimized polygon count

**3. Still Images**
- PNG 16-bit (lossless for post-production)
- JPEG (web distribution)
- 4K resolution
- Color-managed output

**4. Sequences**
- OpenEXR (.exr) for VFX compositing
- Multi-pass rendering (diffuse, normal, depth, etc.)
- Linear color space

### Expected Output
- 3 video sequences (total 5+ minutes)
- 20+ hero still images
- Interactive 3D model (game-ready)
- Web viewer version
- VFX-ready sequences

### Success Criteria
✅ All animations smooth at 24fps  
✅ 4K renders are artifact-free  
✅ Color grading consistent  
✅ Audio/music ready (if included)  
✅ Multiple format exports successful  
✅ Interactive model performs well (<60fps)  

---

## QUALITY GATES

At end of each phase, verify:

```
□ No broken/overlapping geometry
□ All objects properly named and organized
□ Materials assigned (no missing shaders)
□ Scene renders without errors
□ File size reasonable (<2GB)
□ Backup created
□ Performance metrics acceptable
```

---

## PERFORMANCE TARGETS

| Phase | Geometry | Polygons | Render Time | Viewport FPS |
|-------|----------|----------|-------------|---------------|
| 1 | Terrain + Roads | 500K | <1 min | 30+ |
| 2 | + Buildings | 5M | 1-2 min | 15+ |
| 3 | + Aura Centre | 8M | 2-3 min | 12+ |
| 4 | + Facilities | 15M | 3-4 min | 10+ |
| 5 | + Water/Waste | 18M | 4-5 min | 8+ |
| 6 | + Vegetation | 50M | 5-10 min | 5+ |
| 7 | + Lighting | 50M | 8-12 min | 5+ |
| 8 | Final Scene | 100M+ | 10-15 min | 3+ |

*Render times with Cycles/256 samples on RTX 3080, resolution 1920×1080*

---

## NEXT: Phase 1 Execution

Ready to start? See [`PHASE-1-DETAILED.md`](PHASE-1-DETAILED.md) for day-by-day breakdown.
