"""
certify_asset.py — Certified Digital Manifest (CDM) Generator
==============================================================
Chapter 4 · Art Between Matter and Code · Gianpiero Moioli
Apress / Springer Nature, 2025 · CC BY-NC 4.0

Companion to §4.3.4 and Appendix A.

Computes a SHA-256 fingerprint for any digital file and writes a
Certified Digital Manifest (.cdm.json) alongside it. CDMs can be
chained to create a tamper-evident audit trail across all versions
of an artwork.

No external libraries required — runs with any Python 3.x installation.

Usage:
    python certify_asset.py  artwork.blend
    python certify_asset.py  artwork.blend  --author "Gianpiero Moioli"
    python certify_asset.py  artwork.blend  --author "G. Moioli"  \\
                             --tool "Blender 5.x"  \\
                             --notes "Final geometry, before texturing" \\
                             --previous artwork.blend.cdm.json

Output:
    artwork.blend.cdm.json   (written next to the source file)
"""

import argparse
import datetime
import hashlib
import json
import os
import sys


# ── CONFIG ────────────────────────────────────────────────────────────────────
DEFAULT_AUTHOR = "Gianpiero Moioli"
DEFAULT_TOOL   = "Python 3.x"
CDM_VERSION    = "CDM-1.0"
# ──────────────────────────────────────────────────────────────────────────────


def sha256_file(path: str) -> str:
    """Return the SHA-256 hex digest of a file, reading in 64 KB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def create_cdm(
    file_path: str,
    author: str,
    tool: str,
    notes: str = "",
    previous_cdm_path: str | None = None,
) -> dict:
    """Build and return the CDM dictionary."""
    previous_hash = None
    if previous_cdm_path:
        if not os.path.exists(previous_cdm_path):
            print(f"[WARNING] Previous CDM not found: {previous_cdm_path}")
        else:
            previous_hash = sha256_file(previous_cdm_path)
            print(f"[certify] Chaining from: {previous_cdm_path}")
            print(f"          previous_hash: {previous_hash[:16]}…")

    return {
        "id_version":    CDM_VERSION,
        "file_name":     os.path.basename(file_path),
        "sha256_hash":   sha256_file(file_path),
        "timestamp_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "author":        author,
        "tool":          tool,
        "previous_hash": previous_hash,
        "notes":         notes,
    }


def write_cdm(file_path: str, cdm: dict) -> str:
    """Write the CDM as a JSON file next to the source file."""
    cdm_path = file_path + ".cdm.json"
    with open(cdm_path, "w", encoding="utf-8") as f:
        json.dump(cdm, f, indent=2, ensure_ascii=False)
    return cdm_path


def verify_cdm(file_path: str, cdm_path: str) -> bool:
    """Re-compute the hash and compare it against the CDM record."""
    with open(cdm_path, "r", encoding="utf-8") as f:
        cdm = json.load(f)
    actual = sha256_file(file_path)
    return actual == cdm.get("sha256_hash", "")


def main():
    parser = argparse.ArgumentParser(
        description="Generate or verify a Certified Digital Manifest (CDM)."
    )
    parser.add_argument("file", help="File to certify")
    parser.add_argument(
        "--author",   default=DEFAULT_AUTHOR,
        help=f'Author name (default: "{DEFAULT_AUTHOR}")'
    )
    parser.add_argument(
        "--tool",     default=DEFAULT_TOOL,
        help=f'Software used (default: "{DEFAULT_TOOL}")'
    )
    parser.add_argument(
        "--notes",    default="",
        help="Free-text description of this version"
    )
    parser.add_argument(
        "--previous", default=None, metavar="CDM_PATH",
        help="Path to the previous .cdm.json file (enables chaining)"
    )
    parser.add_argument(
        "--verify",   action="store_true",
        help="Verify an existing CDM instead of creating a new one"
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}")
        sys.exit(1)

    # ── VERIFY MODE ───────────────────────────────────────────────────────────
    if args.verify:
        cdm_path = args.file + ".cdm.json"
        if not os.path.exists(cdm_path):
            print(f"[ERROR] No CDM found at: {cdm_path}")
            sys.exit(1)
        ok = verify_cdm(args.file, cdm_path)
        if ok:
            print(f"[OK] Hash matches — file is unaltered since certification.")
        else:
            print(f"[FAIL] Hash mismatch — file has been modified!")
            sys.exit(2)
        return

    # ── CERTIFY MODE ──────────────────────────────────────────────────────────
    print(f"[certify] File   : {args.file}")
    cdm      = create_cdm(args.file, args.author, args.tool,
                          args.notes, args.previous)
    cdm_path = write_cdm(args.file, cdm)

    print(f"[certify] SHA-256: {cdm['sha256_hash']}")
    print(f"[certify] Time   : {cdm['timestamp_utc']}")
    print(f"[certify] CDM    : {os.path.abspath(cdm_path)}")
    print()
    print("  Next steps:")
    print("  1. Stamp with OpenTimestamps:  ots stamp " + os.path.basename(cdm_path))
    print("  2. Upload to IPFS/Arweave for permanent storage.")
    print("  3. For a new version: python certify_asset.py <file> "
          "--previous " + os.path.basename(cdm_path))


if __name__ == "__main__":
    main()
