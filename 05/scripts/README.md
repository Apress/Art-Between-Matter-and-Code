# Chapter 5 — Scripts

> Python scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Standard Python 3.x — no external libraries required.

## Quick start

| Script | Launcher (Windows) | Blender? | Section | Description |
|--------|--------------------|----------|---------|-------------|
| `hybrid_workflow_diagram.py` | `run_hybrid_workflow_diagram.bat` | No | §5.1 | Hybrid Workflow diagram → SVG |
| `geometry_nodes_growth.py` | `run_geometry_nodes_growth.bat` | Yes | §5.4.3 | Creates `procedural_sculpture_demo.blend` in models/ |
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
