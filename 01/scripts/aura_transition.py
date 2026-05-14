"""
aura_transition.py — Aura & Reproducibility Diagram
=====================================================
Chapter 1 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Programmatic companion to images/ref_aura_transition_diagram.svg.

Generates the diagram as a standalone SVG file — no external libraries needed,
runs with any Python 3.x installation (including the Python bundled in Blender).

Walter Benjamin argued that mechanical reproduction strips the artwork of its
"aura" — the sense of unique presence tied to a specific place and time.
This diagram maps five phases from handmade uniqueness to AI-generated work,
plotting Aura and Reproducibility as two crossing curves.

Usage:
    Double-click  run_aura_transition.bat   (Windows — recommended)
    or: python aura_transition.py
    or: python aura_transition.py --output path/to/folder

Output:
    ref_aura_transition_diagram.svg   (vector, opens in any browser)
"""

import argparse
import os
import sys

# ── DATA ──────────────────────────────────────────────────────────────────────
PHASES = [
    {
        "label":  "Handmade\nObject",
        "year":   "pre-1800",
        "aura":   1.00,
        "repro":  0.00,
        "color":  "#7B5C3A",
        "note":   "Original, unique,\nplace-bound",
    },
    {
        "label":  "Cast /\nMould",
        "year":   "1800-1880",
        "aura":   0.75,
        "repro":  0.22,
        "color":  "#A07850",
        "note":   "Limited series;\naura partially\npreserved",
    },
    {
        "label":  "Mechanical\nReproduction",
        "year":   "1880-1960",
        "aura":   0.30,
        "repro":  0.70,
        "color":  "#4A6FA5",
        "note":   "Benjamin's\nwatershed:\nphoto, print, film",
    },
    {
        "label":  "Digital /\nParametric",
        "year":   "1960-2020",
        "aura":   0.20,
        "repro":  0.95,
        "color":  "#2E8B57",
        "note":   "Infinite copies;\nNFT / blockchain\nre-aura",
    },
    {
        "label":  "AI-Generated",
        "year":   "2020 onwards",
        "aura":   0.55,
        "repro":  1.00,
        "color":  "#8B2E8B",
        "note":   "Generative aura:\nunique process,\ninfinite output",
    },
]
# ──────────────────────────────────────────────────────────────────────────────

W, H    = 900, 480
PAD_L   = 60
PAD_R   = 30
PAD_T   = 70
PAD_B   = 110
CHART_W = W - PAD_L - PAD_R
CHART_H = H - PAD_T - PAD_B


def val_to_xy(phase_index, value, n_phases):
    x = PAD_L + phase_index * CHART_W / (n_phases - 1)
    y = PAD_T + (1.0 - value) * CHART_H
    return x, y


def polyline_points(values, n):
    return " ".join(
        f"{val_to_xy(i, v, n)[0]:.1f},{val_to_xy(i, v, n)[1]:.1f}"
        for i, v in enumerate(values)
    )


def xe(s):
    """Escape special XML characters."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_text(x, y, text, size=11, color="#333", anchor="middle",
             bold=False, italic=False, dy=0):
    weight = "bold" if bold else "normal"
    style  = "italic" if italic else "normal"
    lines  = text.split("\n")
    if len(lines) == 1:
        return (
            f'<text x="{x:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" '
            f'font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" font-style="{style}">'
            f'{xe(text)}</text>'
        )
    parts = []
    for k, line in enumerate(lines):
        dy_val = 0 if k == 0 else size * 1.3
        parts.append(f'<tspan x="{x:.1f}" dy="{dy_val:.1f}">{xe(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" fill="{color}" '
        f'font-weight="{weight}" font-style="{style}">'
        + "".join(parts) + "</text>"
    )


def build_svg():
    n      = len(PHASES)
    auras  = [p["aura"]  for p in PHASES]
    repros = [p["repro"] for p in PHASES]

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Georgia, serif">'
    )
    out.append(f'<rect width="{W}" height="{H}" fill="#FAFAF7"/>')
    out.append(
        f'<rect x="{PAD_L}" y="{PAD_T}" width="{CHART_W}" height="{CHART_H}" '
        f'fill="none" stroke="#DDDDDD" stroke-width="1"/>'
    )

    # grid lines
    for val, label in [(0.0, "0"), (0.25, "0.25"), (0.5, "0.50"),
                       (0.75, "0.75"), (1.0, "1.00")]:
        _, gy = val_to_xy(0, val, n)
        out.append(
            f'<line x1="{PAD_L}" y1="{gy:.1f}" '
            f'x2="{PAD_L + CHART_W}" y2="{gy:.1f}" '
            f'stroke="#EEEEEE" stroke-width="1"/>'
        )
        out.append(svg_text(PAD_L - 6, gy + 4, label, size=9,
                            color="#888", anchor="end"))

    # Benjamin threshold
    bx, _ = val_to_xy(2, 0, n)
    out.append(
        f'<line x1="{bx:.1f}" y1="{PAD_T}" '
        f'x2="{bx:.1f}" y2="{PAD_T + CHART_H}" '
        f'stroke="#4A6FA5" stroke-width="1" stroke-dasharray="4 3" opacity="0.6"/>'
    )
    out.append(svg_text(bx + 6, PAD_T + 10, "Benjamin\nthreshold",
                        size=8, color="#4A6FA5", anchor="start", italic=True))

    # area fills
    aura_pts  = polyline_points(auras,  n)
    repro_pts = polyline_points(repros, n)
    x0, _ = val_to_xy(0,     0, n)
    x1, _ = val_to_xy(n - 1, 0, n)
    bot   = PAD_T + CHART_H
    out.append(
        f'<polygon points="{aura_pts} {x1:.1f},{bot} {x0:.1f},{bot}" '
        f'fill="#7B5C3A" opacity="0.08"/>'
    )
    out.append(
        f'<polygon points="{repro_pts} {x1:.1f},{bot} {x0:.1f},{bot}" '
        f'fill="#2E5D8B" opacity="0.07"/>'
    )

    # curves
    out.append(
        f'<polyline points="{aura_pts}" fill="none" '
        f'stroke="#7B5C3A" stroke-width="2.5" stroke-linejoin="round"/>'
    )
    out.append(
        f'<polyline points="{repro_pts}" fill="none" '
        f'stroke="#2E5D8B" stroke-width="2" stroke-dasharray="6 3" '
        f'stroke-linejoin="round"/>'
    )

    # dots, labels, notes
    note_offsets = [-52, -52, 28, -52, 28]
    for i, p in enumerate(PHASES):
        ax, ay = val_to_xy(i, p["aura"],  n)
        rx, ry = val_to_xy(i, p["repro"], n)
        c = p["color"]

        out.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="6" '
                   f'fill="{c}" stroke="white" stroke-width="1.5"/>')
        sq = 5
        out.append(f'<rect x="{rx - sq:.1f}" y="{ry - sq:.1f}" '
                   f'width="{sq * 2}" height="{sq * 2}" '
                   f'fill="{c}" stroke="white" stroke-width="1.5"/>')

        ny = ay + note_offsets[i]
        out.append(
            f'<line x1="{ax:.1f}" y1="{ay - 7:.1f}" '
            f'x2="{ax:.1f}" y2="{ny + 2:.1f}" '
            f'stroke="#BBBBBB" stroke-width="0.8"/>'
        )
        out.append(svg_text(ax, ny, p["note"], size=8, color="#555"))

        label_y = PAD_T + CHART_H + 18
        out.append(svg_text(ax, label_y, p["label"],
                            size=9.5, color=c, bold=True))
        out.append(svg_text(ax, label_y + 26, p["year"],
                            size=8, color="#777", italic=True))

    # legend
    lx, ly = W - PAD_R - 220, PAD_T + 10
    out.append(
        f'<rect x="{lx - 8}" y="{ly - 8}" width="220" height="52" '
        f'rx="4" fill="white" stroke="#DDDDDD" stroke-width="1" opacity="0.85"/>'
    )
    out.append(
        f'<line x1="{lx}" y1="{ly + 8}" x2="{lx + 30}" y2="{ly + 8}" '
        f'stroke="#7B5C3A" stroke-width="2.5"/>'
    )
    out.append(
        f'<circle cx="{lx + 15}" cy="{ly + 8}" r="5" '
        f'fill="#7B5C3A" stroke="white" stroke-width="1.5"/>'
    )
    out.append(svg_text(lx + 36, ly + 12, "Aura (presence / uniqueness)",
                        size=9, color="#333", anchor="start"))
    out.append(
        f'<line x1="{lx}" y1="{ly + 28}" x2="{lx + 30}" y2="{ly + 28}" '
        f'stroke="#2E5D8B" stroke-width="2" stroke-dasharray="6 3"/>'
    )
    sq = 4
    out.append(
        f'<rect x="{lx + 11}" y="{ly + 24}" width="{sq * 2}" height="{sq * 2}" '
        f'fill="#2E5D8B" stroke="white" stroke-width="1.5"/>'
    )
    out.append(svg_text(lx + 36, ly + 32, "Reproducibility / circulation",
                        size=9, color="#333", anchor="start"))

    # title
    out.append(svg_text(W / 2, 22,
                        "Aura and Reproducibility - from Handmade Object to AI-Generated Work",
                        size=14, color="#2A2A2A", bold=True))
    out.append(svg_text(W / 2, 42,
                        "after Walter Benjamin, Das Kunstwerk im Zeitalter seiner technischen Reproduzierbarkeit (1935)",
                        size=9, color="#666", italic=True))

    # copyright
    out.append(svg_text(
        PAD_L, H - 8,
        "2025 Gianpiero Moioli - CC BY-NC 4.0 - Art Between Matter and Code, Apress / Springer",
        size=7, color="#AAAAAA", anchor="start"
    ))

    out.append("</svg>")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Generate the aura/reproducibility diagram as SVG."
    )
    parser.add_argument("--output", default=".",
                        help="Output directory (default: current directory)")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    path = os.path.join(args.output, "ref_aura_transition_diagram.svg")

    with open(path, "w", encoding="utf-8") as f:
        f.write(build_svg())

    abs_path = os.path.abspath(path)
    print(f"[aura_transition] Saved -> {abs_path}")
    print("  Open the SVG in any browser to view the diagram.")

    try:
        import subprocess
        import platform
        if platform.system() == "Windows":
            os.startfile(abs_path)
        elif platform.system() == "Darwin":
            subprocess.call(["open", abs_path])
        else:
            subprocess.call(["xdg-open", abs_path])
    except Exception:
        pass


if __name__ == "__main__":
    main()
