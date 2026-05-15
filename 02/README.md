# Chapter 2 — Modeling as Creative Gesture

> Supplementary materials for **Art Between Matter and Code** by Gianpiero Moioli.

## Images (`images/`)

### Book figures — in order of appearance

| File | Caption (from book) |
|------|---------------------|
| `ref_canova_three_graces_hermitage.jpg` | Fig. 1 (left) — Canova, *Three Graces*, 1813–16, marble, Hermitage Museum. Public Domain |
| `ref_canova_tre_grazie_digital.jpg` | Fig. 1 (right) — Digital reinterpretation modeled in Blender (CC BY, pickle / Sketchfab) |
| `fig_02_mediterranean_landscape_original.png` | Fig. 2 (left) — G. Moioli, *Mediterranean Landscape*, original hand-painted work, 2025 |
| `fig_02a_mediterranean_landscape_ai_01.jpg` | Fig. 2 (centre) — AI reinterpretation via MidJourney V7. © G. Moioli |
| `fig_02b_mediterranean_landscape_ai_02.jpg` | Fig. 2 (right) — AI reinterpretation via MidJourney V7. © G. Moioli |
| `fig_02c_mediterranean_landscape_ai_03.jpg` | Fig. 2 — AI variation 3. © G. Moioli |
| `fig_02d_mediterranean_landscape_ai_04.jpg` | Fig. 2 — AI variation 4. © G. Moioli |
| `fig_03_raster_vs_vector.svg` | Fig. 3 — Raster vs. vector in digital painting and design |
| `fig_03_raster_vs_vector.png` | Fig. 3 — PNG version |
| `fig_04_modeling_and_sculpting.svg` | Fig. 4 — 3D Modeling & Sculpting: From Mesh Precision to Organic Detail |
| `fig_05_procedural_ai_diagram.svg` | Fig. 5 — From procedural/parametric design to AI-driven synthesis |
| `fig_06_interactive_xr_environments.svg` | Fig. 6 — Interactive installations and immersive XR environments |
| `fig_07_three_modeling_approaches.svg` | Fig. 7 — Three primary approaches to digital form-making |
| `fig_07_three_modeling_approaches.png` | Fig. 7 — PNG version |
| `fig_08_napoleon_bust_sketchfab.png` | Fig. 8 — Napoleon bust, Sketchfab / Virtual Museums of Małopolska, CC BY 4.0 |
| `fig_09_expanded_digital_artwork.svg` | Fig. 9 — Framework of the expanded digital artwork |
| `fig_10_real_vs_virtual.svg` | Fig. 10 — Real and Virtual: a fundamental polarity |
| `fig_11_hybrid_workflow_map.svg` | Fig. 11 — Hybrid Workflow Map (cyclical model) |
| `fig_11_hybrid_workflow_map.png` | Fig. 11 — PNG version |
| `fig_12_creative_design_process.svg` | Fig. 12 — The Creative Design Process: From Idea to Realization |
| `fig_12_creative_design_process.png` | Fig. 12 — PNG version |
| `fig_13_imaginative_phase.svg` | Fig. 13 — The Imaginative Phase: idea → sketches → preliminary design |
| `fig_13_imaginative_phase.png` | Fig. 13 — PNG version |
| `fig_14_productive_phase.svg` | Fig. 14 — The Productive Phase: design → prototype → production → installation |
| `fig_14_productive_phase.png` | Fig. 14 — PNG version |
| `fig_15_piazza_metafisica_object_mode.png` | Fig. 15 — *Piazza Metafisica*, Hybrid Sculpture (Object Mode) |
| `fig_16_piazza_metafisica_edit_mode.png` | Fig. 16 — *Piazza Metafisica*, Hybrid Sculpture (Edit Mode) |
| `fig_17_piazza_metafisica_sculpt_mode.png` | Fig. 17 — *Piazza Metafisica*, Hybrid Sculpture (Sculpt Mode) |
| `fig_18a_kiri_engine_home.jpg` | Fig. 18 — Photogrammetric scanning with Kiri Engine (home screen) |
| `fig_18b_kiri_engine_scan.jpg` | Fig. 18 — Kiri Engine scan in progress |
| `fig_18c_kiri_engine_result.jpg` | Fig. 18 — Kiri Engine 3D result |

### Reference images

| File | Subject |
|------|---------|
| `ref_3d_modeling_workflow_graph.svg` | 3D modeling workflow diagram (alternate) |
| `ref_digital_sculpture_diagram.svg` | Digital sculpture concept diagram |
| `ref_expanded_studio_diagram.svg` | Expanded Studio concept (alternate version) |
| `ref_piazza_metafisica_detail.png` | *Piazza Metafisica* — additional detail view |

---

## Scripts (`scripts/`)

Three Blender 5.x scripts with `.bat` / `.sh` launchers.  
Full parameter reference, stage descriptions and workflow notes: **[scripts/README.md](scripts/README.md)**

| Script | Section | Description |
|--------|---------|-------------|
| `piazza_metafisica.py` | §2.5.1 | *Piazza Metafisica* — hybrid sculpture across Object / Edit / Sculpt Mode (Figs. 15–17) |
| `hybrid_workflow.py` | §2.3 | Four-phase workflow: Manual → Digital → Generative → Fabrication (Fig. 11) |
| `scan_cleanup.py` | §2.1.2 | Photogrammetry mesh post-processing: clean, repair, remesh |

---

## Models (`models/`)

| File / Folder | License | Description |
|---------------|---------|-------------|
| `Napoleon.blend` | CC BY 4.0 | Blender scene with the Napoleon bust 3D scan |
| `Napoleon/` | CC BY 4.0 — Virtual Museums of Małopolska | OBJ + texture maps of the Napoleon bust (Fig. 8) |
| `Three_Graces/` | CC Attribution — pickle / Sketchfab | GLTF model of Canova's Three Graces digital reinterpretation (Fig. 1) |

---

## Media (`media/`)

| File | Section | Description |
|------|---------|-------------|
| `fig_02_mediterranean_landscape_animation.mp4` | §2.1.1 | *Mediterranean Landscape* — rendered animation (960 frames, Blender 5.0 + Midjourney V7) |
| `ai_video_mediterranean_01.mp4` | §2.1.1 | AI-generated video variation 01 (OpenArt) |
| `ai_video_mediterranean_02.mp4` | §2.1.1 | AI-generated video variation 02 (OpenArt) |
| `ai_video_mediterranean_03.mp4` | §2.1.1 | AI-generated video variation 03 (OpenArt) |
| `ai_video_mediterranean_04.mp4` | §2.1.1 | AI-generated video variation 04 (OpenArt) |
| `lofi-lofi-song-2-434695.mp3` | — | Royalty-free soundtrack (Pixabay — see `beats-lofi-lofi-song-2-434695-license.txt`) |

Music attribution: *Music by FreeMusicForVideo from Pixabay*

---

## Documents (`docs/`)

| File | Section | Description |
|------|---------|-------------|
| `ref_glossary.md` | all | Key terms: mesh, retopology, photogrammetry, NeRF, boolean, XR, PBR |
| `ref_bibliography.md` | all | References and further reading |
| `artist_notes/01_kapoor_balmond.md` | §2.4.1 | Anish Kapoor & Cecil Balmond — digital form-finding, *Marsyas*, *Cloud Gate* |
| `artist_notes/02_eliasson.md` | §2.2 | Olafur Eliasson — *The Weather Project*, real/virtual perception |
| `artist_notes/03_moore.md` | §2.2, §2.5.2 | Henry Moore — maquettes as generative seeds, mass/void |
