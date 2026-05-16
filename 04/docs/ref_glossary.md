# Glossary — Chapter 4
## Uniqueness, Identity, and Digital Certification

> Key terms for *Art Between Matter and Code* · Gianpiero Moioli · Apress 2025

---

**Aura**
Walter Benjamin's term for the unique quality of an original artwork — its embeddedness in a specific place, time, and history. In Benjamin's argument, mechanical reproduction destroys this quality. The chapter traces how digital tools attempt to reconstruct it through metadata and cryptographic certification.

**Hic et nunc**
Latin: *here and now*. Benjamin's phrase for the irreducible singularity of an original work — its presence at a particular location at a particular moment. The foundation of aura.

**NFT (Non-Fungible Token)**
A cryptographic token recorded on a blockchain that certifies ownership of a unique digital asset. Unlike a cryptocurrency coin (fungible — any coin equals any other), an NFT is non-interchangeable: it represents a specific item. Owning an NFT means owning the certified record of ownership, not necessarily the file itself or its copyright.

**Fungible / Non-Fungible**
A fungible asset is interchangeable: one euro is equivalent to any other euro. A non-fungible asset is unique: owning an NFT of a specific artwork is not equivalent to owning an NFT of a different artwork. The distinction is fundamental to understanding how blockchain certificates work.

**Blockchain**
A distributed, append-only ledger shared across a network of computers. Each block contains a batch of transactions and a cryptographic hash of the previous block, making the chain tamper-evident. No single authority controls it. Used for NFTs to create an unalterable ownership history.

**Smart Contract**
Self-executing code stored on a blockchain that automatically enforces agreed-upon rules when conditions are met. In the art market: can automate royalty payments to artists on every secondary sale (see ERC-2981 standard), eliminating intermediaries.

**SHA-256**
A cryptographic hash function that produces a unique 64-character hexadecimal fingerprint for any file. Change a single pixel and the hash changes completely. Used to certify that a digital artwork has not been altered since certification. Part of the CDM protocol described in Appendix A.

**CDM (Certified Digital Manifest)**
The certification format proposed in the chapter: a JSON document recording filename, SHA-256 hash, timestamp, tool used, and a chain of previous hashes for a complete audit trail of transformations. See `certification_protocol.md` for the full schema.

**OpenTimestamps**
An open-source protocol that anchors a SHA-256 hash to the Bitcoin blockchain without creating a full NFT. Provides a verifiable, decentralized timestamp: proof that a file existed in a specific form at a specific moment. Low cost, no transaction fees.

**IPFS (InterPlanetary File System)**
A peer-to-peer distributed file storage protocol. Files are addressed by their content hash (not by server location), so a file's address changes if its content changes. Used to store NFT assets in a decentralised way, reducing dependence on a single server that could go offline.

**Arweave**
A decentralised permanent storage network. Unlike IPFS (which requires ongoing pinning), Arweave stores data permanently through a one-time payment. Recommended for long-term preservation of certified digital artworks.

**Proof-of-Work / Proof-of-Stake**
Two mechanisms for validating blockchain transactions. Proof-of-Work (PoW, used by Bitcoin) requires enormous computational energy. Proof-of-Stake (PoS, adopted by Ethereum in 2022) uses negligible energy by comparison. Relevant to artists concerned about the environmental footprint of NFT minting.

**Disintermediation**
The removal of traditional intermediaries (galleries, auction houses, notaries) from transactions. Blockchain enables artists to sell directly to collectors with ownership automatically recorded, though it introduces new intermediaries (platforms, wallets, gas fees).

**Metadata**
Structured data embedded in or attached to a file that describes its content, origin, and history. In Blender: Custom Properties. In images: EXIF/XMP fields. In certified workflows: a CDM JSON file. Metadata is the "digital identity document" of an artwork.

**Post-authorship**
A condition in which authorship is distributed between multiple agents — human designer, generative algorithm, and interacting audience. The artist defines the system and its possibility space; specific outcomes emerge from execution. Related to Roland Barthes' "death of the author" (1967).

**Art Coefficient**
Marcel Duchamp's term (*The Creative Act*, 1957) for the gap between the artist's intention and the work as received by the spectator. The spectator's interpretation completes the work, making them a co-author. Cited in the chapter as a historical anticipation of distributed authorship in generative and NFT art.

**Creative Commons (CC)**
A set of standardised public licenses allowing creators to grant specific rights to the public while retaining others. Ranges from CC0 (complete public domain dedication) to CC BY-NC-ND (attribution required, no commercial use, no derivatives). See the chapter for the full comparative table.

**ERC-2981**
An Ethereum token standard that embeds royalty information directly into an NFT contract, enabling automatic royalty payments to the original artist on every secondary market sale.

**Generative Aura**
A term introduced in the chapter to describe the paradox of AI-generated work: reproducibility reaches its maximum (infinite output) while aura partially recovers, because each generation is an unrepeatable process tied to a specific prompt, model state, and moment. See the aura/reproducibility diagram (`scripts/ref_aura_transition_diagram.svg`).
