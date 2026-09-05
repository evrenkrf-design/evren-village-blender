# BLENDER ENVIRONMENT SETUP

## Prerequisites

- **Blender 4.0+** (https://www.blender.org/download/)
- **Python 3.10+** (included with Blender)
- **8GB+ RAM** (16GB+ recommended)
- **GPU** (NVIDIA CUDA, AMD HIP, or Intel oneAPI preferred)
- **20GB free disk space** (for complete project + renders)

---

## INSTALLATION

### 1. Install Blender

**macOS:**
```bash
brew install blender
# or download from blender.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install blender
```

**Windows:**
Download installer from https://www.blender.org/download/ and run.

### 2. Verify Installation

```bash
blender --version
# Should output: Blender 4.x.x

blender --python-console
# Should show Python 3.10+ available
```

---

## PYTHON SETUP

### Install Dependencies

```bash
cd evren-village-blender/scripts
pip install -r requirements.txt
```

**Contents of requirements.txt:**
```
numpy>=1.21
scipy>=1.7
Pillow>=8.0
svg.path>=4.0
jsonschema>=4.0
```

### Verify Python in Blender

```
Blender Menu → Scripting
Script Editor → Open Console (not text editor)
Type: import numpy
If no error, numpy is available
```

---

## GPU ACCELERATION SETUP

### NVIDIA CUDA (Recommended)

**1. Install CUDA Toolkit**
```bash
# macOS: Not officially supported by NVIDIA, use Metal instead
# Linux:
sudo apt install cuda-toolkit

# Windows:
Download from https://developer.nvidia.com/cuda-downloads
```

**2. Enable in Blender**
```
Preferences → System → Cycles Render Devices
Select: CUDA
Check "GeForce GTX 1080" (or your GPU)
Close preferences
```

**3. Verify CUDA Works**
```
Open any .blend file
Set Render Engine: Cycles
Properties → Render → Device: GPU Compute
Press F12 to render - should be much faster
```

### AMD HIP

```
Preferences → System → Cycles Render Devices
Select: HIP (not CUDA)
Check your AMD GPU
```

### macOS Metal

```
Blender 3.3+ has native Metal support
Preferences → System → Cycles Render Devices
Select: Metal
All compatible GPUs listed
```

### Intel oneAPI

```
Preferences → System → Cycles Render Devices
Select: oneAPI
Check Intel GPU / Arc GPU
```

---

## ADD-ONS & PLUGINS

### Essential Add-ons (Built-in)

Enable in **Preferences → Add-ons**:

- ✅ **Import-Export: FBX Format** (for game engines)
- ✅ **Import-Export: glTF 2.0 Format** (WebGL export)
- ✅ **Import-Export: SVG as Curve** (for plan import)
- ✅ **Add Curve: Bézier Curve IK** (for roads)
- ✅ **UV: Unwrap** (texturing tools)
- ✅ **Modifier Tools** (mesh operations)

### Recommended Third-Party Add-ons

**1. BAT (Blender Asset Tracer)**
```bash
# For managing linked assets
# Download: https://github.com/fsiddi/BAT
# Extract to: ~/.config/blender/4.0/scripts/addons/
```

**2. Scatter Object (Optional - for vegetation)
```
Third-party (paid/free versions)
BlenderMarket: https://blendermarket.com/products/scatter
```

**3. GeometryNodes Support**
```
# Built-in to Blender 3.0+
# Already available - no install needed
Modifiers → Add Modifier → Geometry Nodes
```

### Enable Add-ons

```
1. Blender → Preferences (Ctrl+,)
2. Add-ons panel (left sidebar)
3. Search for add-on name
4. Click checkbox to enable
5. Close preferences
```

---

## PROJECT FOLDER STRUCTURE

Create these directories locally:

```bash
cd evren-village-blender

# Create output folders
mkdir -p renders/stills
mkdir -p renders/sequences
mkdir -p renders/exports

# Create cache folders (auto-generated but good to have ready)
mkdir -p .cache/renders
mkdir -p .cache/temp

# Verify structure
tree -L 2 --dirsfirst
```

---

## PREFERENCES OPTIMIZATION

### For Rendering Performance

```
Preferences → Performance

✓ Enable CUDA / HIP / Metal / oneAPI
✓ Multithreading: Enabled
✓ Auto Save: Every 5 minutes
✓ Undo Steps: 32 (balance speed/memory)
```

### For Navigation (Smooth Viewport)

```
Preferences → Viewport

✓ Smooth Scroll: Enabled
✓ Smooth Pan: Enabled
✓ Invert Zoom Direction: Your preference
✓ Auto Depth: Enabled
```

### For File Management

```
Preferences → File Paths

Set these to your project:
- Temporary Files: ./evren-village-blender/.cache/temp
- Render Output: ./evren-village-blender/renders/
- Script Directories: ./evren-village-blender/scripts/
```

### Memory Settings

```
Preferences → System

- Undo Memory Limit: 256 MB (or higher if you have RAM)
- VBOs: Enabled (for faster viewport)
- Texture Size Limit: 8192 (if GPU has enough VRAM)
```

---

## THEME & WORKSPACE SETUP

### Recommended Theme

```
Preferences → Themes

Choose: Blender Light (easier on eyes during long sessions)
or: Blender Dark (easier for rendering previews)
```

### Default Workspace Layout

We've configured workspaces in the .blend files:
- **Layout**: Default for modeling
- **Modeling**: For detailed work
- **Shading**: For materials & textures
- **Sculpting**: For terrain refinement
- **UV Editing**: For texture mapping
- **Rendering**: Pre-configured render settings
- **Compositing**: Post-processing (for final quality)
- **Scripting**: For Python automation

---

## STARTUP FILE

Optional: Create a custom startup file with preferred settings.

```bash
# Create startup template
cp 00-base-plan/evren-masterplan-base.blend \
   ~/.config/blender/4.0/startup.blend

# Every new project will start with this setup
```

---

## TESTING YOUR SETUP

### Step 1: Open Base File
```bash
blender 00-base-plan/evren-masterplan-base.blend
```

### Step 2: Check Scene
- Top-right corner should show: **Blender 4.x**
- Properties panel should show render engine options
- Outliner should show scene hierarchy

### Step 3: Test Render
```
Press F12 to render
Should see viewport render in ~30 seconds
(Using Eevee engine - fast preview)
```

### Step 4: Test GPU
```
Properties → Render → Device: GPU Compute
Press F12 again
Should render 2-3x faster if GPU is working
```

### Step 5: Test Python Script
```
Scripting workspace → Open scripts/utils.py
Press Alt+P to run
Check System Console for output messages
```

---

## TROUBLESHOOTING

### Problem: "CUDA not available"
```
Solution:
1. Check NVIDIA GPU: nvidia-smi (Linux/Mac) or Device Manager (Windows)
2. Install CUDA Toolkit matching GPU & driver
3. Restart Blender
4. Preferences → System → Cycles Render Devices should show GPU
```

### Problem: "Scene too slow in viewport"
```
Solution:
1. Reduce subdivision levels (Modifier panel)
2. Switch viewport shading: Z → Wireframe
3. Hide heavy objects: Select → H (hide)
4. Lower viewport resolution: Viewport → Resolution Scale 50%
```

### Problem: "Out of memory"
```
Solution:
1. Increase swap space:
   - Linux: fallocate -l 16G /swapfile
   - macOS: automatic
   - Windows: Virtual Memory settings
2. Reduce scene resolution temporarily
3. Clear undo history: Edit → Undo History → Clear
```

### Problem: "Python modules not found"
```
Solution:
1. Install globally: pip install numpy
2. Or install in Blender:
   Preferences → Python Packages → Install Package
   Type: numpy (or module name)
```

---

## FINAL CHECKLIST

- [ ] Blender 4.0+ installed
- [ ] Python 3.10+ verified
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] GPU acceleration enabled
- [ ] Key add-ons enabled
- [ ] Project folders created
- [ ] Preferences optimized
- [ ] Base file opens without errors
- [ ] F12 render works
- [ ] Python scripts run

**All checked? You're ready for production!** ✅

---

**Next Step:** Read `docs/QUICK-START.md` to begin your first project.
