# Brainstorm-to-artifact handoff

Create one `HANDOFF.md` as the entry point. It is a record of decisions, not a second implementation skill. Include the following information proportionately:

- **Status and authority:** unselected, user-selected, or chosen without a person in an unattended run. Include the user's actual selection statement or a reference to it, and after a direction round the seed and the directions shown. Name any subsequent changes. Never record your own recommendation, or anyone else's preference, as the user's approval.
- **Selected visual:** exact relative file path; where useful, link alternative versions and prompts. State its role in the builder's terms: an exact target, whose evidenced layout and proportions are to be preserved, or inspiration, with the qualities to carry named (composition, palette, type, mood). A concept can be an exact target for its composition and inspiration for the rest; say which.
- **Product contract:** audience, task, screen/state, exact fixture data, key domain rules, required interactions and important recovery paths. Label invented demo data and backend simulation.
- **Design intent and adaptation:** record the selected qualities, why they matter to the user task, and what the builder may adapt. Distinguish fixed constraints from flexible treatments, including relevant visibility priorities. Carry the purpose of the design across formats and viewports rather than requiring incidental geometry. Preserve exact structure when the user requires it; do not guess pixel tokens from a raster.
- **Correct:** an explicit list of hallucinated content, impossible states, misleading controls and other image defects the builder must not reproduce.
- **Resolve:** questions or states the image does not establish, including responsive behavior, keyboard use and error recovery. Distinguish a real blocker from choices the builder may make.
- **Assets and provenance:** original concept images, separate usable media assets and their roles. A full UI screenshot is not an asset to lay invisible hotspots over; painted text and embedded photos should not be extracted as if they were supplied production assets.
- **Build request:** only when authorized, name the requested implementation scope, format, viewports and observable acceptance outcomes. Otherwise mark implementation as not requested.

Requirements and explicit user decisions take priority over contradictory details in a generated image. Preserve its meaningful design choices while correcting domain errors and inaccessible treatments. Explain significant departures instead of either blindly copying the image or silently replacing it with the builder's default design.

Example invocation for a user-authorized build:
“Use design-artifact-studio to implement the selected direction in HANDOFF.md. Inspect the linked image, preserve the documented decisions, correct the listed defects and verify the required interactions. Do not start a new visual exploration unless a material conflict prevents implementation.”
