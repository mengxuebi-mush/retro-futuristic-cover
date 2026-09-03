# COMPOUND_SET Prompt A/B Diagnosis

## Question

Does `COMPOUND_SET` collapse because the image generator is merely inconsistent, or because the compiled request does not resolve and communicate the members of the assembly?

## Controlled comparison

Both variants used the same existing `compound-set.brief.json`, bundled style reference, carrier, copy, canvas, layout, focal event, speculative family and function, custom morphology, treatment, scale, screen state, palette, active hues, topology, typography, and detail language.

Variant A used the current `generator_instruction` unchanged. Variant B appended one assembly-only block that named three complete functional members, required each member to remain independently traceable, joined them through one shared tangent/baseline into one outer mass, and prohibited both over-fusion and three detached hero products.

## Pixel evidence

### A — current compiler output

- One continuous ring and one suspended cabin are visible.
- Seams, windows, bridges, and interior rooms remain parts of that one object; they do not establish two or three complete members.
- The result therefore collapses into `SINGLE_OBJECT` again.
- Title-first hierarchy, exact seven-string copy, opaque delivery, background coverage, and overall subject unity pass.

### B — explicit member plan

- Three complete objects remain countable at full size and 25%: a toroidal collaboration chamber, a crescent fabrication dock, and an oval material-library pod.
- Each has its own shell and functional aperture; none is merely a seam, room, or appendage of the main ring.
- Their contact bridge, shared baseline, overlapping footprint, common material, and curvature make them read first as one compact set rather than three floating product heroes.
- Title-first hierarchy, exact seven-string copy, opaque delivery, background coverage, and subject unity pass.

Both outputs introduce an independent apricot/orange field beyond the locked warm-ivory and pale-pistachio hues. Because the same color leak occurs on both sides of the comparison, it is a separate palette-generation failure and does not explain the assembly difference.

## Code-path evidence

- The selector manifest already contains `subject_assembly_count` and `subject_mass_rule`.
- The compiled brief retains `subject.mass_rule`.
- `_generator_instruction()` emits only the assembly identifier and omits both the count and mass-rule text.
- `generation-content.schema.json` has no field for resolving two or three complete assembly members or their roles.
- The singular custom morphology repeatedly says “one loop” and “one cabin,” so the generator receives much more concrete singular-object language than multi-object language.

## Diagnosis

The primary problem is not the composition family and not an overly restrictive future-object morphology system. It is an instruction-model gap between the structured recipe and the generator-facing request:

1. existing assembly semantics are dropped during prompt serialization; and
2. `COMPOUND_SET` has no content-level member plan that converts an abstract count into two or three concrete, complete, related objects.

Variant B demonstrates that the current visual system can produce a valid compact compound set once those members are resolved explicitly.

## Recommended implementation direction

Make the fix generic rather than preserving this experiment's torus/crescent/oval objects:

1. Serialize `subject_assembly_count` and `subject_mass_rule` into every generated instruction.
2. For multi-object assemblies, resolve a small member plan before compilation. A `COMPOUND_SET` plan should contain 2–3 complete member roles, each with a distinct function/form cue, plus one shared relationship.
3. Add a generic anti-collapse instruction: every compound member remains independently traceable at full size and thumbnail size; internal parts of one object do not count as members.
4. Keep the existing anti-competition rule: members form one outer mass and do not become equal detached heroes.
5. Add compiler tests proving that the count, mass rule, member roles, shared relation, and anti-collapse language survive into `generator_instruction`.

Do not change Composition Contracts or constrain future forms to this test's shapes. Treat the repeated apricot field as a separate color-fidelity issue.
