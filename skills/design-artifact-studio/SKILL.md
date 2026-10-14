---
name: design-artifact-studio
description: Design, prototype, critique, and refine UI as rendered, reviewable artifacts, such as mockups, app screens and flows, landing and editorial pages, redesigns, side-by-side direction studies, and working HTML prototypes. Use when the user wants a screen or page designed, prototyped, reviewed, or improved, including inside an existing project, where its stack and design system are kept. For AI-generated concept images use ui-design-brainstorm. Not for backend implementation.
---

# Design Artifact Studio

Create a design someone can inspect and make a decision about. Deliver a rendered artifact or the requested critique, with the few decisions and limitations needed to judge it. Visual craft and usability are separate responsibilities; fulfill both at the chosen fidelity.

## Establish what this surface must do

Read the request, supplied references, relevant existing screens, and any project design rules. Determine whether this is a new concept, an extension of an existing system, or a refinement. A missing design document is not evidence that no system exists. Preserve the user's chosen content, identity, behavior, and scope during refinement.

Establish the kind of work and fidelity needed: critique, visual exploration, functional prototype, extension/refinement, constrained reconstruction, or a combination. State what must remain fixed and what may change. A critique can end with findings; a visual study can remain static; a functional prototype must support its promised actions. Do not add screens or behavior merely to satisfy a process checklist.

Identify the audience, situation, primary task, necessary information, and successful outcome. Separate supplied facts from sample content and assumptions. For multi-screen work, identify the entry point and the state users should reach. Ask only for missing information that would materially change the design. Offer a specific recommendation when taste is open; do useful work while awaiting optional input. Do not introduce an approval gate for ordinary local prototyping; the one planned stop is the person's choice of visual direction when it is open.

Make success observable before styling: what must the person understand, decide or finish, and what would show that they succeeded? For a new product flow, read the structure guidance in [references/interaction-design.md](references/interaction-design.md) before choosing screens. Keep this proportional: a small component edit does not need a new product strategy.

For an open or ambiguous brief, name the product decision this prototype should help resolve and the unsupported assumption most likely to change the flow. Choose scope and fidelity to examine that question; keep assumptions explicit rather than inventing research. For a constrained reconstruction, the supplied target is sufficient.

Choose priorities by the surface's job. These are examples, not an exhaustive set:

| Job | Design priority | Frequent failure |
|---|---|---|
| Complete a task | Clear action, relevant context, predictable controls and recovery | Decorative dashboard with no usable workflow |
| Decide whether to act | Specific offer, credible evidence, resolved objections | A beautiful page that never explains the offer |
| Understand content | Reading rhythm, navigation, legible structure | Treating every paragraph as a card |
| Inspect creative work | The work itself, useful comparison and detail | Interface decoration overwhelming the subject |

A product can need several of these. Decide per surface, not once for the entire brand.

## Choose a direction with reasons

When choosing an original direction or translating supplied visual references, read [references/art-direction.md](references/art-direction.md). Identify each reference's role: exact target, existing-system constraint, inspiration, or source content. Compare or borrow only what that role and the brief justify; preserve evidenced defining decisions for a reconstruction.

When the work starts from a ui-design-brainstorm handoff, read `HANDOFF.md` and inspect its linked image before choosing anything. Its status says whether a person selected the concept, and its build request says what is authorized; without a build request, ask before building. Treat the image in the role the handoff gives it. Requirements and the person's stated decisions outrank painted details: the handoff's Correct list is binding, and its Resolve list names what you decide or ask.

When the visual direction itself is open, with no existing system, selected concept or supplied target, run the direction round in [references/divergence.md](references/divergence.md) before building: three dealt directions, shown as static studies, then the person's choice. For a screen inside a product, two keep the layout the category's products share and one is a stretch, all in the category's own surface. A model's first direction, and its own choice of alternatives, repeat from brief to brief; the deal is what makes the options worth choosing between.

Explore only choices that are open. When the user requests alternatives, produce two or three small visual directions using representative content and the allowed dimensions of change. Structural exploration may vary reading order or task organization; a styling study may deliberately hold both fixed. Otherwise select and briefly explain a suitable direction without manufacturing alternatives for a settled design.

State the selected direction in concrete terms: what takes visual priority, how information is organized, what gives it character, and why this serves the audience. Design around actual content early. A familiar convention is valid when it makes the task easier. A surprising treatment must earn its cost in comprehension.

For a new surface, a direction round, or a multi-screen prototype, create or update a short `DESIGN.md` alongside the artifact. Record:

- Audience, primary task, scope, sample-data assumptions, and any open product decision being examined.
- Chosen direction, reference observations, and important rejected alternatives with reasons. After a direction round: the seed, the directions shown, and what the person chose and said.
- Semantic color roles, typography with actual available fonts and fallbacks, spacing, component treatment, and responsive behavior.
- Principal interaction states and what is simulated.

Reuse an existing source of truth rather than starting a competing document. Keep project taste in project files; do not silently change this reusable skill or personal memory.

## Make the artifact

Read [references/html-delivery.md](references/html-delivery.md) when creating standalone HTML, and [references/interaction-design.md](references/interaction-design.md) for interactions within the promised scope.

Before implementation or a substantial refinement, use the [review planning guidance](references/review.md#plan-the-checks-around-the-artifact) to define critical checks for the actual medium, fidelity, features, and supported layouts.

Default to a self-contained HTML file with embedded CSS and modest JavaScript for an interactive prototype. Unless the project or the person names a place, save a standalone artifact and its records in `outputs/<short-name>/`. Use local companion assets when fidelity justifies them and bundle them for delivery. Favor SVG for an inherently vector diagram; use the relevant document tools for a requested PDF or slide deck. In an existing application, keep its framework and conventions. Select the format by the decision the user needs to make, not by the skill's favorite technology.

Build the primary content and experience first, then the surrounding interface. Use semantic tokens rather than scattered aesthetic decisions. When small screens are supported, design their hierarchy deliberately; shrinking the desktop composition is insufficient. Add expression where it serves the brief, and preserve useful conventions. A restrained interface still needs considered typography, proportions, spacing, color relationships, and imagery.

Use truthful, domain-specific copy. Do not invent endorsements, verified outcomes, live activity, or customer claims. Distinguish fictional fixtures from real data in review context. A prototype may simulate local interactions, but must not imply that money moved, a message was sent, or a server saved data when it did not.

In a functional prototype, implement controls within the promised scope with appropriate state and feedback. Omit unrelated navigation rather than populate a shell with dead links. Make deliberately excluded destinations and static studies' interaction limits apparent in the review context. A toast alone does not demonstrate a promised action: an export creates a file, a save changes the displayed state, and a filter changes the results.

## Inspect and improve

Read [references/review.md](references/review.md). Inspect the result in its actual medium: a browser for web artifacts, an appropriate renderer for other formats, or the supplied surface for a critique. For functional UI, exercise the primary task and recovery paths needed by the promised interaction on supported layouts; treat missing required states as gaps. Inspect the state the user actually reaches. For static studies, review composition, content, legibility, and output integrity. View rendered evidence to judge visual craft; source inspection or passing functional checks alone cannot establish visual quality.

Prioritize defects that block the task, mislead the user, hide content, or break access. Then improve the few visual decisions with the greatest effect. Recheck affected views after fixes. Stop when the agreed scope works and the remaining observations are optional taste alternatives; do not iterate indefinitely for an unsupported perfection score. If rendering or a specific check is unavailable, identify it as unverified.

Deliver the requested artifact or critique, a brief rationale, relevant verification evidence, and material limits. Name `DESIGN.md` and `VALIDATION.md` where you wrote them; inside an existing repository, put such records where its conventions put documentation. Provide a clickable artifact and explain what can be tried when interaction is promised. Open artifacts in the app when supported. Include screenshots or a portable bundle when useful. Keep implementation and research notes outside the product's main flow. End a collaborative design round with a concrete next decision only when one remains.
