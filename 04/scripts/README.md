# Chapter 4 — Scripts

> Python script for **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> No Blender required — runs with any Python 3.x installation (including Blender's bundled Python).

## Quick start

| Script | Launcher (Windows) | Description |
|--------|--------------------|-------------|
| `aura_transition.py` | `run_aura_transition.bat` | Generates the Aura & Reproducibility diagram as a standalone SVG |

**Windows:** double-click `run_aura_transition.bat`  
**macOS/Linux:** `./run_aura_transition.sh`  
**Manual:** `python aura_transition.py`  
**Custom output folder:** `python aura_transition.py --output path/to/folder`

Output: `ref_aura_transition_diagram.svg` — opens in any browser.

---

## `aura_transition.py` — Aura & Reproducibility Diagram

Programmatic companion to the conceptual diagram in the chapter. Generates a vector SVG plotting two crossing curves — **Aura** and **Reproducibility** — across five historical phases of art production, from the handmade object to AI-generated work.

This diagram maps Walter Benjamin's argument (*Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit*, 1935) that mechanical reproduction strips the artwork of its "aura" — the sense of unique presence tied to a specific place and time — and extends it through the digital and generative AI era.

### The five phases

| Phase | Period | Aura | Reproducibility |
|-------|--------|------|-----------------|
| Handmade Object | pre-1800 | 1.00 | 0.00 |
| Cast / Mould | 1800–1880 | 0.75 | 0.22 |
| Mechanical Reproduction | 1880–1960 | 0.30 | 0.70 |
| Digital / Parametric | 1960–2020 | 0.20 | 0.95 |
| AI-Generated | 2020 onwards | 0.55 | 1.00 |

> Note the "generative aura" paradox at the AI-Generated phase: reproducibility reaches its maximum (infinite output) while aura partially recovers — because each AI generation is a unique, unrepeatable process.

### Parameters (edit inside the script)

| Variable | Default | Description |
|----------|---------|-------------|
| `PHASES` | 5 entries | List of phases — each with `label`, `year`, `aura`, `repro`, `color`, `note` |
| `W`, `H` | `900`, `480` | SVG canvas width and height in pixels |
| `PAD_L/R/T/B` | `60/30/70/110` | Chart margins |

> **Tip:** Adjust the `aura` and `repro` values in the `PHASES` list to model alternative interpretations of the aura curve.
