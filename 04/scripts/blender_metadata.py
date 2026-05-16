"""
blender_metadata.py — Standardised Metadata via Blender Custom Properties
==========================================================================
Chapter 4 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §4.2.2 — "Metadata in 3D Files".

Adds a standardised block of Custom Properties to the active Blender scene,
functioning as an informal internal metadata record (author, title, date,
license, version, notes). The metadata is visible in the Properties panel
(Scene Properties > Custom Properties) and survives .blend save/export.

This is the first level of certification described in §4.2.2:
  Level 1 — Internal / Informal  (this script)
  Level 2 — External / Certified (SHA-256 + CDM via certify_asset.py)
  Level 3 — On-chain / Permanent (OpenTimestamps, IPFS, NFT)

Usage:
    Double-click  run_blender_metadata.bat   (Windows — recommended)
    or: Blender → Scripting workspace → Open → Alt+P
    or: blender --python blender_metadata.py
"""

import bpy
import datetime
import os

# ── CONFIG — edit this block ───────────────────────────────────────────────
AUTHOR      = "Gianpiero Moioli"
TITLE       = "Untitled Work"
DATE        = datetime.date.today().isoformat()   # e.g. "2025-01-01"
LICENSE     = "CC BY-NC 4.0"                      # or "CC0", "CC BY", "All Rights Reserved"
VERSION     = "1.0"
CHAPTER_REF = "Art Between Matter and Code — Chapter 4"
NOTES       = ""   # free-text: technique, exhibition, edition info, etc.
# ──────────────────────────────────────────────────────────────────────────



def set_metadata(scene, data: dict) -> None:
    """Write key/value pairs as Custom Properties on a Blender scene."""
    for key, value in data.items():
        scene[key] = value
        id_props = scene.id_properties_ui(key)
        id_props.update(description=f"Artwork metadata: {key}")


def main():
    """Write the metadata block to the current scene. Run with Alt+P."""
    scene = bpy.context.scene

    metadata = {
        "meta_author":      AUTHOR,
        "meta_title":       TITLE,
        "meta_date":        DATE,
        "meta_license":     LICENSE,
        "meta_version":     VERSION,
        "meta_chapter_ref": CHAPTER_REF,
        "meta_notes":       NOTES,
    }

    set_metadata(scene, metadata)

    print("\n[blender_metadata] Metadata written to scene Custom Properties:")
    for key, value in metadata.items():
        print(f"  {key}: {value!r}")
    print()
    print("  View: Properties panel → Scene → Custom Properties")
    print("  These properties are saved inside the .blend file.")
    print()
    print("  For certified external metadata, run:")
    print(f'  python certify_asset.py your_file.blend --author "{AUTHOR}"')


if __name__ == "__main__":
    main()
