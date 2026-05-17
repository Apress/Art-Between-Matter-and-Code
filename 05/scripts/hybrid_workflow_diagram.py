"""
hybrid_workflow_diagram.py
──────────────────────────
Art Between Matter and Code · Gianpiero Moioli · Apress 2025
Chapter 5 — States of Transformation: Painting, Sculpture, and Digital Expansion

Generates the Hybrid Workflow diagram as a standalone SVG.

The diagram maps the technical continuum of hybrid artistic processes:
  Manual Painting / Sculpting
    → 2D / 3D Scanning
    → Digital Painting · AI Image Generation · 3D Modeling
    → Prototyping (3D Printing / Fabrication)
    → Physical Exhibition · XR Exhibition · Installation · Certification

Reference: §5.1 (Hybrid Techniques), Figures 4 and 5 in the chapter.

Usage
─────
  python hybrid_workflow_diagram.py                   # saves SVG in current folder
  python hybrid_workflow_diagram.py --output ./out    # custom output folder

Requirements: Python 3.x, no external libraries.
"""

import argparse
import os
import math
import textwrap
from pathlib import Path

# ─────────────────────────────────────────────
# CONFIGURATION — edit freely
# ─────────────────────────────────────────────

OUTPUT_FILENAME = "ref_hybrid_workflow_diagram.svg"

# Canvas
W, H = 960, 680
PAD = 40            # outer margin

# Colours  (dark-mode-friendly on white)
COL_MANUAL    = "#4A7FA5"   # blue — manual / physical
COL_DIGITAL   = "#6BAB6B"   # green — digital tools
COL_AI        = "#C9623F"   # orange — AI / generative
COL_OUTPUT    = "#7B5EA7"   # purple — outputs / exhibition
COL_CERT      = "#B8860B"   # gold — certification / CDM
COL_ARROW     = "#555555"
COL_BG        = "#FAFAFA"
COL_TITLE     = "#1A1A1A"
COL_LABEL     = "#333333"
COL_SUB       = "#666666"
COL_LEGEND_BG = "#FFFFFF"

FONT = "Arial, Helvetica, sans-serif"

# Node layout: (cx, cy, w, h, label, sublabel, color)
# Three columns: Physical → Digital Core → Outputs
#   col_x values at 110, 370, 630, 860 (quarter points minus padding)

NODES = [
    # ── LEFT: Physical inputs ──────────────────────────────
    (110, 160, 160, 54, "Manual Painting",   "acrylic · ink · pen",      COL_MANUAL),   # 0
    (110, 300, 160, 54, "Manual Sculpture",  "clay · plaster · metal",   COL_MANUAL),   # 1
    (110, 450, 160, 54, "Physical Object",   "scan target · heritage",   COL_MANUAL),   # 2

    # ── CENTER-LEFT: Scanning / acquisition ────────────────
    (340, 300, 160, 54, "2D / 3D Scanning",  "photogrammetry · LiDAR",   COL_DIGITAL),  # 3

    # ── CENTER: Digital processing ─────────────────────────
    (530, 155, 150, 50, "Digital Painting",  "GIMP · Procreate · Krita", COL_DIGITAL),  # 4
    (530, 290, 150, 50, "AI Generation",     "SD 1.5 · MidJourney V7",   COL_AI),       # 5
    (530, 420, 150, 50, "3D Modeling",       "Blender · Geo Nodes",      COL_DIGITAL),  # 6
    (530, 560, 150, 50, "Digital Sculpture", "ZBrush · Gravity Sketch",  COL_DIGITAL),  # 7 NEW

    # ── CENTER-RIGHT: Prototyping / certification ───────────
    (730, 290, 160, 54, "Prototyping",       "FDM · SLA · CNC",          COL_DIGITAL),  # 8
    (730, 490, 160, 54, "Certification",     "SHA-256 · CDM · OTS",      COL_CERT),     # 9

    # ── RIGHT: Exhibition / output ─────────────────────────
    (900, 155, 130, 46, "Physical\nExhibition",  "", COL_OUTPUT),   # 10
    (900, 270, 130, 46, "XR / VR\nExhibition",   "", COL_OUTPUT),   # 11
    (900, 380, 130, 46, "Installation",           "", COL_OUTPUT),   # 12
    (900, 490, 130, 46, "Digital /\nNFT / CDM",  "", COL_OUTPUT),   # 13
]

# Arrows: (from_index, to_index, label)
# Node indices: 0=ManualPainting 1=ManualSculpture 2=PhysicalObject
#   3=Scanning 4=DigitalPainting 5=AIGeneration 6=3DModeling 7=DigitalSculpture
#   8=Prototyping 9=Certification 10=PhysicalExh 11=XRExh 12=Installation 13=DigitalNFT
ARROWS = [
    (0, 3, "scan"),           # Manual Painting → Scanning
    (0, 4, "digitize"),       # Manual Painting → Digital Painting
    (0, 5, "AI expand"),      # Manual Painting → AI Generation
    (1, 3, "scan"),           # Manual Sculpture → Scanning
    (1, 6, "import"),         # Manual Sculpture → 3D Modeling
    (1, 7, "sculpt"),         # Manual Sculpture → Digital Sculpture
    (2, 3, "scan"),           # Physical Object → Scanning
    (3, 5, "img2img"),        # Scanning → AI Generation
    (3, 6, "mesh"),           # Scanning → 3D Modeling
    (3, 7, "retopo"),         # Scanning → Digital Sculpture
    (4, 5, "hybrid"),         # Digital Painting → AI Generation
    (4, 10, ""),              # Digital Painting → Physical Exhibition
    (4, 11, ""),              # Digital Painting → XR Exhibition
    (5, 4, "inpaint/\noutpaint"),  # AI → Digital Painting (feedback, dashed)
    (5, 8, "print"),          # AI → Prototyping
    (5, 13, ""),              # AI → Digital / NFT
    (5, 9, "certify"),        # AI → Certification
    (6, 8, "export STL"),     # 3D Modeling → Prototyping
    (6, 9, "certify"),        # 3D Modeling → Certification
    (7, 8, "export STL"),     # Digital Sculpture → Prototyping
    (7, 9, "certify"),        # Digital Sculpture → Certification
    (7, 11, "VR"),            # Digital Sculpture → XR/VR Exhibition
    (8, 10, ""),              # Prototyping → Physical Exhibition
    (8, 12, "install"),       # Prototyping → Installation
    (9, 13, ""),              # Certification → Digital / NFT
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


def _tspan_lines(x, y, lines, size, fill, weight, anchor, line_height=16):
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


def _arrow_line(x1, y1, x2, y2, label="", color=COL_ARROW, dash=""):
    dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
    line = (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="1.4" marker-end="url(#arr)" {dash_attr}/>'
    )
    parts = [line]
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        parts.append(_text(mx, my, label, size=9, fill=COL_SUB))
    return "\n".join(parts)


def _node_edge(ni, nj, nodes, direction="right"):
    """Return (x1,y1) on edge of node ni toward node nj."""
    cx1, cy1, w1, h1 = nodes[ni][:4]
    cx2, cy2, w2, h2 = nodes[nj][:4]
    dx, dy = cx2 - cx1, cy2 - cy1

    # Choose exit side
    if abs(dx) >= abs(dy):
        # horizontal dominant
        if dx > 0:
            x1 = cx1 + w1 / 2
            x2 = cx2 - w2 / 2
        else:
            x1 = cx1 - w1 / 2
            x2 = cx2 + w2 / 2
        # vertical offset proportional
        frac = dy / (abs(dx) + 1)
        y1 = cy1 + frac * h1 / 2 * 0.5
        y2 = cy2 - frac * h2 / 2 * 0.5
    else:
        # vertical dominant
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
    lines.append(_text(W / 2, 34, "Hybrid Workflow — Technical Process", size=16,
                       fill=COL_TITLE, weight="bold"))
    lines.append(_text(W / 2, 56, "Chapter 5 · Art Between Matter and Code · Gianpiero Moioli · Apress 2025",
                       size=10, fill=COL_SUB))

    # Column headers
    col_labels = [
        (110, 100, "Physical / Manual"),
        (340, 100, "Acquisition"),
        (530, 100, "Digital Processing"),
        (730, 100, "Fabrication &\nCertification"),
        (900, 100, "Exhibition /\nOutput"),
    ]
    for cx, cy, lbl in col_labels:
        for i, part in enumerate(lbl.split("\n")):
            lines.append(_text(cx, cy + i * 14, part, size=10, fill=COL_SUB, weight="bold"))

    # Arrows (draw before nodes so nodes sit on top)
    node_data = [(n[0], n[1], n[2], n[3]) for n in NODES]
    for (fi, ti, lbl) in ARROWS:
        x1, y1, x2, y2 = _node_edge(fi, ti, node_data)
        # Feedback arrow: AI ← Digital Painting → dashed
        dash = "4,3" if fi == 5 and ti == 4 else ""
        lines.append(_arrow_line(x1, y1, x2, y2, label=lbl, dash=dash))

    # Nodes
    for (cx, cy, w, h, label, sublabel, color) in NODES:
        lines.append(_box(cx, cy, w, h, color))
        label_lines = label.split("\n")
        if sublabel:
            # label on top, sublabel below
            label_y = cy - 7 if len(label_lines) == 1 else cy - 12
            if len(label_lines) == 1:
                lines.append(_text(cx, label_y, label, size=11, fill="white", weight="bold"))
            else:
                lines.append(_tspan_lines(cx, label_y, label_lines, 11, "white", "bold", "middle"))
            lines.append(_text(cx, cy + 10, sublabel, size=9, fill="rgba(255,255,255,0.82)"))
        else:
            # label only, centered
            if len(label_lines) > 1:
                lines.append(_tspan_lines(cx, cy, label_lines, 11, "white", "bold", "middle"))
            else:
                lines.append(_text(cx, cy, label, size=11, fill="white", weight="bold"))

    # Legend
    legend_items = [
        (COL_MANUAL,  "Physical / Manual"),
        (COL_DIGITAL, "Digital Tools"),
        (COL_AI,      "AI / Generative"),
        (COL_CERT,    "Certification (CDM)"),
        (COL_OUTPUT,  "Exhibition / Output"),
    ]
    lx, ly = PAD, H - 64
    lines.append(
        f'<rect x="{lx}" y="{ly}" width="310" height="52" rx="6" fill="{COL_LEGEND_BG}" '
        f'opacity="0.9" stroke="#ddd" stroke-width="1"/>'
    )
    lines.append(_text(lx + 155, ly + 11, "Legend", size=9, fill=COL_SUB, weight="bold"))
    for i, (col, lbl) in enumerate(legend_items):
        row, col_i = divmod(i, 3)
        x = lx + 12 + col_i * 102
        y = ly + 24 + row * 16
        lines.append(f'<rect x="{x}" y="{y - 5}" width="10" height="10" rx="2" fill="{col}"/>')
        lines.append(_text(x + 14, y, lbl, size=8.5, fill=COL_LABEL, anchor="start"))

    # Note
    note = "Dashed arrow = bidirectional feedback (AI ⟷ Digital Painting)"
    lines.append(_text(W - PAD, H - 14, note, size=8.5, fill=COL_SUB, anchor="end"))

    lines.append("</svg>")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Hybrid Workflow diagram SVG")
    parser.add_argument("--output", default=".", help="Output folder (default: current directory)")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / OUTPUT_FILENAME

    svg_content = build_svg()
    out_path.write_text(svg_content, encoding="utf-8")
    print(f"[hybrid_workflow_diagram] Saved -> {out_path.resolve()}")
    print("  Open in any browser or vector editor.")


if __name__ == "__main__":
    main()
