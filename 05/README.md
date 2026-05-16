# Chapter 5 — States of Transformation

> Supplementary materials for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Chapter 5: *States of Transformation: Painting, Sculpture, and Digital Expansion*  
> Part II — From Real to Virtual

## Contents

| Folder | Files | Description |
|--------|-------|-------------|
| `scripts/` | 1 Python script + 1 .bat launcher | Hybrid Workflow diagram generator |
| `docs/` | 1 glossary + 3 artist notes | Key terms and artist profiles |
| `images/` | 1 SVG | Reference workflow diagram |
| `models/` | — | (see Chapter 6 for 3D scanning workflows) |
| `media/` | — | Video links in the chapter text |

## Scripts

| Script | Launcher | Section | Description |
|--------|----------|---------|-------------|
| `hybrid_workflow_diagram.py` | `run_hybrid_workflow_diagram.bat` | §5.1 | Generates the Hybrid Workflow SVG diagram |

**Run:**
```bash
python scripts/hybrid_workflow_diagram.py             # saves SVG in current folder
python scripts/hybrid_workflow_diagram.py --output scripts/../images
```

Or double-click `scripts/run_hybrid_workflow_diagram.bat` — saves to `images/` and opens in browser.

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
