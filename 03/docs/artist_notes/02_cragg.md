# Tony Cragg (b. 1949)

> Artist Note for **§3.6.3.1** — *Stratified Torsional Surfaces*  
> **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025

---

## Profile

Anthony Douglas Cragg CBE RA was born in Liverpool and trained as a laboratory technician before studying sculpture at Wimbledon School of Art and the Royal College of Art, London. He has lived and worked in Wuppertal, Germany, since 1977, and served as Director of the Kunstakademie Düsseldorf (2009–2013). He was awarded the Turner Prize in 1988 and the Praemium Imperiale in 2007.

Cragg is associated with the New British Sculpture movement of the 1980s, though his practice has consistently evolved beyond the found-object aesthetics of that period toward a sustained investigation of **organic form, material behaviour, and the latent shapes hidden within matter**.

## Formal Language

Cragg's mature sculpture falls into several recurring families:

- **Stacks** — layered, stratified volumes assembled from cross-sections of organic or functional forms. The stack reads differently from every angle: the plan-view silhouettes are simple, but the accumulated layering produces complex torsional surfaces.
- **Rational Beings** — upright, torque-twisted columns that suggest compressed human or animal presence without depicting it.
- **Early Forms** — elongated vessels whose walls billow outward like soap bubbles or cellular membranes.
- **Points of View** — large-scale works where multiple profile silhouettes of figurative objects (bottles, vases, tools) are merged into a single three-dimensional body.

The common thread is **emergence**: forms that could not have been designed from a single viewpoint but arise from the interaction of cross-sections, rotations, and material constraints.

## *Stack* (2011) and Related Works

*Stack* (2011, bronze, 285 × 80 × 85 cm) is one of Cragg's characteristic stratified sculptures. A column of horizontal slabs, each slightly rotated relative to its neighbour, accumulates into a form that simultaneously reads as geological strata, as a twisting human torso, and as an abstract topological surface. The torsion is distributed: no single layer is dramatically different from its neighbour, but the total rotation across the full height is substantial.

The script `cragg_stack.py` (§3.6.3.1) models this logic:

- A starting cube is **torsion-twisted** in bmesh (rotating top vertices while anchoring the base).
- A **Subdivision Surface** modifier adds resolution.
- A **Displace modifier** driven by a Musgrave Hybrid Multifractal texture introduces the geological layering — stratified noise that recalls sedimentary rock or the annual rings of wood.
- An optional **animation** shows the displacement strength growing from zero, making visible the moment when inert geometry acquires organic complexity.

## Key Works

| Work | Date | Material |
|------|------|----------|
| *Palette* | 1982 | Plastic objects on plywood |
| *Loco* | 1986 | Mixed media |
| *Secretions* | 1987 | Various |
| *Rational Beings* | 1996– | Bronze, stainless steel |
| *Stack* | 2011 | Bronze |
| *Versus* | 2016 | Bronze |

## Permanent Collections

Tate Collection (London), Museum of Modern Art (New York), Centre Pompidou (Paris), Von der Heydt-Museum (Wuppertal), Museo Nacional Centro de Arte Reina Sofía (Madrid).

## Further Reading

- Cragg, Tony, and Friedemann Malsch. *Tony Cragg: Sculptures and Drawings*. Kunstmuseum Liechtenstein, 2007.
- Fer, Briony, et al. *Tony Cragg*. Lund Humphries, 1996.
- Blistène, Bernard (ed.). *Tony Cragg: Entre la matière et l'esprit*. Centre Pompidou, 2011.
