# Chapter 2 — Scripts

> Blender 5.x scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Each script opens Blender with the scene already built and loads itself into the Scripting workspace so the CONFIG block is immediately editable.

## Quick start

| Script | Windows | macOS / Linux | Section |
|--------|---------|---------------|---------|
| `piazza_metafisica.py` | `run_piazza_metafisica.bat` | `run_piazza_metafisica.sh` | §2.5.1 |
| `hybrid_workflow.py` | `run_hybrid_workflow.bat` | `run_hybrid_workflow.sh` | §2.3 |
| `scan_cleanup.py` | `run_scan_cleanup.bat` | `run_scan_cleanup.sh` | §2.1.2 |

**Windows:** double-click the `.bat` file — Blender is located automatically (checks versions 4.0–5.1).  
**macOS / Linux:** first run only: `chmod +x run_*.sh`, then `./run_script_name.sh`  
**Manual:** Blender → Scripting workspace → Open file → `Alt+P`

---

## `piazza_metafisica.py` — Piazza Metafisica: Hybrid Sculpture

Demonstrates the three-stage manual modeling workflow (§2.5.1, Figs. 15–17): a hybrid architectural-sculptural scene evoking De Chirico's metaphysical piazzas. The scene contains three types of elements:

- **Arcade** — three bays of paired pillars, lintels and a frieze (rational geometric architecture)
- **Floor** — a ground plane refined in Edit Mode with a sinusoidal wave deformation
- **Displaced volumes** — a floating sphere (blue-metallic), a tilted cube (red) and a tall obelisk: the surrealist elements that break the rational order of the piazza

The floating sphere serves a double role: it is the compositional surrealist element *and* the object prepared for Stage 3 (Sculpt Mode), receiving a Subdivision Surface and a Clouds displacement that simulate gestural brush marks.

The `MODE` parameter controls which stages are executed:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MODE` | `"all"` | Stages to run: `"object"` · `"edit"` · `"sculpt"` · `"all"` |
| `APPLY_BOOLEAN` | `True` | Apply boolean cuts on the arcade (reserved for future use) |
| `SUBDIVISIONS` | `2` | Subdivision Surface levels on the sphere before Sculpt Stage |

**Stage 1 — Object Mode:** volumetric composition with primitives (floor, arcade, displaced volumes).  
**Stage 2 — Edit Mode:** floor mesh subdivided 6× and deformed with a `sin(x) · cos(y)` wave.  
**Stage 3 — Sculpt Mode:** sphere prepared with Subdivision + Clouds displacement (simulates gestural sculpting). Switch to Sculpt Mode and use brushes to add further detail.

> **Tip:** set `MODE = "object"` to inspect Stage 1 alone, then `"edit"` or `"sculpt"` for the full sequence.

---

## `hybrid_workflow.py` — The Four-Phase Hybrid Workflow

Models the cyclical hybrid workflow (§2.3, Fig. 11): the same object evolves through four phases, each representing a node in the hybrid creative cycle. Use `START_PHASE` and `END_PHASE` to inspect any individual phase.

| Phase | Name | What happens |
|-------|------|-------------|
| 1 | Manual / Traditional | UV sphere with Clouds displacement simulates a hand-pressed clay maquette. Base flattened to simulate resting on a surface |
| 2 | Digital / Computational | Modifiers baked, voxel remesh for uniform topology, Subdivision Surface added |
| 3 | AI / Generative | Two-layer Musgrave noise (medium undulation + fine detail) simulates unpredictable AI variation |
| 4 | Digital Fabrication | All modifiers applied, merge doubles, normals recalculated, scaled to 20 cm diameter, optional STL export |

| Parameter | Default | Description |
|-----------|---------|-------------|
| `START_PHASE` | `1` | First phase to execute (1–4) |
| `END_PHASE` | `4` | Last phase to execute (1–4) |
| `EXPORT_STL` | `False` | Export the Phase 4 result as STL for 3D printing |
| `EXPORT_PATH` | `""` | STL output path — empty = saves next to the .blend file |

> **Tip:** run with `END_PHASE = 1` to see the raw maquette, then increase to watch it evolve.

---

## `scan_cleanup.py` — Photogrammetry Mesh Cleanup

Automates the post-processing pipeline for imported photogrammetry scans (§2.1.2, §2.5.2.1). Works on the **currently selected object** — import your scan first, select it, then run.

**Pipeline order:**
1. Apply transforms (rotation + scale)
2. Merge vertices by distance (remove scan noise)
3. Recalculate normals (outside-facing)
4. Fill small holes (up to 50 vertices per hole)
5. *(optional)* Voxel remesh → recalculate normals again
6. *(optional)* Subdivision Surface for smooth sculpt-ready preview
7. *(optional)* Musgrave displacement for artistic variation

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MERGE_DISTANCE` | `0.0005` | Vertex merge threshold in scene units (0.5 mm — typical scan noise) |
| `VOXEL_REMESH` | `True` | Rebuild as uniform voxel grid (cleans chaotic scan topology) |
| `VOXEL_SIZE` | `0.003` | Voxel size in scene units — smaller = more detail, heavier mesh |
| `SUBDIVIDE` | `True` | Add Subdivision Surface modifier (levels set by `SUB_LEVELS`) |
| `SUB_LEVELS` | `1` | Subdivision levels (1–3 recommended for scans) |
| `ADD_ARTISTIC` | `False` | Add Musgrave noise displacement for experimental variation |
| `NOISE_STRENGTH` | `0.015` | Displacement strength when `ADD_ARTISTIC = True` |

> **Workflow:** File → Import → OBJ / FBX / PLY → select the mesh in the viewport → run this script.  
> After cleanup, switch to **Sculpt Mode** to add gestural detail on top of the clean base.
