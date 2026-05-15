# Chapter 3 — Scripts

> Blender 5.x scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Each script opens Blender with the scene already built and loads itself into the Scripting workspace so the CONFIG block is immediately editable.

## Quick start

| Script | Launcher (Windows) | Section | Description |
|--------|--------------------|---------|-------------|
| `organic_surface.py` | `run_organic_surface.bat` | §3.6.1.1 | Displace modifier — skin, terrain, alien membranes |
| `modular_patterns.py` | `run_modular_patterns.bat` | §3.6.1.2 | Geometry Nodes instancing with noise-driven density |
| `lattice_structures.py` | `run_lattice_structures.bat` | §3.6.1.3 | Wireframe + Remesh — bone, coral, architectural trusses |
| `fluid_geometry.py` | `run_fluid_geometry.bat` | §3.6.1.5 | Animated noise deformation — flowing organic form |
| `fibonacci_growth.py` | `run_fibonacci_growth.bat` | §3.3 | Golden-angle spiral — phyllotaxis in 3D |
| `picasso_gesture.py` | `run_picasso_gesture.bat` | §3.6.2 | Bézier gesture → volumetric light trace, animated |
| `cragg_stack.py` | `run_cragg_stack.bat` | §3.6.3.1 | Stratified torsional surfaces (after Tony Cragg) |
| `kapoor_tall_tree.py` | `run_kapoor_tall_tree.bat` | §3.6.3.2 | Column of mirrored spheres (after Anish Kapoor) |

**Windows:** double-click the `.bat` file — Blender is located automatically (checks versions 4.3–5.1).  
**Manual:** Blender → Scripting workspace → Open file → `Alt+P`

> **§3.6.1.4 — no script.** This section uses the same modifier stack as `organic_surface.py` (Plane + Subdivision + Displace + Subdivision) but replaces the procedural texture with a **ChatGPT-generated image** as the displacement height map. The conceptual point is the choice of the image, not the code — open `3_6_1_4.blend` directly and swap the image in the Displace modifier to experiment.  
Or run from terminal: `blender --python script_name.py`

---

## `organic_surface.py` — Organic Surface with the Displace Modifier

**§3.6.1.1 · Figure 14**

Transforms a flat plane into a complex relief by applying procedural displacement textures. The modifier stack is:

1. **Subdivision Surface** (pre) — adds geometry for the displacement to work on
2. **Displace** — procedural texture drives the surface relief
3. **Subdivision Surface** (post) — smooths the displaced surface

| Parameter | Default | Description |
|-----------|---------|-------------|
| `TEXTURE_TYPE` | `"MUSGRAVE"` | Texture type: `"MUSGRAVE"` · `"CLOUDS"` · `"VORONOI"` |
| `STRENGTH` | `0.25` | Displacement height |
| `MIDLEVEL` | `0.5` | Neutral plane offset |
| `NOISE_SIZE` | `1.0` | Texture spatial scale |
| `SUB_PRE` | `2` | Subdivision levels before displacement |
| `SUB_POST` | `2` | Subdivision levels after displacement |

> **Tip:** Change `TEXTURE_TYPE` to `"VORONOI"` for a cellular, skin-like result; use `"CLOUDS"` for softer, geological undulations.

---

## `modular_patterns.py` — Repeating Patterns with Geometry Nodes

**§3.6.1.2 · Figure 15**

Distributes sphere instances across a grid surface using a Geometry Nodes network. Density is driven by a Noise Texture, creating organic clusters that shift between ordered grids and chaotic arrangements.

Node graph: `Group Input → Distribute Points on Faces (noise density) → Instance on Points (random scale) → Realize Instances → Group Output`

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DENSITY_MAX` | `2.0` | Maximum instance density (points/m²) |
| `SCALE_MIN` | `0.08` | Minimum random scale |
| `SCALE_MAX` | `0.22` | Maximum random scale |
| `NOISE_SCALE` | `0.3` | Spatial frequency of density variation |
| `MODULE_RADIUS` | `0.12` | Radius of the sphere module |

> **Tip:** Replace the `Module_Sphere` object with any mesh (cone, cube, custom shape) for a completely different pattern vocabulary.

---

## `lattice_structures.py` — Hollow and Lattice Structures

**§3.6.1.3 · Figure 16**

Converts solid icospheres into open frameworks recalling bone, coral, or architectural trusses. Two methods compared side by side:

- **Wireframe method** — Wireframe modifier converts edges into structural struts
- **Remesh method** — Voxel Remesh rebuilds topology, optional Decimate adds organic irregularity

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MODE` | `"both"` | `"wireframe"` · `"remesh"` · `"both"` |
| `WIRE_THICKNESS` | `0.03` | Strut width (Wireframe modifier) |
| `VOXEL_SIZE` | `0.08` | Voxel resolution (smaller = finer lattice) |
| `DECIMATE_RATIO` | `0.5` | Mesh reduction after remesh (1.0 = none) |

---

## `fluid_geometry.py` — Fluid Simulation in Geometry Nodes

**§3.6.1.5 · Figure 18**

An icosphere deforms continuously through a 4D Noise Texture driven by `Scene Time`, producing animated ripples and fluid distortions. The form exists between sculpture and performance — it can be exported as GLB for virtual exhibition platforms.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `NOISE_SCALE` | `1.5` | Spatial frequency of deformation |
| `NOISE_STRENGTH` | `0.35` | Displacement amplitude |
| `SPEED` | `0.02` | Animation speed (noise W offset per frame) |
| `SUBDIVISIONS` | `4` | Icosphere subdivision level |
| `EXPORT_GLB` | `False` | Export as GLB for virtual platforms |

> **Press Space** to play the 120-frame fluid animation.

---

## `fibonacci_growth.py` — Fibonacci-Based Organic Growth

**§3.3 · Figure 10**

Places mesh instances along a golden-angle (≈137.5°) distribution — the mathematical principle found in sunflower seeds, pinecones, and nautilus shells. Each element is positioned using `r = √(i/N) · 2.5`, rotated by the golden angle, and scaled proportionally to its distance from the centre.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `N_ELEMENTS` | `120` | Total number of instances |
| `SCALE_BASE` | `0.08` | Base scale per element |
| `HEIGHT_FACTOR` | `0.04` | Vertical rise per element |
| `NOISE_AMOUNT` | `0.015` | Random jitter (0 = perfect mathematical spiral) |
| `MODULE` | `"SPHERE"` | Module type: `"SPHERE"` · `"CUBE"` · `"CONE"` |

> Set `NOISE_AMOUNT = 0` for a perfect mathematical spiral; increase it for organic irregularity.

---

## `picasso_gesture.py` — Picasso's Procedural Gesture

**§3.6.2**

A Bézier curve drawn in 3D space is given volume via bevel depth and transformed through a Trim Curve Geometry Nodes modifier that animates the progressive unfolding of the line — as if traced by Picasso's hand in a darkened room. The curve emits light (Emission shader) against a dark world background.

> The companion `.blend` (`Picasso.blend`) includes the Starlight Atmosphere add-on for a full night-sky environment. This script provides a self-contained version using standard Cycles nodes.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BEVEL_DEPTH` | `0.04` | Thickness of the volumetric line |
| `ANIMATE` | `True` | Animate the Trim Curve (gesture draws itself) |
| `LIGHT_COLOR` | `(1.0, 0.85, 0.4)` | Emissive colour of the light trace |
| `EMISSION_STR` | `8.0` | Glow intensity |
| `CURVE_POINTS` | `12` | Control points of the gesture path |

> **Press Space** to watch the 80-frame light-drawing animation.

---

## `cragg_stack.py` — Tony Cragg: Stratified Torsional Surfaces

**§3.6.3.1 · Figure 20**

Generates layered, twisted volumes inspired by Tony Cragg's *Stack* (2011). A bmesh torsion twists the base cube, then a Subdivision Surface + Musgrave Displace modifier adds stratified geological layering. An optional animation shows the displacement strength growing from 0 to maximum over 60 frames — a "frozen moment of movement" made editable.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `STRENGTH` | `0.40` | Displacement amplitude (layering depth) |
| `NOISE_SCALE` | `0.8` | Texture spatial frequency |
| `SUB_LEVELS` | `3` | Subdivision levels |
| `TORSION` | `35.0` | Twist angle top-to-bottom (degrees) |
| `ANIMATE` | `True` | Keyframe animation of displacement growth |

---

## `kapoor_tall_tree.py` — Anish Kapoor: Tall Tree & The Eye

**§3.6.3.2 · Figure 22**

Procedurally recreates Kapoor's vertical column of mirrored spheres using two complementary approaches. The Geometry Nodes method distributes spheres inside a cylindrical volume with density and scale variation; the Python loop method builds the column element by element with explicit random offsets.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MODE` | `"geonodes"` | `"geonodes"` · `"python"` · `"both"` |
| `N_SPHERES` | `60` | Number of spheres |
| `COLUMN_HEIGHT` | `5.0` | Total height in scene units |
| `RADIUS_BASE` | `0.30` | Base sphere radius |
| `RADIUS_VAR` | `0.10` | Random radius variation |
| `MIRROR_FINISH` | `True` | Near-mirror metallic material |

> Use `MODE = "both"` for a side-by-side comparison of the two approaches. Set `MIRROR_FINISH = False` for a matte study version.
