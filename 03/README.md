# Chapter 3 — Procedurality and Artificial Growth

> Supplementary materials for **Art Between Matter and Code** by Gianpiero Moioli.

## Contents

| Folder | Description |
|--------|-------------|
| `images/` | Reference images and figures |
| `models/` | Blender scene files (.blend) |
| `scripts/` | Python / Blender procedural scripts |
| `docs/` | Supplementary documents |
| `media/` | Videos and animations |

---

## Scripts (`scripts/`)

Eight Blender 5.x scripts demonstrating procedural modeling, algorithmic growth, and generative sculpture.  
Full parameter reference: **[scripts/README.md](scripts/README.md)**

| Script | Section | Description |
|--------|---------|-------------|
| `organic_surface.py` | §3.6.1.1 | Displace modifier — organic surfaces from procedural textures |
| `modular_patterns.py` | §3.6.1.2 | Geometry Nodes instancing with noise-driven density |
| `lattice_structures.py` | §3.6.1.3 | Wireframe + Remesh — bone, coral, architectural trusses |
| `fluid_geometry.py` | §3.6.1.5 | Animated noise deformation — flowing organic form |
| `fibonacci_growth.py` | §3.3 | Golden-angle phyllotaxis spiral in 3D |
| `picasso_gesture.py` | §3.6.2 | Bézier gesture → volumetric light trace, animated |
| `cragg_stack.py` | §3.6.3.1 | Stratified torsional surfaces (Tony Cragg, *Stack*) |
| `kapoor_tall_tree.py` | §3.6.3.2 | Column of mirrored spheres (Anish Kapoor, *Tall Tree & The Eye*) |

---

## Models (`models/`)

Blender scene files corresponding to the book figures. Open directly in Blender 5.x.

| File | Section | Description |
|------|---------|-------------|
| `3_6_1_1.blend` | §3.6.1.1 | Organic surface — Plane + Subdivision + Displace (Fig. 14) |
| `3_6_1_2.blend` | §3.6.1.2 | Modular patterns — Grid + Geometry Nodes instancing (Fig. 15) |
| `3_6_1_4.blend` | §3.6.1.4 | Techno-mechanical — Displace with grayscale image (Fig. 17) |
| `3_6_1_5.blend` | §3.6.1.5 | Fluid deformation — Icosphere + Geometry Nodes (Fig. 18) |
| `Fibonacci.blend` | §3.3 | Fibonacci / golden-angle growth via Geometry Nodes (Fig. 10) |
| `Fillotassi.blend` | §3.5.2 | Phyllotaxis — six procedural variations (Fig. 12–13) |
| `Picasso.blend` | §3.6.2 | Gesture curve + Starlight Atmosphere environment ⚠️ |
| `Kapoor.blend` | §3.6.3.2 | Tall Tree & The Eye — Geometry Nodes sphere column (Fig. 22) |
| `Cragg.blend` | §3.6.3.1 | Stack — Subdivision + Displace stratified surfaces (Fig. 20) |
| `AggregatoCellulare.blend` | §3.3 | Cellular aggregate — Icosphere + Geometry Nodes |
| `WireFlood.blend` | §3.6.1.3 | Wire flood lattice via Geometry Nodes |
| `Wires.blend` | §3.6.1.3 | Wireframe mesh + Geometry Nodes |
| `GeoNodes_001.blend` | §3.6.1.2 | Geometry Nodes introductory study |
| `Artificial_Intelligence_Flow.blend` | §3.1 | *Synthetic Circulation* — multi-object scene ⚠️ |

> ⚠️ `Picasso.blend` requires the **Starlight Atmosphere** add-on.  
> ⚠️ `Artificial_Intelligence_Flow.blend` references external texture assets (Poly Haven / BlenderKit).  
> Use the companion `.py` scripts for self-contained, dependency-free versions.
