"""
fabrication_workflow_diagram.py
────────────────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 6 — From Virtuality to Matter: 3D Printing and Material Translation

Generates the Virtual-to-Physical Fabrication Workflow diagram as a standalone SVG.

The diagram maps the complete fabrication chain:
  3D Model / Scan
    → Mesh Repair (3D Print Toolbox)
    → Slicing (Anycubic Slicer Next / Cura)
    → Printing (FDM / SLA / SLS / WASP Ceramic)
    → Post-Processing (Support Removal, Finishing, Assembly)
    → Output (Exhibition Prototype / Lost-Wax Casting / CDM Certification)

Reference: §6.1 (Virtual-to-Physical Workflow), Figures in the chapter.

Usage
─────
  python fabrication_workflow_diagram.py                   # saves SVG in current folder
  python fabrication_workflow_diagram.py --output ./out    # custom output folder
  python fabrication_workflow_diagram.py --output ../images

Requirements: Python 3.x, no external libraries.
"""

import argparse
import os
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION — edit freely
# ─────────────────────────────────────────────

W, H = 960, 620
OUTPUT_FILE = "ref_fabrication_workflow_diagram.svg"

PAD = 36            # outer margin

# Colours (dark-mode-friendly on white)
COL_VIRTUAL  = "#4A7FA5"   # blue  — virtual model inputs
COL_PREP     = "#6BAB6B"   # green — preparation
COL_FAB      = "#C9623F"   # orange — fabrication
COL_POST     = "#4A9C9C"   # teal  — post-processing
COL_OUTPUT   = "#7B5EA7"   # purple — outputs
COL_ARROW    = "#888888"
COL_BG       = "#FAFAFA"
COL_TITLE    = "#1A1A1A"
COL_LABEL    = "#333333"
COL_SUB      = "#666666"
COL_LEGEND_BG = "#FFFFFF"

FONT = "Arial, Helvetica, sans-serif"

# ── Column centre-x values ──────────────────────────────────────────────────
# Col 1 Virtual | Col 2 Preparation | Col 3 Fabrication | Col 4 PostProc | Col 5 Output
CX1, CX2, CX3, CX4, CX5 = 100, 252, 450, 680, 870

# ── Row centre-y values ──────────────────────────────────────────────────────
R1, R2, R3, R4, R5, R6 = 175, 270, 345, 420, 495, 555

# Standard node dimensions
NW, NH = 148, 48

# Node list: (cx, cy, w, h, label, sublabel, color)
NODES = [
    # ── Col 1: Virtual Model inputs ─────────────────────────────────────────
    (CX1, R1, NW, NH, "3D Model", "(Blender)",           COL_VIRTUAL),   # 0
    (CX1, R3, NW, NH, "Scan / SfM", "(Photogrammetry)", COL_VIRTUAL),   # 1

    # ── Col 2: Preparation ───────────────────────────────────────────────────
    (CX2, R2, NW, NH, "Mesh Repair", "(3D Print Toolbox)", COL_PREP),   # 2
    (CX2, R4, NW, NH, "Slicing", "(Anycubic / Cura)",      COL_PREP),   # 3

    # ── Col 3: Fabrication ───────────────────────────────────────────────────
    (CX3, R1, NW, NH, "FDM", "(PLA / PETG)",               COL_FAB),   # 4
    (CX3, R2+20, NW, NH, "SLA/MSLA", "(Resin)",            COL_FAB),   # 5
    (CX3, R3+30, NW, NH, "SLS", "(Nylon)",                 COL_FAB),   # 6
    (CX3, R4+30, NW, NH, "WASP Ceramic", "(Clay / Porcelain)", COL_FAB),  # 7

    # ── Col 4: Post-Processing ───────────────────────────────────────────────
    (CX4, R2, NW, NH, "Support Removal", "& Sanding",      COL_POST),  # 8
    (CX4, R3+15, NW, NH, "Manual Finishing", "& Painting", COL_POST),  # 9
    (CX4, R4+30, NW, NH, "Assembly", "(Modular)",          COL_POST),  # 10

    # ── Col 5: Output ────────────────────────────────────────────────────────
    (CX5, R2, NW, NH, "Exhibition", "Prototype",           COL_OUTPUT), # 11
    (CX5, R3+15, NW, NH, "Lost-Wax", "Casting",           COL_OUTPUT), # 12
    (CX5, R4+30, NW, NH, "CDM", "Certification",          COL_OUTPUT), # 13
]

# Arrows: (from_index, to_index)
# Node indices:
#   0 3DModel  1 ScanSfM
#   2 MeshRepair  3 Slicing
#   4 FDM  5 SLA/MSLA  6 SLS  7 WASPCeramic
#   8 SupportRemoval  9 ManualFinishing  10 Assembly
#  11 ExhibitionPrototype  12 LostWax  13 CDMCert
ARROWS = [
    # Virtual → Preparation
    (0, 2),   # 3DModel → MeshRepair
    (1, 2),   # ScanSfM → MeshRepair
    # Preparation chain
    (2, 3),   # MeshRepair → Slicing
    # Slicing → Fabrication
    (3, 4),   # Slicing → FDM
    (3, 5),   # Slicing → SLA/MSLA
    (3, 6),   # Slicing → SLS
    (3, 7),   # Slicing → WASPCeramic
    # Fabrication → Post-Processing
    (4, 8),   # FDM → SupportRemoval
    (5, 8),   # SLA/MSLA → SupportRemoval
    (4, 9),   # FDM → ManualFinishing
    (5, 9),   # SLA/MSLA → ManualFinishing
    (6, 9),   # SLS → ManualFinishing
    (7, 9),   # WASPCeramic → ManualFinishing
    (4, 10),  # FDM → Assembly
    # Post-Processing → Output
    (8, 11),  # SupportRemoval → ExhibitionPrototype
    (9, 11),  # ManualFinishing → ExhibitionPrototype
    (9, 12),  # ManualFinishing → LostWax
    (10, 11), # Assembly → ExhibitionPrototype
    (9, 13),  # ManualFinishing → CDMCertification
]


# ─────────────────────────────────────────────
# SVG helpers
# ─────────────────────────────────────────────

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _box(cx, cy, w, h, fill, radius=8):
    x, y = cx - w / 2, cy - h / 2
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="{radius}" ry="{radius}" '
        f'fill="{fill}" opacity="0.93" stroke="{fill}" stroke-width="1.5"/>'
    )


def _text(x, y, text, size=12, fill=COL_TITLE, weight="normal", anchor="middle"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">'
        f"{_esc(text)}</text>"
    )


def _tspan_lines(x, y, lines, size, fill, weight, anchor, line_height=15):
    """Multi-line text via tspan."""
    n = len(lines)
    base_y = y - (n - 1) * line_height / 2
    parts = [f'<text x="{x:.1f}" y="{base_y:.1f}" font-family="{FONT}" font-size="{size}" '
             f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">']
    for i, line in enumerate(lines):
        dy = 0 if i == 0 else line_height
        parts.append(f'<tspan x="{x:.1f}" dy="{dy}">{_esc(line)}</tspan>')
    parts.append("</text>")
    return "".join(parts)


def _arrow_line(x1, y1, x2, y2, color=COL_ARROW, dash=""):
    dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="1.4" marker-end="url(#arr)" {dash_attr}/>'
    )


def _node_edge(ni, nj, nodes):
    """Return (x1,y1,x2,y2) on edges of nodes ni → nj."""
    cx1, cy1, w1, h1 = nodes[ni][:4]
    cx2, cy2, w2, h2 = nodes[nj][:4]
    dx, dy = cx2 - cx1, cy2 - cy1

    if abs(dx) >= abs(dy):
        if dx > 0:
            x1 = cx1 + w1 / 2
            x2 = cx2 - w2 / 2
        else:
            x1 = cx1 - w1 / 2
            x2 = cx2 + w2 / 2
        frac = dy / (abs(dx) + 1)
        y1 = cy1 + frac * h1 / 2 * 0.5
        y2 = cy2 - frac * h2 / 2 * 0.5
    else:
        if dy > 0:
            y1 = cy1 + h1 / 2
            y2 = cy2 - h2 / 2
        else:
            y1 = cy1 - h1 / 2
            y2 = cy2 + h2 / 2
        frac = dx / (abs(dy) + 1)
        x1 = cx1 + frac * w1 / 2 * 0.5
        x2 = cx2 - frac * w2 / 2 * 0.5

    return x1, y1, x2, y2


# ─────────────────────────────────────────────
# Build SVG
# ─────────────────────────────────────────────

def build_svg():
    lines = []

    # Header
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    lines.append(f'<rect width="{W}" height="{H}" fill="{COL_BG}"/>')

    # Arrow marker
    lines.append("""<defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="{}" />
  </marker>
</defs>""".format(COL_ARROW))

    # Title
    lines.append(_text(W / 2, 32, "Virtual-to-Physical Fabrication Workflow", size=16,
                       fill=COL_TITLE, weight="bold"))
    lines.append(_text(W / 2, 52, "Chapter 6 · Art Between Matter and Code · Gianpiero Moioli · Apress 2025",
                       size=10, fill=COL_SUB))

    # Column headers
    col_labels = [
        (CX1, 95, "Virtual\nModel"),
        (CX2, 95, "Preparation"),
        (CX3, 95, "Fabrication"),
        (CX4, 95, "Post-\nProcessing"),
        (CX5, 95, "Output"),
    ]
    for cx, cy, lbl in col_labels:
        parts = lbl.split("\n")
        for i, part in enumerate(parts):
            lines.append(_text(cx, cy + i * 13, part, size=10, fill=COL_SUB, weight="bold"))

    # Arrows
    node_data = [(n[0], n[1], n[2], n[3]) for n in NODES]
    for (fi, ti) in ARROWS:
        x1, y1, x2, y2 = _node_edge(fi, ti, node_data)
        lines.append(_arrow_line(x1, y1, x2, y2))

    # Nodes
    for (cx, cy, w, h, label, sublabel, color) in NODES:
        lines.append(_box(cx, cy, w, h, color))
        if sublabel:
            lines.append(_text(cx, cy - 7, label, size=11, fill="white", weight="bold"))
            lines.append(_text(cx, cy + 9, sublabel, size=9, fill="rgba(255,255,255,0.82)"))
        else:
            lines.append(_text(cx, cy, label, size=11, fill="white", weight="bold"))

    # Legend
    legend_items = [
        (COL_VIRTUAL, "Virtual Model"),
        (COL_PREP,    "Preparation"),
        (COL_FAB,     "Fabrication"),
        (COL_POST,    "Post-Processing"),
        (COL_OUTPUT,  "Output"),
    ]
    lx, ly = PAD, H - 58
    lines.append(
        f'<rect x="{lx}" y="{ly}" width="360" height="48" rx="6" fill="{COL_LEGEND_BG}" '
        f'opacity="0.9" stroke="#ddd" stroke-width="1"/>'
    )
    lines.append(_text(lx + 180, ly + 10, "Legend", size=9, fill=COL_SUB, weight="bold"))
    for i, (col, lbl) in enumerate(legend_items):
        row, col_i = divmod(i, 3)
        x = lx + 12 + col_i * 116
        y = ly + 24 + row * 16
        lines.append(f'<rect x="{x}" y="{y - 5}" width="10" height="10" rx="2" fill="{col}"/>')
        lines.append(_text(x + 14, y, lbl, size=8.5, fill=COL_LABEL, anchor="start"))

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate the Virtual-to-Physical Fabrication Workflow diagram as an SVG (Chapter 6)."
    )
    parser.add_argument(
        "--output", default=".",
        help="Output folder for the SVG file (default: current directory)"
    )
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / OUTPUT_FILE

    svg_content = build_svg()
    out_path.write_text(svg_content, encoding="utf-8")
    print(f"[fabrication_workflow_diagram] Saved -> {out_path.resolve()}")
    print("  Open in any browser or vector editor (Inkscape, Illustrator, Affinity Designer).")


if __name__ == "__main__":
    main()
