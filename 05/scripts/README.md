# Chapter 5 — Scripts

> Python scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Standard Python 3.x — no external libraries required.

## Quick start

| Script | Launcher (Windows) | Blender? | Section | Description |
|--------|--------------------|----------|---------|-------------|
| `hybrid_workflow_diagram.py` | `run_hybrid_workflow_diagram.bat` | No | §5.1 | Hybrid Workflow diagram → SVG |
| `geometry_nodes_growth.py` | — (open in Blender Scripting, Alt+P) | Yes | §5.4.3 | Creates `procedural_sculpture_demo.blend` in models/ |
| `blender_vse_setup.py` | `run_blender_vse_setup.bat` | Yes | §5.3.1.4.1 | Configures VSE for AI video workflow |

---

## `hybrid_workflow_diagram.py` — Hybrid Workflow Diagram

**§5.1 · Reference diagram**

Generates the Hybrid Workflow — Technical Process diagram as a standalone SVG.  
The diagram maps the full continuum of hybrid artistic practices described in Chapter 5, from physical gesture to digital tools to AI generation to fabrication and exhibition.

**Run:**
```bash
python hybrid_workflow_diagram.py                    # saves SVG in current folder
python hybrid_workflow_diagram.py --output path/folder  # custom output folder
```

**Or double-click** `run_hybrid_workflow_diagram.bat` — saves to `../images/` and opens in your browser automatically.

### What the diagram shows

The diagram is organized in five columns, left to right:

| Column | Stage | Colour |
|--------|-------|--------|
| Physical / Manual | Manual painting, sculpture, physical objects | Blue |
| Acquisition | 2D / 3D Scanning (photogrammetry, LiDAR) | Green |
| Digital Processing | Digital painting, AI generation, 3D modeling | Green / Orange |
| Fabrication & Certification | 3D printing / FDM / SLA, CDM certification | Green / Gold |
| Outputs | Physical exhibition, XR, installation, digital / NFT | Purple |

Arrows show the workflow connections; a dashed arrow marks the bidirectional feedback loop between AI generation and digital painting (inpainting / outpainting).

### Parameters (edit inside the script)

| Variable | Default | Description |
|----------|---------|-------------|
| `W`, `H` | `960`, `600` | SVG canvas size in pixels |
| `NODES` | 13 entries | Position, label, sublabel, colour for each node |
| `ARROWS` | 20 connections | From/to node pairs with optional label |
| `COL_*` | various hex | Colour scheme for each category |

### Output file

`ref_hybrid_workflow_diagram.svg` — opens in any browser or vector editor (Inkscape, Illustrator, Affinity Designer).

---

## `geometry_nodes_growth.py` — Procedural Sculpture

**§5.4.3 · Algorithmic Growth: Toward Procedural Sculpture**

Creates a procedural sculpture in Blender using Geometry Nodes:
- **NoiseDisplacement** modifier: subdivided icosphere displaced along surface normals by a 3D noise texture
- **InstanceGrowth** modifier (interactive only): icosphere instances scattered across the surface, simulating organic growth
- Two exposed parameters: **Displacement** strength and **Density**
- Warm-stone Principled BSDF material, Cycles render setup (1920×1080, 64 samples)

**Run (interactive):**
1. Open Blender → Scripting workspace
2. Open `geometry_nodes_growth.py`
3. Press **Alt+P** — both modifiers are built; adjust parameters in the modifier stack

**Output:** `../models/procedural_sculpture_demo.blend`

### Parameters (edit inside the script)

| Variable | Default | Description |
|----------|---------|-------------|
| `DISP_STRENGTH` | `0.38` | Displacement amplitude |
| `NOISE_SCALE` | `2.8` | Noise frequency |
| `NOISE_DETAIL` | `10.0` | Noise octaves |
| `SUBDIV_LEVEL` | `4` | Subdivision iterations |
| `SPIKE_DENSITY` | `12.0` | Growth instances per unit area |
| `BASE_COLOR` | `(0.72, 0.67, 0.58, 1.0)` | Warm stone colour |

### Requirements

Blender 4.3 LTS or later. Uses the `ng.interface` API — not compatible with Blender 3.x.

---

## `blender_vse_setup.py` — Blender VSE Configuration

**§5.3.1.4.1 · Mini tutorial: AI Video with MidJourney V7 and Blender 5.0**

Configures Blender's Video Sequence Editor (VSE) for the AI video workflow:
- Output format: **H.264 / MP4**, CRF 18 (high quality)
- Resolution: **1920 × 1080**, 24 fps
- Switches to the **Video Editing** workspace automatically
- Creates a `VSE_Workflow_Instructions` text block inside Blender with the full step-by-step guide

**Run:**
1. Double-click `run_blender_vse_setup.bat` — Blender opens with the script pre-loaded in Scripting
2. Press **Alt+P** — render settings are applied and workspace switches to Video Editing
3. Add clips: **Add → Movie**
4. Export: **Render → Render Animation** (`Ctrl+F12`)

**Or from the Scripting workspace:** open `blender_vse_setup.py` and press **Alt+P**.

### What it sets up

| Setting | Value |
|---------|-------|
| Container | MP4 |
| Codec | H.264 |
| Quality (CRF) | 18 (near-lossless) |
| Resolution | 1920 × 1080 |
| Frame rate | 24 fps |
| Workspace | Video Editing |
