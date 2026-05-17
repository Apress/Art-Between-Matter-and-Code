# Chapter 5 — States of Transformation

> Supplementary materials for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Chapter 5: *States of Transformation: Painting, Sculpture, and Digital Expansion*  
> Part II — From Real to Virtual

## Contents

| Folder | Files | Description |
|--------|-------|-------------|
| `scripts/` | 3 Python scripts + 2 .bat launchers | Workflow diagram, procedural sculpture, VSE setup |
| `docs/` | 1 glossary + 3 artist notes | Key terms and artist profiles |
| `images/` | 6 SVG / PNG | Workflow diagram + book figures |
| `models/` | `procedural_sculpture_demo.blend` | Geometry Nodes sculpture (Blender 4.3+) |
| `media/` | `0001-0488.mp4` | AI-generated video clip for VSE demo |

## Scripts

| Script | Launcher | Section | Description |
|--------|----------|---------|-------------|
| `hybrid_workflow_diagram.py` | `run_hybrid_workflow_diagram.bat` | §5.1 | Generates the Hybrid Workflow SVG diagram |
| `geometry_nodes_growth.py` | Open in Blender Scripting → Alt+P | §5.4.3 | Creates `procedural_sculpture_demo.blend` in models/ |
| `blender_vse_setup.py` | `run_blender_vse_setup.bat` | §5.3.1.4.1 | Configures Blender VSE for AI video workflow |

**Run (Python):**
```bash
python scripts/hybrid_workflow_diagram.py             # saves SVG in current folder
python scripts/hybrid_workflow_diagram.py --output scripts/../images
```

Or double-click `scripts/run_hybrid_workflow_diagram.bat` — saves to `images/` and opens in browser.

**Run (Blender scripts):**
1. Open Blender → Scripting workspace
2. Open the script (`geometry_nodes_growth.py` or `blender_vse_setup.py`)
3. Press **Alt+P** to run

Or double-click `run_blender_vse_setup.bat` to launch Blender with the VSE script pre-loaded.

## 3D Models

| File | Section | Description |
|------|---------|-------------|
| `models/procedural_sculpture_demo.blend` | §5.4.3 | Procedural sculpture: noise-displaced icosphere with Geometry Nodes. Open in Blender 4.3+. Adjust **Displacement** and **Noise Scale** in the NoiseDisplacement modifier. |

## Media

| File | Section | Description |
|------|---------|-------------|
| `media/0001-0488.mp4` | §5.3.1.4.1 | AI-generated video clip (488 frames). Import into Blender VSE: **Add → Movie**. |

## Documents

| File | Section | Description |
|------|---------|-------------|
| `docs/ref_glossary.md` | all | Key terms: hybrid techniques, AI generation, CDM, photogrammetry, lost-wax casting, post-human identity… |
| `docs/artist_notes/01_hockney.md` | §5.2.2 | David Hockney — iPad drawings, scale independence, manual gesture in digital space |
| `docs/artist_notes/02_fontana.md` | §5.3.1.5 / §5.4 | Lucio Fontana — Spatialism, precursor to AI outpainting and virtual sculpture |
| `docs/artist_notes/03_op_de_beeck.md` | §5.4.4 | Hans Op de Beeck — 3D scanning + manual resin finishing (*Nocturnal Journey*, 2025) |

## Key tools in this chapter

| Tool | Type | Role |
|------|------|------|
| Stable Diffusion 1.5 | Local AI | Image generation, inpainting, outpainting |
| ComfyUI (Python 3.11.9, PyTorch 2.4.1) | Local AI interface | Node-based SD workflows |
| MidJourney V7 | Cloud AI | Image and video generation |
| Kling 2.5 / Runway Gen-3 | Cloud AI | Video synthesis |
| Blender 4.4 / 5.0 | 3D software | Modeling, procedural generation, video editing |
| ZBrush / Gravity Sketch | 3D/VR | Digital sculpting |
| GIMP / Procreate / Adobe Fresco | Digital painting | Manual digital painting workflows |
| Topaz Gigapixel AI v8.4.4 | Upscaling | 4× enlargement for monumental prints (SSIM > 0.95) |
| Real-ESRGAN / SwinIR | Upscaling (free) | Open-source alternatives to Gigapixel AI |
| certify_asset.py (Ch. 4) | Certification | SHA-256 + CDM for final artworks |

## How to use

- Blender files require **Blender 4.4 LTS** or later.
- Scripts require **Python 3.x** with no external libraries.
- For 3D scanning protocols, see Chapter 6.
- For CDM certification of final artworks, see `04/scripts/certify_asset.py`.
