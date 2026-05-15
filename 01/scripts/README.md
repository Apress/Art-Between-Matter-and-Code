# Chapter 1 — Scripts

> Blender 5.x scripts for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Each script opens Blender with the scene already built and loads itself into the Scripting workspace so the CONFIG block is immediately editable.

## Quick start

| Script | Windows | macOS / Linux |
|--------|---------|---------------|
| `fontana_cut.py` | `run_fontana_cut.bat` | `run_fontana_cut.sh` |
| `parametric_space.py` | `run_parametric_space.bat` | `run_parametric_space.sh` |
| `material_spectrum.py` | `run_material_spectrum.bat` | `run_material_spectrum.sh` |

**Windows:** double-click the `.bat` file — Blender is located automatically (checks versions 4.0–5.1).  
**macOS / Linux:** first run only: `chmod +x run_*.sh`, then `./run_script_name.sh`  
**Manual:** Blender → Scripting workspace → Open file → `Alt+P`

---

## `fontana_cut.py` — Procedural Fontana Cut

Parametric reinterpretation of Fontana's *Concetto Spaziale, Attese*. Builds a vertical linen canvas (manifold cube) and carves organic boolean cuts into it. Each blade is a custom bmesh volume with a curved spine (sine), tapered width (zero at both tips), and independent edge noise reproducing the *slabbrato* — the frayed, torn quality of a real Fontana cut.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `NUM_CUTS` | `5` | Number of cuts (Fontana typically used 1–7) |
| `CUT_ANGLE` | `10.0` | Lean of each blade from vertical in degrees — alternates ± |
| `CUT_DEPTH` | `0.08` | How far the blade protrudes through the canvas (Y axis) |
| `CUT_WIDTH` | `0.015` | Blade thickness — thin = sharp cut, wider = torn gap |
| `CUT_LENGTH` | `0.72` | Cut length as fraction of canvas height (0.0–1.0) |
| `CANVAS_SIZE` | `2.0` | Canvas half-extent in Blender units (total = 2 × this) |
| `SPACING` | `"even"` | Cut distribution: `"even"` · `"random"` · `"golden"` |
| `SEED` | `42` | Random seed — change to explore different organic variations |

---

## `parametric_space.py` — Space as Generative Field

Translates the chapter's central concept into geometry: a dense vertex grid deformed by a sinusoidal field equation. Designed to run **in the same Blender session** as `fontana_cut.py` — it preserves the FontanaCanvas and adds the ParametricSpace object alongside it.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `GRID_DENSITY` | `40` | Vertices per side — 40 = 1 600 points (resolution of spatial fabric) |
| `GRID_SIZE` | `4.0` | Total extent of the field in Blender units |
| `WAVE_AMPLITUDE` | `0.35` | Height of field deformation — spatial energy intensity |
| `WAVE_FREQUENCY` | `2.5` | Oscillation cycles across the grid |
| `FIELD_PROFILE` | `"radial"` | Field shape: `"radial"` (concentric) · `"linear"` (directional) · `"turbulent"` (noise) |
| `NOISE_SCALE` | `1.8` | Turbulence detail scale — active when `FIELD_PROFILE = "turbulent"` |
| `NOISE_DEPTH` | `4` | Octaves of turbulence noise detail |
| `SOLIDIFY` | `True` | Add thickness to the surface (print / fabrication ready) |
| `SOLIDIFY_THICK` | `0.02` | Solidify thickness in Blender units |
| `EMIT_PARTICLES` | `False` | Add a particle system to visualise energy propagation |

> **Workflow note:** run after `fontana_cut.py` in the same Blender session. The FontanaCanvas is preserved.

---

## `material_spectrum.py` — The Material-Digital Continuum

The same sculptural form rendered in five material states, left to right:  
**white marble → terracotta → bronze → digital glass → wireframe**  
Maps the arc from Canova's studio to the 3D printer — the central argument of §1.2.

Each state uses a distinct Principled BSDF configuration: marble has subsurface scattering for inner luminosity; terracotta is rough and opaque with displacement; bronze is fully metallic; glass uses full transmission; wireframe uses the Wireframe modifier with an emission material — geometry without surface, code without matter.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BASE_FORM` | `"sphere"` | Sculptural shape: `"sphere"` · `"cube"` · `"torus"` |
| `SPACING` | `1.8` | Distance between objects in Blender units |
| `SEED` | `7` | Random seed for marble and terracotta surface variation |
