# Retro Editorial Cover

A ChatGPT/Codex Skill that turns an article, draft, topic, or sentence into one finished retro-futuristic editorial social-media cover.

The Skill extracts one core idea, aggressively condenses it into a short headline, and generates a polished cover with seamless soft gradients, diffuse light, fine grain, readable typography, generous negative space, and restrained geometric accents.

## Visual direction

- Seamless, continuous soft gradients rather than isolated color halos
- Diffuse light and fine frosted grain
- Slightly softened color with controlled palette families
- One dominant, highly readable headline
- Minimal category label and micro-subtitle
- Small randomized stars, triangles, rhombi, dots, rings, or corner brackets
- Subtle orbs, curves, portals, grids, and hairline structures
- No cyberpunk neon, dense collage, experimental type, or text-heavy layouts

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

The Skill generates one final cover by default and does not expose the intermediate image prompt.
