# Pablo Picasso (1881–1973)

> Artist Note for **§3.6.2** — *Picasso's Procedural Gesture*  
> **Art Between Matter and Code** · Gianpiero Moioli · Apress 2025

---

## Profile

Pablo Ruiz Picasso was a Spanish painter, sculptor, printmaker, ceramicist, and stage designer. One of the most influential artists of the twentieth century, he is best known as a co-founder of Cubism and as a restless experimenter across media and technique. Picasso worked in Paris for most of his adult life and produced an estimated 20,000 works.

## Light Drawing and the Gjon Mili Photographs (1949)

In 1949, the photographer **Gjon Mili** visited Picasso at his studio in Vallauris, southern France. Mili had previously pioneered stroboscopic photography in collaboration with Harold Edgerton at MIT. In the darkened studio he equipped Picasso with a small electric lamp and asked him to draw in the air while Mili held the shutter open.

The resulting images — published in *Life* magazine in January 1950 — show luminous lines suspended in space: bulls, centaurs, a nude figure, rendered in a single unbroken gesture. Picasso reportedly drew the forms spontaneously, in seconds, without hesitation or revision. The photographs are among the earliest examples of what would later be called **light painting** or **light graffiti**.

The gesture is pure duration: it exists only while the shutter is open. No physical trace remains on any surface — only light inscribed on film emulsion.

## Connection to Chapter 3

The script `picasso_gesture.py` (§3.6.2) recreates this logic procedurally:

- A **Bézier curve** drawn in 3D space substitutes for the gesture traced by hand.
- **Bevel depth** gives the curve volumetric presence — thickness in space.
- An **Emission shader** makes the curve glow against a black background, mimicking long-exposure light.
- A **Trim Curve** Geometry Nodes modifier animates the progressive unfolding of the line from its start point to its end — as if Picasso's hand were still moving.

The procedural version inverts Picasso's spontaneity: it is parametric, repeatable, and editable. Yet it preserves the essential logic — a line tracing itself through darkness.

## Key Works Referenced

| Work | Date | Medium |
|------|------|--------|
| *Guernica* | 1937 | Oil on canvas |
| Light drawing (Gjon Mili photographs) | 1949 | Long-exposure photography |
| *Las Meninas* (after Velázquez) | 1957 | Oil on canvas |

## Further Reading

- Berger, John. *The Success and Failure of Picasso*. Penguin, 1965.
- Richardson, John. *A Life of Picasso*, 4 vols. Random House, 1991–2021.
- Mili, Gjon. "Picasso Takes a Pencil of Light." *Life*, 30 Jan 1950, pp. 76–79.
