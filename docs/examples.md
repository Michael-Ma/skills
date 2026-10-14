# Usage examples

These skills work independently. Use `design-artifact-studio` when you want a reviewable artifact or critique. Use `ui-design-brainstorm` when you want generated visual concepts before choosing a direction. Combining them is optional; brainstorming does not automatically authorize implementation.

The prompts below use **Alder**, a fictional research-library app, with invented sample content. Output paths are relative to your current project. Adapt the audience, content, constraints, and scope to your own brief.

## 1. Build a functional prototype directly

Paste this into a task where `design-artifact-studio` is available:

```text
Use $design-artifact-studio to create a functional HTML prototype for
Alder, a fictional research-library app for a small design team.

The primary task is to find a research note, inspect it, and mark it
for a team discussion. Design one library screen and a note detail view.

Use these fictional notes:
- Navigation interviews — Research — 8 Sep 2026 — 6 min read
- Search usability notes — Research — 10 Sep 2026 — 4 min read
- Workshop planning — Planning — 12 Sep 2026 — 3 min read
Write short sample excerpts and label the data as fictional in the
review notes. Do not invent customer endorsements or research outcomes.

Include search, topic filtering, note details, and a reversible
“Discuss with team” marker. Show marker changes in the library and
detail view. Simulate this locally; no message should be sent.
Include an understandable no-results state and a way to clear filters.

Choose a visual direction suited to sustained reading. Explain the
typography, hierarchy, and spacing choices. Support desktop and mobile.
Deliver a self-contained artifact in outputs/alder-prototype/ with a
short DESIGN.md. Inspect the rendered UI and exercise the promised
interactions, including keyboard access. Report any unverified checks.
```

The result should be a usable prototype with stated simulation limits. A successful interaction test does not establish visual quality; the rendered composition also needs review.

## 2. Explore concepts, then choose

`ui-design-brainstorm` needs an image tool: the host's own, or Codex's built-in tool reached through the `codex` CLI when the host has none. It never asks for an API key and does not switch providers silently. With neither available, it prepares a written brief and reports the image stage as blocked. Generation is not free or unlimited; through the Codex CLI it counts against your ChatGPT plan.

```text
Use $ui-design-brainstorm to explore the visual style of Alder,
a fictional research-library app for a small design team.

The representative screen is the library. Users scan notes, open one,
and mark it for a team discussion. Keep the information hierarchy fixed:
page title and search, topic filters, then a readable list of notes.
Each note shows its title, topic, date, reading time, and discussion marker.

Use the same three fictional notes in both concepts:
- Navigation interviews — Research — 8 Sep 2026 — 6 min read
- Search usability notes — Research — 10 Sep 2026 — 4 min read
- Workshop planning — Planning — 12 Sep 2026 — 3 min read
All discussion markers start off. Do not add metrics or endorsements.

Generate two concepts: a warm editorial direction and a precise,
restrained typographic direction. Explore typography, palette, spacing,
and component treatment while preserving the structure and content.

Save the original images, exact prompts, attempt record, and HANDOFF.md
in outputs/alder-concepts/. Show what actually differs between the
images and identify any incorrect content or states. Stop for my choice;
do not build an HTML prototype in this pass.
```

The images are conceptual. They do not prove working interactions, responsiveness, accessibility, or correct product behavior. An optional comparison gallery is a review aid, not the app.

## 3. Authorize implementation of a selected concept

After viewing the concepts, give a specific selection and a separate build instruction. Replace the choice below if you prefer another result:

```text
I select the warm editorial concept. Preserve its reading hierarchy,
warm neutral surfaces, and typographic character. This selection does
not approve any incorrect text or impossible states in the image.

Record that decision in outputs/alder-concepts/HANDOFF.md. Then use
$design-artifact-studio to build the selected direction in
outputs/alder-prototype/. Read the handoff and inspect its linked image.

Implement search, topic filtering, note details, and a reversible
“Discuss with team” marker with visible state changes. Keep data local
and make the simulation limits clear in review notes. Correct the
handoff's listed image defects. Adapt the layout for desktop and mobile
while preserving the qualities I selected. Verify the required actions,
recovery states, and keyboard access in the browser. Explain significant
departures from the concept and report checks that were unavailable.
```

The handoff carries intent and decisions; the builder still needs to resolve behavior and responsive layouts. A generated screen should not become a background image with invisible clickable hotspots.

## 4. Critique or refine a small existing surface

Run this in the relevant application repository. Identify the real screen or component if its location is ambiguous:

```text
Use $design-artifact-studio to critique the existing Library screen.
Inspect its implementation, rendered UI, and project design rules.
Focus on reading hierarchy, spacing, and the distinction between
primary content and metadata. Preserve the existing identity, framework,
navigation, and behavior. Do not propose a new product-wide visual style.

Deliver up to five concrete findings with their effect on the reader
and a suggested correction. This pass is critique only; do not edit files.
```

To authorize a subsequent refinement, follow with: “Apply findings 1 and 2 to the Library screen. Preserve the remaining design and behavior, inspect the affected views, and report what changed and what you verified.” A narrow change does not require a new concept exploration or an unrelated full-app test suite.

## 5. Leave the direction open and choose from three

When you have no look in mind, say so. The skill deals three directions, shows each as a static study, and stops:

```text
Use $design-artifact-studio for Alder's library screen. The goal is
that a researcher finds last month's note in under ten seconds. The
visual direction is open and I will choose it. Show me three directions for
the screen with the three fictional notes from example 1, all
discussion markers off. Do not build the working prototype yet.
```

The agent first notes how two or three note-taking apps lay out a library screen. Two directions keep that layout and the third, marked as the stretch, tries a different structure. Each comes with the values it was dealt, the card it carries and where that card came from, and one line on what it gains and risks. Stating an objective, a scene of use or comparable products gives the agent more to write cards from. Reply with a choice, a combination, a redirect, a card to add or strike, or “deal again”. Then authorize the build:

```text
I choose direction 2. Build the working prototype from that study in
outputs/alder-prototype/, with the interactions from example 1.
```

The build starts from the chosen study and reports where the working result departs from it. To skip the round, ask for one quick result or name the direction yourself.
