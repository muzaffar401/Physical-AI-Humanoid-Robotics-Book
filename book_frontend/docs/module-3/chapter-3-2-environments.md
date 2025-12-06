---
id: chapter-3-2-environments
title: "Chapter 3.2: Building Photorealistic Environments"
sidebar_label: "3.2 Environments"
sidebar_position: 2
---

# Chapter 3.2: Building Photorealistic Environments

## From Basic 3D to Movie-Quality Realism

Training a computer vision model on cartoon-like simulations creates a **reality gap**—algorithms fail when deployed to real cameras capturing texture-rich, naturally-lit environments. Isaac Sim's photorealistic rendering closes this gap with **physically-based materials (PBR)**, **ray-traced lighting**, and **USD composition** for building complex, reusable scenes.

In this chapter, you'll construct photorealistic warehouses, homes, and outdoor environments using USD primitives, import high-fidelity CAD models, and apply cinematic lighting techniques from the film industry.

---

## Learning Objectives

By the end of this chapter, you will:

- **Understand**: Explain PBR (Physically Based Rendering) and how materials interact with light realistically
- **Apply**: Create USD scenes with buildings, terrain, and props using Isaac Sim's toolset
- **Apply**: Configure HDR environment maps, area lights, and ray-traced shadows for realism
- **Create**: Import CAD models (FBX, OBJ, GLTF) and optimize for simulation performance
- **Analyze**: Balance visual quality vs. rendering performance (LODs, texture compression)

**Estimated Time**: 2.5 hours

---

## Prerequisites

- **Chapter 3.1 complete** (Isaac Sim installed, USD basics)
- **Module 2 knowledge** (world building concepts from Gazebo)
- **Basic 3D modeling familiarity** helpful (Blender, Maya) but not required

---

## What You'll Build

By the end of this chapter, you'll have:

✅ **Photorealistic warehouse** with PBR materials, proper lighting
✅ **Indoor home environment** with furniture, textures, windows
✅ **Outdoor scene** with terrain, HDR sky, shadows
✅ **USD asset library** for reusing environments across projects

---

## Physically Based Rendering (PBR) Fundamentals

### What is PBR?

**PBR** simulates how real-world materials reflect light, using **physics equations** instead of artistic guesswork.

**Key properties**:
1. **Albedo (Base Color)**: Object's color without lighting (e.g., wood is brown)
2. **Metallic**: 0 = non-metal (wood), 1 = metal (steel)
3. **Roughness**: 0 = mirror-smooth, 1 = completely matte
4. **Normal Map**: Simulates surface bumps without geometry
5. **Emissive**: Self-lit surfaces (screens, LEDs)

**Why it matters**: PBR materials look correct under any lighting—same wood texture works indoors, outdoors, day, night. Non-PBR materials look fake when lighting changes.

### PBR in Isaac Sim

Isaac Sim uses **OmniPBR** shader (NVIDIA's implementation of PBR).

**Example**: Create a metal shelf
- Albedo: Gray (#808080)
- Metallic: 1.0 (fully metal)
- Roughness: 0.3 (slight scratches)
- Result: Reflects environment, shows scratches catching light

---

## Hands-On: Building a Warehouse Environment

### Step 1: Create New Scene

1. Open Isaac Sim
2. **File** → **New**
3. You'll see empty stage with default lighting

### Step 2: Add Ground Plane

1. **Create** menu → **Physics** → **Ground Plane**
2. Ground plane appears at origin
3. **Select ground plane** in Stage panel (`/GroundPlane`)
4. In Property panel, set **Scale**: (50, 50, 1) for 50m × 50m floor

### Step 3: Apply Concrete Material

Isaac Sim includes a material library with PBR textures.

1. **Content Browser** (bottom-left) → **Materials**
2. Navigate to `http://omniverse-content-production.s3-us-west-2.amazonaws.com/Materials/Base/Concrete/`
3. Find **"Concrete_New.mdl"**
4. **Drag material onto ground plane** in viewport
5. Ground now has realistic concrete texture!

**Alternative (manual PBR)**:
1. Select ground plane
2. Property panel → **Material** tab
3. **Shader**: OmniPBR
4. Set:
   - **Albedo**: Light gray (#CCCCCC)
   - **Roughness**: 0.8 (matte concrete)
   - **Metallic**: 0.0

### Step 4: Create Warehouse Walls

**Create a wall**:
1. **Create** → **Mesh** → **Cube**
2. Rename to `Wall_North` in Stage panel
3. Set **Scale**: (40, 0.2, 4) → 40m long, 0.2m thick, 4m tall
4. Set **Position**: (0, 20, 2) → North side

**Duplicate for other walls**:
1. Right-click `Wall_North` → **Duplicate**
2. Rename to `Wall_South`
3. Position: (0, -20, 2)
4. Repeat for `Wall_East` (20, 0, 2, scale: 0.2, 40, 4) and `Wall_West` (-20, 0, 2)

**Apply material**:
1. Drag **"Concrete_Painted_White.mdl"** onto all walls

### Step 5: Add Shelving Units

Isaac Sim has pre-built warehouse props.

1. **Content Browser** → **Warehouse Assets** (if installed)
   - Path: `omniverse://localhost/NVIDIA/Assets/Isaac/2023.1/Isaac/Environments/Simple_Warehouse/Props/`
2. Drag **"SM_ShelfD_01.usd"** into viewport
3. Position: (10, 0, 0)
4. Duplicate and arrange in rows:
   - `Shelf_Row1`: (10, -5, 0), (10, 0, 0), (10, 5, 0)
   - `Shelf_Row2`: (5, -5, 0), (5, 0, 0), (5, 5, 0)

**If assets not available**, create simple shelf:
1. **Create** → **Mesh** → **Cube**
2. Scale: (0.5, 3, 2) → Thin, long shelf
3. Apply **"Wood_Walnut.mdl"** material

### Step 6: Add Lighting

**Remove default light** (too generic):
1. Stage panel → Find `/World/defaultLight`
2. Right-click → **Delete**

**Add area lights** (warehouse ceiling lights):
1. **Create** → **Light** → **Rect Light**
2. Properties:
   - **Intensity**: 50,000 (bright warehouse)
   - **Width**: 2m, **Height**: 2m
   - **Position**: (0, 0, 3.8) → Just below ceiling
   - **Rotation**: Point downward (X: -90°)
3. Duplicate for grid of lights:
   - Positions: (-10, -10, 3.8), (-10, 10, 3.8), (10, -10, 3.8), (10, 10, 3.8)

**Add ambient light** (subtle fill):
1. **Create** → **Light** → **Dome Light**
2. **Intensity**: 100 (very dim, just to fill shadows)
3. **Texture**: Choose an HDR from library (e.g., `indoor_warehouse.hdr`)

### Step 7: Add Physics

For robots to collide with walls/shelves:

1. Select all walls (hold Ctrl, click each in Stage)
2. Right-click → **Add** → **Physics** → **Collision Mesh**
3. Property panel → **Collider**: Check **"Approximation Shape"** → **"Convex Hull"** (faster than mesh)
4. Repeat for shelves

---

## Advanced Material Techniques

### Creating Custom PBR Material

**Example: Rusty metal**

1. **Create** → **Material** → **OmniPBR**
2. Rename to `Mat_RustyMetal` in Stage
3. Properties:
   - **Albedo**: Brown-orange (#8B4513)
   - **Metallic**: 0.7 (partially rusted)
   - **Roughness**: 0.9 (very rough)
   - **Normal Map**: Load texture from file (e.g., `rust_normal.png`)

**Apply to object**:
1. Drag `Mat_RustyMetal` from Stage onto object in viewport

### Using Texture Maps

PBR uses multiple texture files for realism:

- **Albedo map** (`_diffuse.png`): Base color texture
- **Normal map** (`_normal.png`): Surface bumps (purple-blue image)
- **Roughness map** (`_roughness.png`): Varying shine (grayscale)
- **AO map** (`_ao.png`): Ambient occlusion (baked shadows in crevices)

**Load textures**:
1. Select material in Property panel
2. **Albedo** → Click folder icon → Browse to `wood_diffuse.png`
3. **Normal** → Browse to `wood_normal.png`
4. **Roughness** → Browse to `wood_roughness.png`

**Where to get textures**:
- [Poly Haven](https://polyhaven.com/textures) - Free PBR textures
- [Quixel Megascans](https://quixel.com/megascans) - Film-quality textures (free with Epic account)
- [Substance Source](https://www.substance3d.com/source) - Adobe's library

---

## Lighting for Photorealism

### HDR Environment Maps

**HDRI** (High Dynamic Range Image) = 360° photo capturing all light in a scene.

**Use case**: Outdoor scenes, reflections on metal/glass.

**Add HDR sky**:
1. **Create** → **Light** → **Dome Light**
2. Property panel → **Texture** → Browse to HDR file
   - Isaac Sim includes: `sky_day.hdr`, `sky_sunset.hdr`, `sky_night.hdr`
3. **Intensity**: 1000-5000 (experiment for desired brightness)

**Effect**: Sky visible in background, realistic lighting from all directions, reflections on shiny objects.

### Three-Point Lighting (Classic Setup)

Film industry technique for pleasing illumination:

**1. Key Light** (main light):
- **Type**: Rect Light or Sphere Light
- **Position**: 45° above and to side of subject
- **Intensity**: Brightest (e.g., 30,000)

**2. Fill Light** (softens shadows):
- **Position**: Opposite side of key, lower intensity
- **Intensity**: 30% of key (e.g., 10,000)

**3. Rim/Back Light** (separates subject from background):
- **Position**: Behind and above subject
- **Intensity**: 50% of key (e.g., 15,000)

**For warehouse robot scene**:
- Key: Overhead warehouse light
- Fill: Bounce light from walls (automatic with ray tracing)
- Rim: Light near entrance/windows

### Shadows and Ray Tracing

**Enable shadows on lights**:
1. Select light
2. Property panel → **Shadow** → **Enable**
3. **Shadow Quality**: Higher = softer, more realistic (but slower)

**Ray-traced shadows** (automatic in Isaac Sim):
- Accurate soft shadows from area lights
- Contact shadows (dark creases where objects touch)
- Shadow penumbra (blurry shadow edges farther from object)

---

## Importing CAD Models

Industrial robots often come with CAD files from manufacturers (SolidWorks, Fusion 360).

### Supported Formats

Isaac Sim can import:
- **USD/USDZ** (native, best quality)
- **FBX** (from Blender, Maya, 3ds Max)
- **OBJ** (simple, widely supported)
- **GLTF/GLB** (web 3D standard)
- **STL** (3D printing, no materials)

**Does NOT directly support**:
- STEP/IGES (engineering CAD) → Convert with Blender
- URDF → Use Isaac Sim's URDF importer (Chapter 3.1)

### Importing FBX/OBJ

**Example: Import a forklift model**

1. **File** → **Import**
2. Select format: **"FBX"** or **"OBJ"**
3. Browse to file (e.g., `forklift.fbx`)
4. **Import Options**:
   - ☑️ **Import Materials**
   - ☑️ **Merge Meshes** (faster rendering)
   - ☐ **Import Animations** (if model has anims)
5. Click **Import**
6. Model appears at origin

**Post-import**:
- Scale if incorrect: Property → **Scale** (often need 0.01 for cm → m)
- Rotate: Property → **Rotation** (Y-up vs Z-up axis differences)
- Add physics: Right-click → **Physics** → **Collision Mesh**

### Optimizing Imported Models

High-poly CAD models (millions of triangles) slow simulation.

**Optimization techniques**:

1. **Decimate (reduce polygons)**:
   - Export to Blender
   - **Modifiers** → **Decimate** → Target 10,000-50,000 tris
   - Re-export as FBX

2. **Use collision proxies**:
   - Visual mesh: High detail (imported model)
   - Collision mesh: Low-poly box/cylinder approximation
   - In Isaac Sim: Separate visual and collision prims

3. **Level of Detail (LOD)**:
   - Create 3 versions: High (close), Medium (mid-distance), Low (far)
   - Isaac Sim automatically switches based on camera distance

---

## USD Composition and Reusability

### Referencing vs. Copying

**Problem**: Duplicate a robot 100 times. Designer changes robot → must update 100 copies manually.

**USD solution**: **Reference** the robot file instead of copying.

**Create reusable asset**:
1. Build robot once, save as `my_robot.usd`
2. In new scene: **Create** → **Reference**
3. Browse to `my_robot.usd`
4. Robot appears! Internally it's a *pointer* to file, not a copy

**Benefits**:
- Edit `my_robot.usd` → All 100 instances update automatically
- File size: 100 references = ~1MB, 100 copies = 100MB

### Layering for Non-Destructive Edits

**USD layers** = Photoshop layers for 3D.

**Example**:
- **Base layer**: Generic warehouse (shipped with game/sim)
- **Custom layer**: Add your company's logo, change colors
- **Don't modify original** → Changes live in separate layer

**How to**:
1. **File** → **Open** → Select `warehouse_base.usd`
2. **File** → **Open As New Layer** → Create `custom_edits.usda`
3. Modify materials, positions → Saved only in custom layer
4. To share: Send both files (base + custom layer)

---

## Hands-On: Indoor Home Environment

Let's build a robot testing home with rooms, furniture, windows.

### Step 1: Room Layout

**Floor**:
1. **Create** → **Mesh** → **Cube**
2. Scale: (10, 10, 0.1) → 10m × 10m floor, 10cm thick
3. Material: **"Wood_Parquet.mdl"** (hardwood floor)

**Walls** (4 walls, 3m tall):
1. North wall: Scale (10, 0.2, 3), Position (0, 5, 1.5)
2. South wall: Scale (10, 0.2, 3), Position (0, -5, 1.5)
3. East wall: Scale (0.2, 10, 3), Position (5, 0, 1.5)
4. West wall: Scale (0.2, 10, 3), Position (-5, 0, 1.5)
5. Material: **"Paint_White.mdl"**

### Step 2: Add Windows

**Window cutout** (fake, no glass physics):
1. In North wall, create **Cube** (window frame)
2. Scale: (1.5, 0.15, 1.2) → 1.5m wide, 1.2m tall
3. Position: (2, 5, 2) → Intersects wall
4. Material: **"Glass_Clear.mdl"**
5. Property → **Opacity**: 0.3 (semi-transparent)

**Sun light through window**:
1. **Create** → **Disk Light**
2. Position: (2, 6, 2) → Just outside window
3. Intensity: 80,000
4. Rotation: Point inward

### Step 3: Add Furniture

**Table**:
1. **Create** → **Mesh** → **Cylinder**
2. Scale: (0.6, 0.6, 0.75) → 1.2m diameter, 0.75m tall
3. Position: (0, 0, 0.75) → Center of room
4. Material: **"Wood_Oak.mdl"**

**Chair** (simplified):
1. Seat: Cube, Scale (0.4, 0.4, 0.05)
2. Back: Cube, Scale (0.4, 0.05, 0.5)
3. Group: Select both → Right-click → **Group** → Name "Chair_01"
4. Duplicate chairs around table

### Step 4: HDR Lighting

1. **Create** → **Light** → **Dome Light**
2. **Texture**: `indoor_living_room.hdr`
3. **Intensity**: 300
4. Provides ambient indoor lighting + window light simulation

---

## Performance Optimization

### Ray Tracing Quality Settings

**Toolbar** → **Rendering** → **Settings**

**For interactive editing** (faster):
- Samples Per Pixel: 1-2
- Max Bounces: 2
- Resolution: 1280×720

**For final renders/screenshots**:
- Samples Per Pixel: 8-16
- Max Bounces: 4-8
- Resolution: 1920×1080 or higher

### Physics vs. Visual Meshes

**Best practice**: Separate collision from visual geometry.

**Example**: Detailed shelf model (10,000 triangles).
- **Visual mesh**: Full detail, looks great
- **Collision mesh**: Simple boxes (50 triangles), fast physics

**Setup**:
1. Import detailed model → Rename `/Shelf_Visual`
2. Create simple cube → Name `/Shelf_Collision`
3. In Stage, make `/Shelf_Collision` a child of `/Shelf_Visual`
4. `/Shelf_Collision` → Property → **Render** → Disable (invisible)
5. `/Shelf_Visual` → No collision component
6. `/Shelf_Collision` → Add **Collision Mesh**

---

## Common Issues and Solutions

### Issue: Scene is very dark

**Cause**: Not enough lights or intensity too low.

**Fix**:
- Increase light **Intensity** values (10x-100x)
- Add **Dome Light** for ambient fill
- Check camera **Exposure** settings (Property → Camera → Exposure)

### Issue: Materials look plastic/fake

**Cause**: Missing roughness variation or normal maps.

**Fix**:
- Add **Normal Map** to simulate surface texture
- Use **Roughness Map** (not uniform value)
- Check **Metallic** value matches material type

### Issue: Reflections show black or incorrect environment

**Cause**: No environment map for reflections.

**Fix**: Add **Dome Light** with HDR texture—even if intensity is low, provides reflection data.

### Issue: Models import at wrong scale/orientation

**Cause**: Unit mismatches (cm vs. m) or axis systems (Y-up vs. Z-up).

**Fix**:
- **Scale**: Multiply by 0.01 if too big (cm → m), or 100 if too small
- **Rotation**: X: 90° to flip Y-up to Z-up (or vice versa)

---

## Key Takeaways

🎓 **PBR (Physically Based Rendering)** uses albedo, metallic, roughness, and normal maps to simulate realistic light interaction.

🎓 **Isaac Sim's OmniPBR shader** enables materials that look correct under any lighting condition.

🎓 **HDR environment maps** provide 360° lighting and realistic reflections—essential for outdoor scenes and shiny objects.

🎓 **USD referencing** creates reusable assets—edit once, update everywhere (vs. copying duplicates).

🎓 **Separate collision and visual meshes** balances visual quality with physics performance.

🎓 **Three-point lighting** (key, fill, rim) creates professional, cinematic illumination for robot testing scenarios.

---

## What's Next?

You've built photorealistic environments—now let's add **advanced sensors** to perceive them!

In **Chapter 3.3: Advanced Sensor Simulation**, you'll:

- Configure RGB-D cameras with realistic noise and motion blur
- Simulate GPU-accelerated LiDAR with thousands of beams
- Generate semantic segmentation masks automatically
- Create ground-truth sensor data for AI training
- Leverage Isaac Sim's Replicator for domain randomization

**Continue to** → [Chapter 3.3: Advanced Sensor Simulation](./chapter-3-3-sensors)

---

## Assessment: Photorealistic Test Environment

**Goal**: Build a custom environment for testing a delivery robot.

**Requirements**:

1. **Scene specifications**:
   - Indoor environment (office or warehouse)
   - Minimum 20m × 20m floor area
   - 4+ walls with at least one doorway
   - 5+ props (shelves, boxes, tables, chairs)

2. **Visual quality**:
   - All surfaces use PBR materials (no default gray)
   - At least 3 different material types (wood, metal, concrete)
   - Proper lighting (minimum 3 lights, or 1 HDR dome + 2 area lights)
   - Realistic shadows visible in render

3. **Physics**:
   - Ground plane and walls have collision meshes
   - Props have simplified collision geometry
   - Demonstrate: Drop a cube, verify it lands on floor (doesn't penetrate)

4. **Deliverables**:
   - Saved USD file (`my_environment.usd`)
   - Screenshot (1920×1080, high quality, 8+ samples)
   - 300-word description explaining:
     - Design choices (why these materials/lighting)
     - Performance optimizations applied
     - Intended use case for robot testing

**Expected Pass Rate**: 70% of learners complete within 90 minutes.

**Bonus**: Import an external CAD model (forklift, pallet, machinery) and integrate with custom materials.

---

## Additional Resources

📚 **Official Documentation**:
- [Isaac Sim Materials Guide](https://docs.omniverse.nvidia.com/isaacsim/latest/advanced_tutorials/tutorial_advanced_materials.html)
- [USD Composition Guide](https://graphics.pixar.com/usd/docs/USD-Glossary.html#USDGlossary-Composition)
- [Omniverse PBR Shader Reference](https://docs.omniverse.nvidia.com/materials-and-rendering/latest/materials.html)

📺 **Video Tutorials**:
- NVIDIA Omniverse - PBR Materials Explained
- Isaac Sim - Building Custom Environments
- USD Composition Workflows

🛠️ **Assets & Tools**:
- [Poly Haven](https://polyhaven.com/) - Free HDRIs, textures, 3D models
- [Quixel Bridge](https://quixel.com/bridge) - Photogrammetry assets for Omniverse
- [Sketchfab](https://sketchfab.com/) - 3D models (check licenses)

📖 **Further Reading**:
- ["Physically Based Rendering" book](https://www.pbr-book.org/) - Deep dive into PBR theory
- [USD Survival Guide](https://lucascheller.github.io/VFX-UsdSurvivalGuide/) - Comprehensive USD reference

---

**Chapter Status**: Complete ✅
**Next Chapter**: [3.3 Advanced Sensor Simulation](./chapter-3-3-sensors)
