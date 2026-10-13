# Evidence-based design review

## Plan the checks around the artifact

Define the intended outcome and choose checks for the actual medium, fidelity, and features. For functional UI, test the primary task, recovery paths needed by the promised interaction, and supported layouts and input methods. A missing required error, empty, or recovery state is a gap, not a reason to exclude the check. For a static study, check content, composition, legibility, and output integrity. For a critique, inspect the supplied surface and distinguish observation from inference; implementing a replacement is not required.

For a responsive web artifact whose supported range is unspecified, default to desktop and narrow mobile. An explicit desktop-only scope or fixed-format visual study does not require a responsive redesign. Viewports around 1360–1440 and 360–390 pixels usually expose the largest differences; include an intermediate width when layout changes there. Check text enlargement or zoom when it can affect the flow.

Before implementation or a substantial refinement, list the critical outcomes and transitions within scope. After an action, inspect the state the user actually reaches. The result and any necessary confirmation must be perceptible and sufficient to verify the outcome. If an overlay stays open, check feedback in its active layer; if it closes, check the destination and focus/context restoration. Test cancellation, invalid input, and recovery when the promised interaction needs them; do not invent unrelated flows to satisfy the checklist. A narrow edit needs checks for its affected path, not an exhaustive matrix of the application.

Use browser tools for web artifacts and the appropriate preview or renderer for other formats. A source scan or zero console errors does not establish a good layout. Save representative captures when useful, and actually view them. Never describe a mock log or intended check as an executed test.

## Inspect the visible result

1. **Purpose and hierarchy:** What attracts attention first? Is the intended content, experience, or task clear? When an action is needed, is the information for it nearby? A reading or contemplative surface need not invent a call to action.
2. **Composition and visual craft:** Inspect type relationships, proportions, alignment, wrapping, density, spacing rhythm, color relationships, image crops, and clipping. Compare mobile task order with desktop when both are supported. Inspect every delivered direction or theme; changed token declarations do not prove that rendered foregrounds and backgrounds changed together. Assess coherence and brief fit separately from whether controls work.
3. **Interaction, when implemented:** Use the controls, confirm visible and underlying data agree, and check relevant repeat, zero/invalid, and recovery states. Follow navigation within scope.
4. **Access:** Inspect readable text, meaningful structure, and actual contrast pairs. For interactive UI, check keyboard access, focus visibility, names/labels, status announcements, and modal behavior where present. Check reduced motion when movement is included.
5. **Artifact integrity:** Confirm assets load, required content has no undeclared service dependency, and the delivered file works as described in its actual medium. For web artifacts, review console errors and broken resources.

Where overlays exist, check their actual bounds as well as document overflow. Feedback needed while a modal, drawer, or popover remains open must be visible in the active layer, not merely present in the DOM. Closing the overlay can be the correct outcome; inspect the resulting view instead of requiring it to stay open.

Match reference comparison to its declared role. For an exact target, compare evidenced layout, proportions, typography, content, and behavior at the relevant state. For an existing system, check consistency with its rules. For inspiration, assess only the qualities chosen for this brief. For source content, check content or asset fidelity without imposing its layout. Correct consequential mismatches and label adaptations or unobserved states; do not claim fidelity beyond the evidence.

When mobile interaction is supported, include its secondary and recovery controls in the review: inspect hit areas, text size, and overlap with content. Keep essential simulation or price disclosures near the relevant action; put research and implementation notes in review context, without requiring a new in-product panel. Where controls are fixed, confirm final content can scroll clear of them.

For dense text, fixed-height controls or sticky UI, try enlarged text or browser zoom through 200% and recheck the task. Include a realistic long label or record where wrapping affects the decision. Record the mechanism and effective viewport: CSS scaling, viewport resizing and device-pixel ratio changes are not interchangeable with browser zoom. Treat any approximation as limited evidence, not an accessibility conformance result.

A browser automation check can detect layout overflow or state mismatches; it cannot certify taste, accessibility, or product-market fit. Keep the evidence labels precise.

## Make the review actionable

Record only material observations in a small `VALIDATION.md`, for the same work that gets a `DESIGN.md`. Select applicable rows; these examples do not require adding missing features:

| View or action | Expected | Observed | Evidence / status |
|---|---|---|---|
| Primary task | Concrete result | What actually happened | Screenshot or browser observation |
| Recovery | User can continue | Actual behavior | Passed / fixed / unresolved |
| Mobile | Essential content and actions remain usable | Actual wrapping and layout | Viewport and capture |
| Static visual study | Coherent, legible composition that fits the brief | Observed visual relationships | Render and critique |

Separate functional defects, visual hierarchy problems, and optional taste choices. Fix consequential defects together, then recheck the affected states. If a review reveals a new meaningful problem, address it; do not keep rebuilding once only speculative polish remains.

Keep failures discovered outside the planned checks visible in the verdict. A passing check count does not establish that all required outcomes work. For an unresolved material issue, name the affected task and viewport rather than calling the artifact complete. Preserve untested conditions as unverified; do not average a blocked workflow away with attractive screenshots.

For a design exploration, compare alternatives on brief fit, clarity, visual craft, and coherence. Consider distinctiveness when identity is part of the brief and implementation cost when relevant to the decision. Explain tradeoffs with evidence rather than assigning an invented “9.8/10” score. A first-person heuristic walkthrough is not feedback from actual users.

If rendering is unavailable, deliver the artifact with that limitation. Name exactly which checks were and were not performed. Never mark an untested state as passing.
