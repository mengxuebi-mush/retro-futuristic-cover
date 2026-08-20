# Retro Editorial Cover

A ChatGPT/Codex Skill that turns an article, draft, topic, or sentence into one finished retro-futuristic editorial social-media cover.

The Skill preserves the semantic identity of an existing article title, rephrases it only when needed for cover readability, and generates a polished cover with seamless soft gradients, diffuse light, fine grain, readable typography, generous negative space, and restrained geometric accents. When no title exists, it derives a faithful title from the source.

## Visual direction

- Seamless, continuous soft gradients rather than isolated color halos
- Diffuse light and fine frosted grain
- Adaptive tonal regimes and monochromatic, analogous, duotone, or tri-color harmony modes
- Controlled coral roles so warm coral may lead, accent, or disappear across outputs
- One dominant, highly readable headline
- Source-title fidelity with locked subject, use-case, promise, meaningful-count, audience, and proper-noun anchors
- Content-aware title modes for titled articles, utility/list content, and thesis-led essays
- Minimal category label and micro-subtitle
- Small randomized stars, triangles, rhombi, dots, rings, or corner brackets
- Rotating arches, portals, flowing chromatic shapes, perspective planes, curved surfaces, and flattened orbs
- An editorial alignment system connecting labels, type, structural lines, and micro-accents
- Typography that rotates between restrained editorial serif, clean sans, and neutral grotesk
- A hard-compliance gate followed by a poster-integration critique of the actual rendered pixels
- Targeted local editing for isolated flaws and fresh regeneration for structural failures
- At most three private versions, with only the final passing cover shown
- Deterministic verification of output format, dimensions, and aspect ratio
- No cyberpunk neon, dense collage, experimental type, or text-heavy layouts
- No generic “high-contrast Didone + glowing planet + orbit + sparkle” AI-poster combination

## Platform presets

| Platform | Canvas |
|---|---:|
| Xiaohongshu cover | 1080 × 1440 px (3:4) |
| X post landscape | 1200 × 675 px (16:9) |
| X post square | 1080 × 1080 px (1:1) |
| X banner | 1500 × 500 px (3:1) |

A generic X post request uses the landscape preset. Square and banner layouts are selected only when explicitly requested, and each format is recomposed rather than cropped or stretched.

## Install

Copy this repository into your personal Skills directory:

```text
~/.agents/skills/retro-editorial-cover
```

Start a new task after installation so the updated Skill is loaded.

## Use

Provide an article, topic, draft, or sentence and ask for a social-media cover. For example:

```text
Use Retro Editorial Cover to turn this article into an X post cover.
```

The Skill generates one final cover by default. It privately critiques and improves the result, and does not expose intermediate images, prompts, or internal verdicts unless requested.
