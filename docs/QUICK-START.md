# QUICK START GUIDE — Evren Village Blender

**⏱️ 10 minutes to your first render**

---

## 1️⃣ INSTALL & OPEN

### Download Blender (if needed)
```bash
# macOS / Linux / Windows
Visit: https://www.blender.org/download/
Install Blender 4.0+
```

### Clone This Repository
```bash
git clone https://github.com/evrenkrf-design/evren-village-blender.git
cd evren-village-blender
```

### Open Base Project
```bash
blender 00-base-plan/evren-masterplan-base.blend
```

---

## 2️⃣ UNDERSTAND THE SCENE

When you open the file, you'll see:

```
Scene Hierarchy (Outliner panel - top right):
├── Master Plan
│   ├── Terrain (heightmap placeholder)
│   ├── Roads (curve-based)
│   ├── Zones (zone boundaries)
│   ├── Water Systems (collection)
│   └── Grid Reference (measurement overlay)
├── Camera (default view)
├── Lighting (3-point setup)
└── World (HDRI environment)
```

**Shortcut to explore:**
- **Home Key** or **Numpad .** → Frame all objects
- **Mouse Wheel** → Zoom
- **Middle Mouse + Drag** → Rotate view
- **Shift + Middle Mouse** → Pan view

---

## 3️⃣ RUN YOUR FIRST SCRIPT

### Open Scripting Workspace
```
Top menu: Scripting (or Shift+F12)
```

### Load the Setup Script
```
Text Editor → Open Text File → scripts/setup.py
Click "Run Script" (Alt+P)
```

**What it does:**
- ✅ Imports all curve data
- ✅ Generates basic terrain
- ✅ Creates road network from SVG coordinates
- ✅ Sets up zone boundaries
- ✅ Configures materials

**Output in System Console (if Blender runs headless):**
```
[Evren Setup] ✓ Terrain created
[Evren Setup] ✓ Roads imported (6 paths)
[Evren Setup] ✓ Zones defined (4 regions)
[Evren Setup] ✓ Materials loaded
[Evren Setup] Complete! Scene ready.
```

---

## 4️⃣ FIRST RENDER (30 seconds)

### Render Settings (Already Preset)
```
Top menu: Render → Render Image (F12)
or Ctrl+F12 to render in new window
```

**Current render settings:**
- Engine: **Eevee** (fast, real-time preview)
- Resolution: **1920×1080** (HD)
- Samples: **64** (quick)
- Expected time: **15-30 seconds**

### What you'll see:
- Aerial view of terrain with zone colors
- Road network visible
- Basic lighting setup
- Placeholder objects for buildings/facilities

---

## 5️⃣ NAVIGATE THE PROJECT

### File Structure You'll Use Most:

```
01-terrain-roads/
└── terrain-heightmap.blend          ← Terrain + road curves

02-plots-buildings/
├── residential-plots.blend          ← H/M/L/V plot templates
└── building-types/
    ├── small-house.blend
    ├── medium-house.blend
    ├── large-house.blend
    └── villa.blend

03-aura-centre/
└── aura-complete.blend              ← Banyan tree + central space

04-facilities/
└── facilities-master.blend          ← Hospital, school, market, etc.

08-materials-lighting/
├── materials-library.blend          ← All textures & shaders
└── lighting-rigs/
    ├── day-cycle.blend              ← Sun + sky animation
    └── night-pathways.blend         ← Night lighting setup
```

---

## 6️⃣ COMMON FIRST TASKS

### ✏️ Task 1: Change View Angle
```
In 3D Viewport:
Numpad 7 → Top view (aerial plan)
Numpad 1 → Front view
Numpad 3 → Side view
Numpad 0 → Camera view (what renders)

Scroll wheel or Numpad + / - → Zoom
```

### ✏️ Task 2: Change Render Engine
```
Properties panel (right side) → Render Properties
Engine dropdown:
  • Eevee (fast preview)
  • Cycles (photorealistic, slower)
```

### ✏️ Task 3: Import a Building
```
File → Link (Link existing object without embedding)
Navigate to: 02-plots-buildings/small-house.blend
Select collection → Link
Place in viewport
```

### ✏️ Task 4: Add a Light
```
Shift+A → Light → Sun / Point / Spot
Move in viewport: G key + drag
Rotate: R key + axis (X/Y/Z)
Scale: S key + number
```

### ✏️ Task 5: Add Terrain Detail
```
Open: 01-terrain-roads/terrain-heightmap.blend
Subdivide terrain mesh (right-click → Subdivide)
Add noise texture (Shader Editor → Noise Texture)
See rendered preview (Z → Rendered)
```

---

## 7️⃣ UNDERSTANDING PYTHON SCRIPTS

### Available Scripts:

```
scripts/
├── setup.py                    ← Run this first (1 time)
├── utils.py                    ← Helper functions (always loaded)
├── road-generation.py          ← Generate organic curves
├── plot-generator.py           ← Create 50 residential plots
├── procedural-trees.py         ← Generate vegetation
└── render-queue.py             ← Batch render automation
```

### How to Run a Script:

**Method 1: Inside Blender**
```
Scripting workspace → Open script → Run (Alt+P)
```

**Method 2: Terminal (Headless)**
```bash
blender --background evren-masterplan-base.blend --python scripts/setup.py
```

**Method 3: Batch Render**
```bash
chmod +x scripts/batch-render.sh
./scripts/batch-render.sh
```

---

## 8️⃣ KEYBOARD SHORTCUTS (ESSENTIAL)

| Action | Shortcut |
|--------|----------|
| **Render Image** | `F12` |
| **Render Animation** | `Ctrl+F12` |
| **Toggle Rendered View** | `Z` → Rendered |
| **Wireframe Toggle** | `Z` → Wireframe |
| **Hide/Show Object** | `H` |
| **Select All** | `A` |
| **Deselect All** | `Alt+A` |
| **Delete** | `X` → Delete |
| **Duplicate** | `Shift+D` |
| **Move** | `G` |
| **Rotate** | `R` |
| **Scale** | `S` |
| **Undo** | `Ctrl+Z` |
| **Redo** | `Ctrl+Shift+Z` |
| **Open File** | `Ctrl+O` |
| **Save File** | `Ctrl+S` |

---

## 9️⃣ NEXT STEPS (AFTER QUICK START)

### Week 1: Learn the Terrain
```
1. Open 01-terrain-roads/terrain-heightmap.blend
2. Follow: docs/BLENDER-SETUP.md
3. Run: scripts/road-generation.py
4. Explore organic curve modifiers
```

### Week 2: Build Residential Zones
```
1. Open 02-plots-buildings/residential-plots.blend
2. Run: scripts/plot-generator.py
3. Assign building types (H/M/L/V)
4. Add variations per plot
```

### Week 3: Central Aura Space
```
1. Open 03-aura-centre/aura-complete.blend
2. Study procedural tree generation
3. Customize Banyan dimensions
4. Place community nodes
```

### Week 4: Add Facilities & Systems
```
1. Link facility models from 04-facilities/
2. Integrate water system (05-water-systems/)
3. Add waste collection routes (06-waste-systems/)
4. Test circulation paths
```

### Week 5-6: Materials & Rendering
```
1. Open 08-materials-lighting/materials-library.blend
2. Apply textures to all surfaces
3. Setup lighting rigs (day/night/monsoon)
4. Configure Cycles render settings
```

### Week 7-8: Animation & Export
```
1. Open 09-animation-camera/camera-master.blend
2. Create camera paths (drone, ground level)
3. Setup keyframe animation
4. Batch render to 4K sequence
5. Export FBX for game engines
```

---

## 🚨 TROUBLESHOOTING

### ❌ "Script won't run"
```bash
# Check Python paths
blender --python-console
# Should show: Python 3.10+
# If error, reinstall Blender completely
```

### ❌ "Scene is too slow to navigate"
```
Viewport shading (top right):
- Switch to "Wireframe" mode (Z → Wireframe)
- Hide heavy objects (H key)
- Reduce subdivision levels (Modifier panel)
```

### ❌ "Objects not rendering"
```
Check:
1. Is object on visible layer? (Eye icon in Outliner)
2. Is camera looking at object? (Numpad 0)
3. Is render engine set correctly? (Eevee vs Cycles)
4. Does material have emission? (Shader Editor)
```

### ❌ "Can't see textures"
```
Viewport Shading (Z key):
- Click "Rendered" or "Material Preview"
- Not "Solid" or "Wireframe"
```

### ❌ "File won't save"
```bash
# Check disk space
df -h

# Check folder permissions
chmod 755 ./

# Save to different location temporarily
File → Save As → /tmp/test.blend
```

---

## 📞 NEED HELP?

- 📖 Full Docs: [`docs/WORKFLOW.md`](../docs/WORKFLOW.md)
- 🐛 Issues: [GitHub Issues](https://github.com/evrenkrf-design/evren-village-blender/issues)
- 💬 Questions: [GitHub Discussions](https://github.com/evrenkrf-design/evren-village-blender/discussions)
- 📧 Email: design@evrenvillage.org

---

## ✅ CHECKLIST: First Session

- [ ] Blender 4.0+ installed
- [ ] Repository cloned locally
- [ ] Base file opened (`00-base-plan/evren-masterplan-base.blend`)
- [ ] First render completed (F12)
- [ ] Setup script ran successfully
- [ ] Navigation shortcuts practiced
- [ ] One building type explored

**If all ✅, you're ready for Phase 1!** 🎉

---

**Estimated time to complete this guide: 10-15 minutes**

**Next: Open `docs/BLENDER-SETUP.md` for environment configuration**

