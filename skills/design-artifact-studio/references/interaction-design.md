# Design the task and its states

Apply this guidance to interactions within the promised scope and fidelity. A static study can illustrate states and disclose its limits without implementing flows merely to satisfy these patterns.

## Start from a concrete scenario

Write a compact sequence: entry state → user action → visible result → next useful action. Name the information required at each decision. Co-locate evidence and action when switching screens would create memory work. For a narrow component, keep the sequence equally narrow.

For a new multi-screen product flow, first identify what people work with, its user-facing terminology, where it belongs, and relevant navigation. Collection/detail/action is one useful structure, not a required architecture. Walk through one realistic task with actual content: can people find the starting point, use the necessary information, complete the action, and retain useful context? Remove needless steps before polishing screens. Preserve an existing product's terminology and navigation unless changing them is part of the brief.

Specify which state survives navigation, dismissal and reload when those transitions matter. Distinguish a draft from a committed result and the current input from an earlier output. Keep the information needed to verify a change near its result, such as a save destination, affected count, or updated record. Do not invent a backend or extra flow to satisfy a hypothetical future requirement.

Build only states that belong to the interaction. A static reading page does not need a fake loading spinner. A booking form needs a valid path and invalid-input recovery. A results list needs selected/filter state and zero results. A remote-operation prototype should label its simulation and preserve retry/cancel behavior if those are in scope.

## Controls tell the truth

- A button performs an action; a link navigates. A selected filter exposes its state semantically and visibly.
- Keep labels consistent across trigger, result, and recovery. Do not replace “Save draft” with ambiguous “Done.”
- Disable a control only when the reason is understandable. For inaccessible destinations in a prototype, provide context or omit the control.
- In local fixtures, update underlying state as well as the message. Preserve relationships: counts reflect filters, totals reflect selections, exports reflect the records shown or clearly name a broader scope.
- Do not manufacture network delays or success claims merely to display a loader.

## Task-specific patterns

**Forms:** Keep visible labels; preserve entered data on failure. Validate at a useful moment, associate errors with fields, and guide focus to the problem after failed submission. Clarify constraints before they cause an error. Make cancellation and draft behavior predictable.

**Tables and collections:** Match columns to the user's comparisons. Make sorting and filtering visible; describe count scope. Ensure selected-item details update together. Empty results explain how to recover. If a compact layout omits information, keep the data needed for the primary task accessible through detail or disclosure.

**Overlays:** Prefer inline editing when it keeps relevant context visible. When a modal is appropriate, use a native dialog or an established accessible component. Verify its name, initial focus, focus containment, Escape/close behavior, and focus return. Do not put important menus inside clipping containers. Test Tab from the final focusable control and Shift+Tab from the first, then Escape and focus return. Repeat after a state change that replaces controls. Native dialog semantics still need verification in the actual browser. For a nested picker or drawer, verify focus returns to the correct surviving opener.

**Charts:** Show units, time range, and enough context to interpret the comparison. Tie plotted marks and textual summaries to the same data. Provide an accessible summary or table. Do not add chart controls that leave the values unchanged.

**Creative tools:** Let users inspect the asset at useful size, preserve position during edits, and distinguish selected, pending, accepted, and failed work. Visual motion should reinforce manipulation or state, not make work appear active when it is idle.

## Small screens and access

Reorder by task importance while keeping DOM and visual order understandable. Collapse navigation only with an operable replacement. For wide data, choose an appropriate detail view or an explicitly scrollable data region; do not crop important columns or suppress page overflow to conceal a layout defect.

Support keyboard navigation, visible focus, readable contrast, and meaningful accessible names. Aim for comfortable touch targets (roughly 44 CSS pixels for primary mobile controls); distinguish this design target from formal conformance criteria. Do not rely only on color, hover, dragging, or animation to communicate or act. Honor reduced motion without removing content or feedback.

Test long names, no results, narrow widths, and repeat actions when relevant. Do not claim usability research or accessibility certification from a heuristic review.
