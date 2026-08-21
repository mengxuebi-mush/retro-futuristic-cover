# Retro Futuristic Cover

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
- Three controlled CJK sans modes—neo-grotesk, soft humanist, and structural sans—with Song/Ming and generic heavy system Heiti explicitly rejected
- A persistent coordinated design deck that rotates palettes, gradient flow, focal mode, hero or atmospheric form, type mode, labels, and accents while excluding recent selections
- Readable article-cover typography: balanced three-line X headlines, regular-to-medium optical weight, relaxed display leading, and a roughly 28–34% tight visible-glyph height for longer landscape titles
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

## Requirements

- **Recommended:** Codex with an image-generation tool enabled.
- **Alternative:** another agent or image-generation model that can accept a local style-reference image, follow exact text constraints, and save the result as a local image file.
- Python 3.9 or newer for the bundled recipe selector and image verifier.

Claude Code is not recommended as the default environment for this Skill because it does not provide the image-generation workflow the Skill depends on by itself. Use it only when it is connected to a compatible external image-generation tool that can accept the bundled reference image and preserve the three required text elements.

## Install

For Codex, clone the repository into your personal Skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/mengxuebi-mush/retro-futuristic-cover.git ~/.codex/skills/retro-futuristic-cover
```

For another compatible agent environment, copy or clone the repository into that environment's Skills directory. Start a new task after installation so the Skill is loaded.

## Use

Provide an article, topic, draft, or sentence and ask for a social-media cover. For example:

```text
Use Retro Futuristic Cover to turn this article into an X post cover.
```

The Skill generates one final cover by default. It privately critiques and improves the result, and does not expose intermediate images, prompts, or internal verdicts unless requested.

## License

Released under the [MIT License](LICENSE).
