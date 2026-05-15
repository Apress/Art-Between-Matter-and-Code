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

Companion to §2.3 and Fig. 11 (*Hybrid Workflow Map*). The script models the cyclical creative process described in the chapter: a single object — a UV sphere — evolves through four distinct phases, each representing one node in the hybrid workflow. The material colour changes at each phase to make the transition immediately visible.

The key idea is that the artist does not work linearly from idea to result, but moves back and forth between four domains: the hand, the computer, the generative system, and the fabrication machine.

---

### The four phases in detail

**Phase 1 — Manual / Traditional** *(warm amber material)*  
A UV sphere receives a *Clouds* procedural texture via a Displace modifier, simulating the irregular surface of a hand-pressed clay maquette. The base vertices below Z = −0.7 are flattened in Edit Mode to simulate the object resting on a surface. This is the starting point: the physical gesture, the artist's hand in matter.

**Phase 2 — Digital / Computational** *(digital blue material)*  
The Phase 1 modifiers are applied (baked into the mesh). A **voxel remesh** rebuilds the topology as a uniform grid — this simulates the retopology step, cleaning the irregular hand-made surface into a controlled digital mesh. A Subdivision Surface is then added for a smooth, precise digital surface. The form is the same, but it now belongs to the logic of the machine.

**Phase 3 — AI / Generative** *(generative violet material)*  
Two layers of **Musgrave** procedural noise are added on top:
- *GenVar_Low*: medium-scale undulation (`HYBRID_MULTIFRACTAL`, scale 1.2) — the large unpredictable deformation
- *GenVar_High*: fine-scale detail (`CLOUDS`, scale 0.25, 4 octaves) — the micro-texture

Together they simulate the kind of unpredictable, multi-frequency variation that a generative or AI system introduces: the form is recognisable but transformed beyond what the artist alone would have done.

**Phase 4 — Digital Fabrication** *(fabrication green material)*  
All modifiers are applied. Duplicate vertices are merged, normals recalculated. The object is **scaled to 20 cm diameter** — a real-world physical dimension, not an abstract Blender unit. If `EXPORT_STL = True`, the mesh is exported as an STL file ready for a 3D printer. The form returns to the physical world, but it carries the marks of all four phases.

---

### How to change phases

The `START_PHASE` and `END_PHASE` parameters in the CONFIG block control which phases are executed. To change them:

1. Open Blender and run the script once (double-click `run_hybrid_workflow.bat` or press `Alt+P` in the Scripting workspace)
2. The script loads itself into the **Scripting workspace** — the CONFIG block is visible at the top of the editor
3. Edit the values directly:

```python
START_PHASE = 1   # change this
END_PHASE   = 4   # and this
```

4. Press **`Alt+P`** to re-run — the scene rebuilds with only the selected phases

**Suggested sequence for a lesson or demonstration:**

| Run | START_PHASE | END_PHASE | What you see |
|-----|-------------|-----------|-------------|
| 1st | `1` | `1` | Raw clay maquette — warm amber, irregular surface |
| 2nd | `1` | `2` | + Digital retopology — blue, clean uniform mesh |
| 3rd | `1` | `3` | + Generative variation — violet, unpredictable noise layers |
| 4th | `1` | `4` | + Fabrication ready — green, 20 cm, optionally exported as STL |

You can also isolate a single phase: `START_PHASE = 3`, `END_PHASE = 3` shows only the generative variation applied to a fresh sphere, without the previous phases.

---

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `START_PHASE` | `1` | First phase to execute (1–4) |
| `END_PHASE` | `4` | Last phase to execute (1–4) |
| `EXPORT_STL` | `False` | Export the Phase 4 result as STL for 3D printing |
| `EXPORT_PATH` | `""` | STL output path — leave empty to save next to the .blend file |

> **Note:** `EXPORT_STL` only has effect when `END_PHASE = 4`. The STL is scaled to real-world dimensions (20 cm diameter) and is manifold — ready to send directly to a slicer.

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
