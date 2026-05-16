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

Five Blender 5.x scripts demonstrating procedural modeling and algorithmic growth.  
Full parameter reference: **[scripts/README.md](scripts/README.md)**

| Script | Section | Description |
|--------|---------|-------------|
| `organic_surface.py` | §3.6.1.1 | Displace modifier — organic surfaces from procedural textures |
| `lattice_structures.py` | §3.6.1.3 | Wireframe + Remesh — bone, coral, architectural trusses |
| `fluid_geometry.py` | §3.6.1.5 | Animated noise deformation — flowing organic form |
| `fibonacci_growth.py` | §3.3 | Golden-angle phyllotaxis spiral in 3D |
| `picasso_gesture.py` | §3.6.2 | Bézier gesture → volumetric light trace, animated |

---

## Models (`models/`)

Blender scene files corresponding to the book figures. Open directly in Blender 5.x.

| File | Section | Description |
|------|---------|-------------|
| `3_6_1_1.blend` | §3.6.1.1 | Organic surface — Plane + Subdivision + Displace (Fig. 14) |
| `3_6_1_2.blend` | §3.6.1.2 | Modular patterns — Grid + Geometry Nodes instancing (Fig. 15) |
| `3_6_1_4.blend` | §3.6.1.4 | AI-driven displacement — Displace with ChatGPT-generated image as height map (Fig. 17). No dedicated script: the conceptual choice is the image, not the code. |
| `3_6_1_5.blend` | §3.6.1.5 | Fluid deformation — Icosphere + Geometry Nodes (Fig. 18) |
| `Fibonacci.blend` | §3.3 | Fibonacci / golden-angle growth via Geometry Nodes (Fig. 10) |
| `Phyllotaxis.blend` | §3.5.2 | Phyllotaxis — procedural variations (Figs. 12–13) |
| `Picasso.blend` | §3.6.2 | Gesture curve + Starlight Atmosphere environment ⚠️ |
| `Kapoor.blend` | §3.6.3.2 | Tall Tree & The Eye — Geometry Nodes sphere column (Fig. 22) |
| `Cragg.blend` | §3.6.3.1 | Stack — Subdivision + Displace stratified surfaces (Fig. 20) |
| `Cellular _Aggregate.blend` | §3.3 | Cellular aggregate — Icosphere + Geometry Nodes |
| `Artificial_Intelligence_Flow.blend` | §3.1 | *Synthetic Circulation* — multi-object scene ⚠️ |

> ⚠️ `Picasso.blend` requires the **Starlight Atmosphere** add-on.  
> ⚠️ `Artificial_Intelligence_Flow.blend` references external texture assets (Poly Haven / BlenderKit).  
> Use the companion `.py` scripts for self-contained, dependency-free versions.

---

## Images (`images/`)

| File | Description |
|------|-------------|
| `001_modeling_paradigms.svg` | Modeling paradigms diagram |
| `002_Picasso_001-Pagina001.bmp` | Fig. 2 — Picasso light-drawing reference |
| `006_Man_Proc_AI-Pagina001.bmp` | Fig. 6 — Manual / Procedural / AI diagram |
| `010_Phyllotaxis.png` | Fig. 10 — Phyllotaxis golden-angle distribution |
| `011_Phyllotaxis.png` | Fig. 11 — Phyllotaxis variation |
| `013_Phyllotaxis_System-Pagina001.png` | Fig. 13 — Phyllotaxis system diagram |
| `Bilbao_-_Museo_Guggenheim_-_Tall_Tree_and_the_Eye_(Anish_Kapoor).jpg` | Ref. — Kapoor, *Tall Tree and the Eye*, Guggenheim Bilbao (Wikimedia CC) |
| `golden-spiral.svg` | Golden spiral — Fibonacci geometry |
| `vogel_sunflower_cc0.svg` | Vogel sunflower — phyllotaxis reference (CC0) |

---

## Media (`media/`)

| File | Description |
|------|-------------|
| `Procedural_Variations.mp4` | Procedural variations animation |
| `openart-video_74b025d4_1770563254591.mp4` | AI-generated video reference |
| `openart-video_9870779e_1770563180891.mp4` | AI-generated video reference |
| `openart-video_fa2743f1_1770563214127.mp4` | AI-generated video reference |

---

## Docs (`docs/`)

| File | Description |
|------|-------------|
| `ref_glossary.md` | 22 key terms for Chapter 3 |
| `artist_notes/01_picasso.md` | Pablo Picasso — light drawing, §3.6.2 |
| `artist_notes/02_cragg.md` | Tony Cragg — *Stack*, §3.6.3.1 |
| `artist_notes/03_kapoor.md` | Anish Kapoor — *Tall Tree and the Eye*, §3.6.3.2 |
