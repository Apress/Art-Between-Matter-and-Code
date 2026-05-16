# Reproducible Digital Certification Protocol
## Appendix A — Chapter 4

> Practical reference for *Art Between Matter and Code* · Gianpiero Moioli · Apress 2025  
> Full theoretical context: §4.3.4 of the chapter.

---

## Overview

This protocol assigns a verifiable, tamper-evident identity to any digital artwork file — 3D model, render, script, or image. It is based on:

- **SHA-256** cryptographic hashing (fingerprint of the file's exact content)
- **CDM** (Certified Digital Manifest) — a JSON record chaining all transformations
- **OpenTimestamps** — free, Bitcoin-anchored timestamp (no NFT required)
- **IPFS / Arweave** — decentralised storage for long-term persistence

No blockchain account, no NFT, no gas fees are required for basic certification. The protocol scales from a local studio practice to full on-chain inscription.

---

## Step 1 — Compute the SHA-256 Hash

The hash is a 64-character hexadecimal string that uniquely identifies the file's content. Any modification — even a single byte — produces a completely different hash.

**Command line (Windows / macOS / Linux):**

```bash
# Windows (PowerShell)
Get-FileHash artwork.blend -Algorithm SHA256

# macOS / Linux
shasum -a 256 artwork.blend
```

**Python:**

```python
import hashlib

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

print(sha256_file("artwork.blend"))
```

---

## Step 2 — Create the Certified Digital Manifest (CDM)

The CDM is a JSON file that records the file's identity and links it to its transformation history. Save it alongside the artwork with the naming convention `<filename>.cdm.json`.

### CDM Schema

```json
{
  "id_version": "CDM-1.0",
  "file_name": "artwork.blend",
  "sha256_hash": "<64-character hex string>",
  "timestamp_utc": "2025-01-01T12:00:00Z",
  "author": "Gianpiero Moioli",
  "tool": "Blender 5.x",
  "previous_hash": null,
  "notes": "Initial certification — base geometry complete"
}
```

### CDM Fields

| Field | Type | Description |
|-------|------|-------------|
| `id_version` | string | Protocol version — always `"CDM-1.0"` |
| `file_name` | string | Exact filename including extension |
| `sha256_hash` | string | SHA-256 hash of the file at this state |
| `timestamp_utc` | string | ISO 8601 UTC timestamp |
| `author` | string | Author name or public key |
| `tool` | string | Software used to create/modify the file |
| `previous_hash` | string \| null | Hash of the previous CDM (creates audit chain); `null` for first entry |
| `notes` | string | Free-text description of this version |

### Chaining CDMs (Audit Trail)

Each new version of the artwork gets a new CDM. The `previous_hash` field references the hash of the **previous CDM file** (not the artwork), creating a tamper-evident chain:

```
v1 CDM (previous_hash: null)
  └─ v2 CDM (previous_hash: sha256 of v1 CDM)
       └─ v3 CDM (previous_hash: sha256 of v2 CDM)
```

If any CDM in the chain is altered, all subsequent hashes become invalid.

### Python: Generate a CDM automatically

```python
import hashlib, json, datetime, os

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def create_cdm(file_path, author, tool, notes="", previous_cdm_path=None):
    previous_hash = None
    if previous_cdm_path and os.path.exists(previous_cdm_path):
        previous_hash = sha256_file(previous_cdm_path)

    cdm = {
        "id_version":    "CDM-1.0",
        "file_name":     os.path.basename(file_path),
        "sha256_hash":   sha256_file(file_path),
        "timestamp_utc": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "author":        author,
        "tool":          tool,
        "previous_hash": previous_hash,
        "notes":         notes,
    }

    cdm_path = file_path + ".cdm.json"
    with open(cdm_path, "w", encoding="utf-8") as f:
        json.dump(cdm, f, indent=2, ensure_ascii=False)

    print(f"CDM written → {cdm_path}")
    print(f"SHA-256: {cdm['sha256_hash']}")
    return cdm_path

# Example usage
create_cdm(
    file_path="artwork.blend",
    author="Gianpiero Moioli",
    tool="Blender 5.x",
    notes="Final geometry, before texturing",
    previous_cdm_path=None   # or path to previous CDM
)
```

---

## Step 3 — Timestamp with OpenTimestamps (optional but recommended)

OpenTimestamps anchors the hash to the Bitcoin blockchain for free. This provides a decentralised, verifiable proof that the file existed in this exact form at this exact moment — without creating an NFT.

```bash
# Install
pip install opentimestamps-client

# Stamp the CDM file (not the artwork — the CDM contains the artwork's hash)
ots stamp artwork.blend.cdm.json

# This creates: artwork.blend.cdm.json.ots
# Verify later (after Bitcoin confirmation, ~1 hour):
ots verify artwork.blend.cdm.json.ots
```

The `.ots` file is the proof. Store it with the CDM and the artwork.

---

## Step 4 — Decentralised Storage (optional)

For long-term persistence independent of any single server:

| Option | Description | Cost |
|--------|-------------|------|
| **IPFS** | Peer-to-peer content-addressed storage. Requires ongoing pinning (e.g., Pinata, web3.storage) | Low / free tier available |
| **Arweave** | Permanent storage via one-time payment. No ongoing fees. | ~$0.01–$0.10 per MB |

Upload the **artwork file + CDM + .ots timestamp** as a bundle. Record the IPFS CID or Arweave transaction ID in the CDM's `notes` field.

---

## Step 5 — Optional On-Chain Inscription

If full blockchain inscription is desired, recommended low-carbon options:

| Chain | Mechanism | Notes |
|-------|-----------|-------|
| **Ethereum** (post-Merge 2022) | NFT via ERC-721/ERC-1155 | Proof-of-Stake, ~99.95% energy reduction vs. PoW |
| **Tezos** | NFT via FA2 standard | Native PoS, very low fees |
| **Polygon** | NFT (Ethereum L2) | Near-zero gas fees |
| **Bitcoin** | Ordinals inscription | Permanent, censorship-resistant |

Platforms: SuperRare, Foundation, Zora, Manifold (Ethereum); objkt.com (Tezos).

---

## Verification Checklist

To verify a certified work:

- [ ] Recompute SHA-256 of the file — must match `sha256_hash` in the CDM
- [ ] Verify `previous_hash` chain — each CDM's hash must match the next CDM's `previous_hash`
- [ ] Verify OpenTimestamps proof: `ots verify artwork.blend.cdm.json.ots`
- [ ] If IPFS: confirm the CID resolves to the same file
- [ ] If on-chain: confirm the token metadata points to the correct CDM hash

---

*For the theoretical context — why this protocol matters, and how it relates to Benjamin's aura and NFT logic — see §4.3.4 of the chapter.*
