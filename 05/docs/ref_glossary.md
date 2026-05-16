# Chapter 5 — Glossary of Key Terms

> **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025  
> Reference companion to Chapter 5: *States of Transformation: Painting, Sculpture, and Digital Expansion*

---

## A

**AI Upscaling**  
Algorithms (e.g., Real-ESRGAN, Topaz Gigapixel AI, SwinIR) that enlarge raster images beyond their original resolution using neural networks trained on high-quality image pairs. Controlled tests with Topaz Gigapixel AI v8.4.4 at 4× enlargement yield SSIM > 0.95, confirming suitability for monumental prints from modest source files. Open-source equivalents: Real-ESRGAN, SwinIR.

**Augmented Imagination**  
A conceptual trajectory identified in §5.1: the expansion of cognitive and aesthetic possibilities through algorithmic systems, which act as catalysts for unforeseen forms, speculative narratives, and symbolic landscapes beyond individual human invention.

---

## C

**CDM — Certified Digital Manifest**  
JSON record containing the SHA-256 fingerprint of a digital file, timestamp, author, and optional chain link to a previous version. Defined in §4.3.4 (Chapter 4). In Chapter 5 it appears as the anchoring mechanism for the Hybrid Painting workflow: final composites are archived as PNG or GLTF/GLB with a CDM providing tamper-evident provenance. See `certify_asset.py` in the Chapter 4 scripts.

**ComfyUI**  
Node-based graphical interface for Stable Diffusion (Python 3.11.9, PyTorch 2.4.1). Allows fully customizable, reproducible generation pipelines through visual node graphs. Used in Chapter 5 for img2img, inpainting, ControlNet, and OpenPose workflows. Free, open-source.

**ControlNet**  
Extension for Stable Diffusion that conditions generation on structural maps (edges, poses, depth) rather than text alone, allowing structural continuity with source material. OpenPose variant reads body keypoints to guide figure generation.

---

## D

**DreamBooth**  
Fine-tuning technique for Stable Diffusion that teaches the model a new visual concept (face, object, style) from a small dataset of reference images. Used in Chapter 5 to personalize AI outputs to the artist's own style or subjects.

**Digital Sculpture**  
Three-dimensional form created in software rather than physical material, manipulated through polygonal modeling, subdivision surfaces, sculpting brushes (Blender, ZBrush), or VR interfaces (Gravity Sketch). Replicates additive and subtractive sculptural logic in virtual space while granting infinite undo, gravity-free forms, and precise scaling.

---

## E

**Expanded Artwork**  
Concept proposed in §5.3.1.3: an ecosystem of related images — physical original, digital hybrid, printed and manually retouched version, video — connected by a shared visual DNA and traceable lineage of transformations rather than a single fixed object.

**Expansions**  
Series by Gianpiero Moioli (§5.3.1.2): AI outpainting applied to a single manual painting to extend the image outward. The AI analyzes colors, textures, and rhythms of the original canvas and generates new sections. The expanded image can be re-materialized through printing and further manual intervention.

---

## F

**FDM — Fused Deposition Modeling**  
3D printing method that deposits layers of melted plastic (typically PLA). Used in Chapter 5 as the first step in the fabrication chain: PLA master model → silicone mold → lost-wax bronze casting. Parameters: Prusa i3 MK3S+, 0.12 mm layer height, 15% gyroid infill (Appendix F).

**Fine-tuning**  
Adapting a pre-trained AI model to a specific domain or style using a curated dataset. In Chapter 5 this includes DreamBooth (Stable Diffusion) and Custom Models (MidJourney V7) to reproduce consistent artistic styles across outputs.

---

## G

**Generative AI**  
Artificial intelligence systems trained on large image or text corpora to generate new content: images (Stable Diffusion, MidJourney, DALL·E), video (Kling 2.5, Runway Gen-3), or other media. In art contexts, generative AI functions as a creative collaborator, curator of emergence, or algorithmic brush — extending rather than replacing the artist's gesture.

**Geometry Nodes**  
Blender's node-based system for procedural geometry generation. Allows artists to define algorithmic rules that generate and transform meshes from parameters rather than direct manual modeling. Used in Chapter 5 for procedural textures, surface patterns, and "digital damage" simulations on scanned models.

**Gravity Sketch**  
VR sculpting environment in which artists wear a headset and use tracked hand controllers to shape virtual clay at real scale, circling the work as if standing inside a studio. Enables an embodied sculptural experience within virtual space.

---

## H

**Hybrid Painting Process**  
Methodology developed in Chapter 5 (§5.1.2): works begin from a physical gesture (acrylic, ink, or pen on paper/cardboard), pass through digital painting and generative AI, and may receive new manual layers, remain in digital state, or be certified as unique works. Three possible outcomes: physical original, digital variation, certified hybrid artwork.

**Hybridizations**  
Series by Gianpiero Moioli (§5.3.1.1): two or more distinct real works merged through digital painting and AI into a single composition or image sequence, creating visual narratives with unforeseen symbolic connections.

**Hybrid Techniques**  
Liminal zone where manual and digital practices intersect (§5.1): drawing, modeling, 3D processes, procedural systems, and AI. Not merely a combination of media but a condition where memory and innovation co-construct aesthetic form.

---

## I

**img2img**  
Stable Diffusion workflow that uses an existing image as structural input for new generation, allowing the AI to maintain compositional continuity while introducing variation. Basis for transformation and hybridization workflows in Chapter 5.

**Inpainting**  
AI process of filling masked or missing zones of an image while maintaining consistency with surrounding areas. Used in Chapter 5 to modify specific parts of a painting or to complete fragmented forms.

**IP-Adapter**  
Extension that injects image reference into Stable Diffusion generation, guiding style and content from a source image rather than text alone. Enables structural or stylistic continuity with source material.

---

## L

**Lost Codes**  
Series of hybrid sculptures by Gianpiero Moioli (§5.5.2): fragments of classical forms — broken, recomposed, reimagined — that become new signs suspended between past and future. Built by integrating 3D scans of classical works with procedurally generated geometry in Blender.

**Lost-Wax Casting (Investment Casting)**  
Traditional bronze casting technique adapted for digital origins: PLA master model → silicone mold → wax copy → ceramic shell → bronze pour. Digital shrinkage compensation: +2.0% applied to the .stl file before printing (Appendix F). Observed failure modes: surface porosity, extreme shrinkage/warping.

---

## M

**MidJourney**  
Cloud-based AI image and video generation platform. Version V7 (used in Chapter 5) supports image-to-video generation, Custom Models for style personalization, and Vary (Region) for selective inpainting. Requires a paid subscription; runs on remote servers — no local GPU needed.

**Morphogenesis (Digital)**  
Simulation of organic growth and development through algorithmic processes. In Chapter 5, geometry node networks generate branching patterns, modular grids, and fractal structures that shift focus from the finished object to the rules of its becoming.

---

## O

**OpenPose**  
ControlNet variant that reads human body keypoints from a reference image and passes them as structural conditioning to Stable Diffusion generation, ensuring pose consistency in figure-based work.

**Outpainting**  
AI process of extending an image beyond its original borders, generating new content that respects the visual syntax of the original. Canonical example: OpenAI's DALL·E 2 outpainting of Van Gogh's *The Starry Night* (September 2022). Core technique behind the "Expansions" series (§5.3.1.2).

---

## P

**Photogrammetry**  
3D scanning technique that reconstructs volumetric geometry from overlapping photographs. Enables the digitization of physical sculptures, faces, or objects for integration into virtual workflows. Full protocols in Chapter 6.

**Post-Human Identity**  
Condition in which human subjectivity extends beyond the boundaries of its own flesh through digital augmentation and transformation (§5.6.2). In Chapter 5 it manifests in self-portraits where the scanned face is fragmented, hybridized, and merged with metaphysical landscapes and symbolic elements by AI.

**PLA — Polylactic Acid**  
Biodegradable thermoplastic used in FDM 3D printing. In Chapter 5 it serves as the prototyping material for the lost-wax casting chain. Characterized as "fragile, imperfect, biodegradable" — its material qualities contrast deliberately with the permanence of the final bronze.

**Procedural Generation**  
Creation of geometry, texture, or other visual elements through algorithmic rules and parameters rather than direct manual modeling. Blender's Geometry Nodes and Houdini are the primary tools. Enables potentially infinite variations from a single set of rules.

**Prompt Engineering**  
Practice of crafting text descriptions (prompts) to guide AI image generation. In Chapter 5, prompts activate "fields of potentialities" rather than prescribing fixed images; the artist intervenes as a curator of emergence.

---

## R

**Real-ESRGAN**  
Open-source neural network for image super-resolution and upscaling. Free alternative to Topaz Gigapixel AI for enlarging digital artworks for monumental prints or immersive installations.

**Retopology**  
Process of rebuilding the polygon mesh of a 3D scan or high-resolution sculpt with cleaner, more efficient geometry optimized for rendering, animation, or fabrication. Performed in Blender after scanning.

---

## S

**Stable Diffusion**  
Open-source latent diffusion model for AI image generation. Version 1.5 checkpoint used in Chapter 5 on an NVIDIA RTX 4070 Ti (12 GB VRAM): generates standard 512×512 images in approximately 2.5–4 seconds. Interfaces: Automatic1111 WebUI, ComfyUI (node-based), InvokeAI.

**Spatialism (Spazialismo)**  
Movement founded by Lucio Fontana (Manifesto 1947): call for art to move beyond the "illusory space" of canvas and traditional sculpture to embrace real space, real time, light, and energy as dimensions of artistic creation. Chapter 5 reads AI expansions and virtual sculpture as contemporary continuations of this ambition.

**Style Transfer**  
AI technique that applies the visual style of one image to the content of another. Used in Chapter 5 as part of transformation and hybridization workflows to introduce historical pictorial styles into contemporary compositions.

---

## T

**Topaz Gigapixel AI**  
Commercial AI upscaling application (v8.4.4 used in Chapter 5). Enlarges raster images by 4× or more with SSIM > 0.95 compared to original quality, enabling gestural digital paintings to be printed at monumental scale.

**Transmedial / Transmaterial Art**  
Art in which real and virtual no longer oppose each other but converge into a single augmented reality of imagination (§5.7). Works exist simultaneously as canvas print, video file, and certified digital matrix, embodying multiple ontological states.

---

## V

**VR Sculpting**  
Sculptural process performed inside a virtual reality environment using tracked hand controllers (Gravity Sketch, Adobe Medium). Artists work at real scale, moving around the virtual object as in a physical studio, while the digital environment removes material constraints of weight, gravity, and cost.

---

## Z

**ZBrush**  
Industry-standard digital sculpting application offering a brush-based interface that simulates physical clay modeling. Known for high polygon density (up to hundreds of millions of polygons), enabling extreme organic detail before retopology for production.

---

*For certification and blockchain terminology (SHA-256, CDM, OpenTimestamps, NFT, blockchain), see the Chapter 4 glossary: `04/docs/ref_glossary.md`.*
