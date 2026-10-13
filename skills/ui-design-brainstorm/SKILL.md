---
name: ui-design-brainstorm
description: Explore product UI directions as AI-generated concept images, compare them, and hand the chosen one off for building. Use when the user wants generated mockup images or image-based visual brainstorming before implementation. For rendered HTML studies, prototypes or critiques use design-artifact-studio; this skill does not build working UI.
---

# UI Design Brainstorm

Help the user decide what the product experience should feel like and how its important work is understood. Deliver generated concepts, their exact prompts and a handoff that records the decision. A static comparison gallery is optional; it is not the product prototype. Do not automatically implement the chosen design.

## Start with the product, not the layout

Establish the audience, purpose, primary workflow and representative moment. Separate user facts from sample data and assumptions. Describe the few domain concepts that matter: what users create, inspect, change or approve, and what those actions mean. Make success observable: what should a person understand or decide from this screen?

When the user wants a familiar product category, choose relevant existing products or supplied references before inventing an art direction. Borrow useful experience patterns; do not let the subject of the content become the app's brand. Distinguish observed screens from marketing descriptions and assumptions. Inspect supplied reference images. Narrow research is useful when examples are missing; do not imply hands-on product testing from documentation.

Declare what this pass explores: workflow, information hierarchy, visual style, or a stated combination. Record what may vary, what must remain fixed, and the decision the alternatives should help the user make. Infer this from the brief when clear; clarify only when the answer would materially change the exploration.

Create a shared base prompt covering the product, workflow, essential domain rules, representative state and experience goals. Exact sample facts provide constraints against which generated states can be checked; prompting does not guarantee fidelity. Leave information architecture, layout and UI wording open where they are part of the exploration. Do not prescribe panel coordinates, dimensions or every visible feature by habit. Capabilities not needed for this moment can stay implicit.

Choose two or three directions that test meaningful alternatives on the declared exploration axis. When visual style is open, deal three directions with [references/divergence.md](references/divergence.md) before writing their prompts. Keep direction-specific instructions separate from the shared product prompt. Honor supplied themes and approved systems; do not turn one successful example into a universal preference. For appearance-only exploration of an approved layout, preserve its structure and use the same supplied visual reference across variants. Structural novelty is not required when structure is fixed.

## Generate and discuss

Read [references/native-images.md](references/native-images.md) before image calls. Use the host's image generation, or the Codex CLI bridge described there when the host has none; never ask for or store an API key. A pass is one exploration of one stated question. It starts when the user gives or changes the brief, the directions or the budget; context compaction and a generic “continue refining” do not start a new one. Normally start a pass with two concepts, or with the three dealt directions when the direction round applies, and keep a ceiling of five image calls per pass, counting edits, failures and retries. A number the user states for the pass replaces that ceiling. Record each call in `run.json` under its pass before submitting, so the count survives compaction, and check whether a slow call is still pending before sending it again. At the ceiling, deliver the existing options and say what a further pass would need.

Show the original images alongside exact prompts. Explain differences actually visible in the results, how they relate to the exploration axis, and which user decision they help evaluate. Do not infer diversity from prompt labels. If outputs converge, report that; reconsider the direction or references only if greater variation would help the stated decision.

Check visible content, claims and available actions against the supplied facts and current workflow state, including implied prior actions and derived explanations. Record contradictions for correction rather than treating painted details as requirements. Keep domain errors separate from taste. A screenshot does not establish interaction behavior, responsiveness, accessibility or operational correctness.

Give the user a real opportunity to select, combine or redirect concepts. A recommendation is not human approval. Record what was selected and what the user actually liked; do not infer blanket acceptance of every painted detail. If no selection was made, keep the result unselected.

Before another generation, state the unresolved question or material defect, the intended change, and the properties to preserve. Iterate within the remaining budget when the result could improve the decision or address requested feedback. Stop when the decision is sufficiently supported or another image would add little useful evidence; the five-attempt ceiling is not a target. Preserve earlier versions and move implementation-level corrections into the handoff instead of spending image attempts on minor typography.

## Finish with a usable handoff

Read [references/handoff.md](references/handoff.md). Keep everything in one folder, `outputs/<short-name>-concepts/` unless the project or the user names another place: `brief.md` (the product facts, the question this pass explores, and its directions), `prompts/`, the original images, `run.json` and `HANDOFF.md`, linked by relative paths. Write `HANDOFF.md` as soon as concepts exist, with status unselected, then stop for the user's selection and update it when they choose. Record selected status honestly, preservation priorities, required corrections and unresolved decisions. A concept may be useful even if its mistakes must be corrected in implementation; make those mistakes explicit.

When the user requests implementation, hand the selected image and brief to design-artifact-studio if available. Read its installed instructions at that point; do not copy its implementation or browser-testing responsibilities into this skill. If it is unavailable, leave a complete portable handoff and say so. The brainstorming result remains useful independently.

Stop after delivering the concepts and handoff unless the user also requested the downstream build. Summarize what changed, what was learned and any remaining decisions. Never change this or another reusable skill during an ordinary design run.
