# Skills

Reusable agent skills for exploring UI directions and turning design decisions into reviewable artifacts.

Start with a brief, explore the choices that are still open, and inspect the actual result. Preserve an existing product's identity and conventions. Visual craft and usable behavior each deserve their own review.

## The collection

| Skill | Use it for | What you get |
|---|---|---|
| [ui-design-brainstorm](skills/ui-design-brainstorm/SKILL.md) | Exploring visual direction before implementation | Generated concepts, exact prompts, critique, and a portable handoff with the selection status recorded |
| [design-artifact-studio](skills/design-artifact-studio/SKILL.md) | Creating, critiquing, or refining UI/UX artifacts | A critique, static study, or working prototype at the requested fidelity, with relevant review evidence |

Use either skill independently. When you want both, explore with `ui-design-brainstorm`, choose a direction, then ask `design-artifact-studio` to implement the selected handoff. Brainstorming does not automatically authorize an application build.

## Install

With Node.js available, use the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills@latest add Michael-Ma/skills
```

Choose the skills, target agent, and installation scope in the installer. To install one skill explicitly for Codex:

```sh
npx skills@latest add Michael-Ma/skills --skill design-artifact-studio --agent codex
npx skills@latest add Michael-Ma/skills --skill ui-design-brainstorm --agent codex
```

Add `--global` if you want a user-wide installation. To inspect the collection without installing:

```sh
npx skills@latest add Michael-Ma/skills --list
```

You can also ask Codex's built-in Skill Installer to install either folder:

```text
Use $skill-installer to install:
https://github.com/Michael-Ma/skills/tree/main/skills/design-artifact-studio
https://github.com/Michael-Ma/skills/tree/main/skills/ui-design-brainstorm
```

This repository distributes ordinary skill folders. It does not install a plugin, an image provider, browser tools, or a runtime. For Codex's skill format and installer behavior, see the [official skills documentation](https://learn.chatgpt.com/docs/build-skills).

## Try it

Create an artifact directly:

```text
Use $design-artifact-studio to design a reading-list app for a small research
team. Build a portable HTML prototype where someone can find an article,
inspect its details, and save it to a collection. Use fictional content.
Support desktop and mobile, and verify the implemented interactions.
Save it under outputs/reading-list/.
```

Explore before implementing:

```text
Use $ui-design-brainstorm to explore two visual directions for that reading-list
app: a restrained workspace and a warm editorial treatment. Use the same
representative content. Show the generated concepts and explain the visible
tradeoffs. Stop for my selection before implementation.
```

See [complete examples](docs/examples.md) for independent use, a selected-concept handoff, and a focused refinement of an existing interface.

## Capabilities and limits

- **UI Design Brainstorm requires native image generation in the host.** The instructions currently name Codex's native image tools. Installing the skill does not make those tools available. Without them, it can prepare a written brief but must report generation as blocked; it does not silently switch to an API-key workflow.
- **Design Artifact Studio needs the appropriate renderer for verified output.** For web artifacts, that means browser access. When rendering or a particular check is unavailable, the result must identify what remains unverified.
- **HTML is a fallback for portable interactive web prototypes.** Existing projects keep their framework and design system. Static studies and critiques need not become applications.
- **Generated UI images are concepts.** They do not demonstrate working interactions, responsive behavior, accessibility, or correct data. The implementation handoff records errors to correct and choices to preserve.
- These are instructions authored for Codex, packaged in the agent-skills folder format. Compatibility with other agents depends on their tools and instruction support; universal host compatibility and improved design quality are not claimed.

## Maintain the collection

Each skill lives in `skills/<name>/`, with its instructions in `SKILL.md` and supporting material loaded only when relevant. Add reusable principles to the skill; keep project-specific taste, generated artifacts, and benchmark fixtures outside it.

Run the packaging checks with Python 3.10 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

The same checks run in GitHub Actions. They check metadata and local file references, not heading anchors, visual taste, accessibility conformance, or behavior on unseen briefs. Evaluation across briefs is a separate activity from validating an individual artifact.

## Acknowledgments

The collection structure is inspired by [Matt Pocock's skills repository](https://github.com/mattpocock/skills). Its skill implementations are not copied here.

Design Artifact Studio's [research provenance](skills/design-artifact-studio/references/provenance.md) records the upstream projects and exact versions studied. Their runtimes, databases, and research snapshots are not bundled in this repository.

## License

[MIT](LICENSE).
