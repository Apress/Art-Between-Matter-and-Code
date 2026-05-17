# Chapter 6 — Scripts

> Python scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Standard Python 3.x — no external libraries required.

## Quick start

| Script | Launcher (Windows) | Blender? | Section | Description |
|--------|--------------------|----------|---------|-------------|
| `fabrication_workflow_diagram.py` | `run_fabrication_workflow_diagram.bat` | No | §6.1 | Virtual-to-physical fabrication workflow → SVG |
| `print_ready_checker.py` | — (open in Blender Scripting, Alt+P) | Yes | §6.2 | Checks active mesh for 3D printability |

---

## `fabrication_workflow_diagram.py` — Fabrication Workflow Diagram

**§6.1 · Reference diagram**

Generates the Virtual-to-Physical Fabrication Workflow diagram as a standalone SVG.  
The diagram maps the complete fabrication chain described in Chapter 6, from 3D model and photogrammetry scan through mesh repair, slicing, and printing to post-processing and final output.

**Run:**
```bash
python fabrication_workflow_diagram.py                      # saves SVG in current folder
python fabrication_workflow_diagram.py --output path/folder # custom output folder
```

**Or double-click** `run_fabrication_workflow_diagram.bat` — saves to `../images/` and opens in your browser automatically.

### What the diagram shows

The diagram is organized in five columns, left to right:

| Column | Stage | Colour |
|--------|-------|--------|
| Virtual Model | 3D Model (Blender), Scan / SfM (Photogrammetry) | Blue |
| Preparation | Mesh Repair (3D Print Toolbox), Slicing (Anycubic / Cura) | Green |
| Fabrication | FDM, SLA/MSLA, SLS, WASP Ceramic | Orange |
| Post-Processing | Support Removal & Sanding, Manual Finishing & Painting, Assembly | Teal |
| Output | Exhibition Prototype, Lost-Wax Casting, CDM Certification | Purple |

Arrows show the workflow connections from digital file to physical object.

### Parameters (edit inside the script)

| Variable | Default | Description |
|----------|---------|-------------|
| `W`, `H` | `960`, `620` | SVG canvas size in pixels |
| `OUTPUT_FILE` | `ref_fabrication_workflow_diagram.svg` | Output filename |
| `NODES` | 14 entries | Position, label, sublabel, colour for each node |
| `ARROWS` | 20 connections | From/to node pairs |
| `COL_*` | various hex | Colour scheme for each category |

### Output file

`ref_fabrication_workflow_diagram.svg` — opens in any browser or vector editor (Inkscape, Illustrator, Affinity Designer).

---

## `print_ready_checker.py` — 3D Print Readiness Checker

**§6.2 · §6.2.5 Mini tutorial: Blender 3D Print Toolbox**

Blender Python script that checks the active mesh object for 3D printability. Reports results in the Blender System Console and as INFO messages. If `AUTO_FIX = True`, automatically runs Remove Doubles and Recalculate Normals before the diagnostic.

**Run (interactive):**
1. Open Blender → Scripting workspace
2. Open `print_ready_checker.py`
3. Select the mesh object you want to check in the viewport
4. Press **Alt+P** — results appear in the System Console

### What it checks

| Check | Method | Notes |
|-------|--------|-------|
| Non-manifold geometry | `bmesh` edge analysis | Edges shared by ≠ 2 faces; must be 0 for a watertight mesh |
| Bounding box dimensions | `obj.bound_box` + scale | Reported in scene units — verify mm in Scene Properties |
| Recalculate normals | `mesh.normals_make_consistent` | AUTO_FIX only |
| Remove doubles | `mesh.remove_doubles` | AUTO_FIX only, threshold = MERGE_THRESHOLD_MM |
| 3D Print Toolbox | `mesh.print3d_check_all` | Full diagnostic: thickness, overhang, distorted faces |

### Parameters (edit inside the script)

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_WALL_THICKNESS_MM` | `2.0` | Minimum wall thickness reference (FDM ≥2 mm) |
| `MAX_OVERHANG_ANGLE` | `45.0` | Overhang threshold in degrees from vertical |
| `MERGE_THRESHOLD_MM` | `0.01` | Merge by distance threshold for Remove Doubles |
| `AUTO_FIX` | `True` | Automatically fix normals and merge duplicate vertices |

### Requirements

Blender 4.3 LTS or later. The script attempts to enable the **3D Print Toolbox** addon automatically if it is not already active (bundled with Blender — no installation needed).
