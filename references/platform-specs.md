# Platform cover specifications

Checked on 2026-08-20. Treat these as defaults, not permanent platform law. If a platform changes its public specifications or display behavior, verify current public documentation and use the newest reliable specification before generating.

## Decision table

| Platform and use | Default canvas | Why |
|---|---:|---|
| Xiaohongshu image-note cover | 3:4 portrait; 1080 x 1440 px | The dominant mobile-feed format and the current common recommendation. A 1242 x 1660 px canvas is also widely used, though it is only approximately 3:4; prefer exact 3:4 when the generator supports it. |
| Xiaohongshu long-form cover | 3:4 portrait delivery; 1080 x 1440 px | User-verified in the current Xiaohongshu long-form flow. Compose it with a deeper crop-safe layout than a normal image-note cover. A 9:16 working master at 1080 x 1920 px may be generated first, with every critical element inside its centered 3:4 window, then center-cropped to the 3:4 delivery asset. |
| X post landscape | 16:9 landscape; exactly 1200 x 675 px | Default for a generic X/Twitter post, post cover, or X cover request. |
| X post square | 1:1 square; exactly 1080 x 1080 px | Use only when the request explicitly says square, 方形, or 1:1. |
| X banner | 3:1 landscape; exactly 1500 x 500 px | Use only when the request explicitly says banner, header, profile banner, 横幅, or 页头. |

Do not silently reuse a canvas across platforms or X presets. Preserve the title and visual family while recomposing the hierarchy, gradient flow, abstract forms, and ornament placement for the target ratio. Never obtain the square or banner preset by simply cropping or stretching the landscape preset.

## Sources and evidence notes

### Xiaohongshu

- A mirrored 2025 Xiaohongshu E-commerce Learning Center beginner guide says product/seeding note covers should use a 3:4 portrait image because it occupies more feed area: https://pdf.dfcfw.com/pdf/H3_AP202504151656814073_1.pdf
- A current 2026 practitioner guide recommends 3:4 and 1080 x 1440 px, and documents 1242 x 1660 px as a common high-resolution template size: https://xiaohongshu.oimi.ai/zh/blog/xiaohongshu-cover-size
- Canva China lists Xiaohongshu portrait covers at 1242 x 1660 px and notes the platform's portrait, square, and landscape formats: https://www.canva.cn/sizes/little-red-book/

Evidence caveat: a stable, directly accessible Xiaohongshu public help page defining one mandatory pixel size was not found during this check. Therefore, treat 3:4 as the well-supported format recommendation and 1080 x 1440 as the clean exact-ratio working canvas, not as an immutable upload requirement.

### Xiaohongshu long-form observed behavior

- User verification on 2026-08-20 confirms that the dedicated long-form cover accepts a 3:4 asset.
- Treat the accepted upload ratio and the reliable visible area as different constraints. Long-form previews may introduce container insets, rounded masking, or small recrops, so a title that merely fits the raw 3:4 canvas can still feel clipped or crowded.
- Default long-form delivery to exact 3:4 at 1080 x 1440 px, but use a **deep-safe composition**: keep critical text within approximately 10–12% horizontal margins, keep the title block to roughly 72–76% of canvas width, and preserve visibly generous space on both sides of the letterforms.
- Preferred construction method: compose a 9:16 master at 1080 x 1920 px; place every critical element inside the centered 1080 x 1440 window from y=240 through y=1680; inspect that crop; then deliver the centered 3:4 crop. The extra 9:16 height is a composition scaffold, not a requirement that the final upload remain 9:16.
- A direct 3:4 generation is acceptable only when it passes the same deep-safe margin and simulated-crop checks. Do not enlarge the title merely because the direct canvas is shorter.

### X

- User-approved design presets recorded on 2026-08-19 are: X post landscape at 1200 x 675 px, X post square at 1080 x 1080 px, and X banner at 1500 x 500 px. These are the skill's exact routing presets and take precedence over alternative working canvases unless the user provides different exact dimensions.
- X Help says posted photos may be JPEG, PNG, or GIF, are automatically scaled for display, and static photos can be up to 5 MB: https://help.x.com/en/using-x/posting-gifs-and-pictures
- X Business currently supports 16:9 at 1920 x 1080 px, along with 4:5, 2:3, 1:1, 9:16, and 1.91:1 for image ad creatives: https://business.x.com/en/blog/x-expands-aspect-ratio-support-for-ad-creatives-replacement
- A current 2026 organic-post size guide recommends 1200 x 675 px at 16:9 for a single in-feed image: https://www.krumzi.com/size-guide/twitter-post-size

Evidence caveat: X's official organic-photo help specifies file types, size limits, and automatic scaling but does not prescribe one universal organic-post aspect ratio. Therefore these three values are controlled design presets, not claims about universal upload limits. Use landscape as the generic X-post default and route square or banner only from explicit user language.

## Re-verification rule

When current platform fit matters, check sources in this order:

1. Current official creator/help documentation for the exact organic content type.
2. Current official business/ads documentation, labeled as advertising guidance rather than an organic-post rule.
3. Recent reputable creator-tool or publishing guides that describe observed in-feed behavior.

Record the verification date when changing these defaults. Prefer a newly published official specification over any value in this file.
