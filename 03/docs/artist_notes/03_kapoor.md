# Anish Kapoor (b. 1954)

> Artist Note for **§3.6.3.2** — *Tall Tree and The Eye*  
> **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025

---

## Profile

Anish Kapoor was born in Mumbai and studied at Hornsey College of Art and Chelsea School of Art in London. He has lived and worked in London since the late 1970s. He received the Turner Prize in 1991 and was awarded a CBE in 2003.

Kapoor's work spans sculpture, installation, and large-scale public art. His practice is organised around a small number of deep formal and philosophical concerns: **the void**, **pigment and colour as pure matter**, **reflective surfaces and perceptual displacement**, **the uncanny interior**, and **non-linear scale**. He does not fabricate his works personally but directs teams of specialist craftspeople and engineers, working at scales from intimate hand-sized objects to monumental urban installations.

## Recurring Formal Themes

### The Void and Interior Space
Many of Kapoor's early works are simple geometric forms (cylinders, cones, hemispheres) whose interiors are filled with intensely pigmented powder — raw ultramarine, cadmium red, stone grey. The viewer sees not a surface but a depth that the eye cannot measure: the pigment scatters light uniformly in all directions, destroying the optical cues that allow the brain to perceive distance.

### Reflective Surfaces
Beginning in the 1990s, Kapoor began working with highly polished stainless steel. The mirror finish reflects and distorts the surrounding environment, inverting the sky, compressing and expanding figures, and turning the boundary between sculpture and world into a zone of perceptual ambiguity. The sculpture does not occupy space so much as consume it.

### Biological and Cosmological Scale
Works like *Marsyas* (Tate Modern, 2002) — a 155-metre PVC skin stretched across three steel rings — operate at a scale that cannot be seen from a single viewpoint. The form is legible only in fragments: here a red membrane, there a horizon of steel, there the far end of a tunnel. Scale becomes content.

## *Tall Tree and The Eye* (2009)

*Tall Tree and The Eye* consists of **73 polished stainless steel spheres** stacked into a vertical column approximately 15 metres tall. The spheres decrease in size from base to apex. Each sphere reflects the others, the surrounding architecture, and the viewer simultaneously, creating an infinite regression of distorted reflections.

The work was first exhibited outside the Guggenheim Bilbao in 2009 and has since been installed in multiple locations. It is sometimes read as a technological tree — organic in its vertical tapering, mechanical in its material — or as a model of atomic structure scaled to human perception.

### Structural Logic

The column is self-supporting only at the base; the upper spheres are attached via internal armature. From a distance the structure reads as a single coherent tower. Up close the seams between spheres disappear into reflection, and the column appears as a continuous shimmering surface.

The script `kapoor_tall_tree.py` (§3.6.3.2) reproduces this logic in two parallel ways:

**Geometry Nodes method:** Spheres are distributed inside a cylindrical volume using `Distribute Points in Volume`, with density and scale variation that concentrates mass at the base and reduces it toward the apex. The near-mirror material uses `Metallic = 1.0` and `Roughness = 0.02`.

**Python loop method:** Spheres are placed element by element with explicit vertical spacing and random radial offsets, giving finer control over the column's silhouette. The two approaches produce visually similar results through different procedural logics — a commentary on the relationship between algorithm and intention.

## Key Works

| Work | Date | Location |
|------|------|----------|
| *To Reflect an Intimate Part of the Red* | 1981 | — |
| *1000 Names* | 1979–80 | — |
| *When I am Pregnant* | 1992 | — |
| *Cloud Gate* | 2006 | Millennium Park, Chicago |
| *Marsyas* | 2002 | Tate Modern, London |
| *Tall Tree and The Eye* | 2009 | Guggenheim Bilbao; multiple sites |
| *Descent into Limbo* | 1992 / 2017 | — |
| *Shooting into the Corner* | 2008–09 | — |

## Further Reading

- Celant, Germano (ed.). *Anish Kapoor*. Charta / Guggenheim Bilbao, 2009.
- Blistène, Bernard, and Marcella Beccaria (eds.). *Anish Kapoor*. Skira, 2011.
- Kapoor, Anish. *Flashback*. Hayward Gallery, 1994.
- Young, James E. *Anish Kapoor: The Jewish Museum*. Jewish Museum, New York, 2018.
