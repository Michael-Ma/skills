# Skills

Reusable agent skills for exploring UI directions and turning design decisions into reviewable artifacts.

Start with a brief, explore the choices that are still open, and inspect the actual result. Preserve an existing product's identity and conventions. Visual craft and usable behavior each deserve their own review.

## The collection

| Skill | Use it for | What you get |
|---|---|---|
| [ui-design-brainstorm](skills/ui-design-brainstorm/SKILL.md) | Exploring visual direction as generated concept images, before implementation | Generated concepts, exact prompts, critique, and a portable handoff with the selection status recorded |
| [design-artifact-studio](skills/design-artifact-studio/SKILL.md) | Creating, critiquing, or refining UI/UX artifacts | A critique, static study, or working prototype at the requested fidelity, with relevant review evidence. When the direction is open, three directions to choose from first |

Use either skill independently. When you want both, explore with `ui-design-brainstorm`, choose a direction, then ask `design-artifact-studio` to implement the selected handoff. Brainstorming does not automatically authorize an application build.

## Choosing a direction

For a new surface whose look is open, both skills run a direction round before anything is built. They show three directions, each as a static study or a concept image, and stop for your choice. You can pick one, combine several, redirect, or ask for another set. Work inside an existing system, small changes, and requests for a single result ("just build it", a quick demo) skip the round and get one direction, with a note that a round is available.

The three directions are dealt by a small seeded script. For app and tool screens, the agent first looks at how two or three products in the category present the same screen. Products in one category share a layout and differ inside it, so the product deck keeps that usual layout in two directions and varies what leads, how each item reads, and one pattern borrowed from an app in another category; the third direction is a stretch with a different structure. Canvas, type and controls follow the category in all three. Brand-led pages, or a request for something bold, use an expressive deck. Before the deal, the agent writes a few cards from what you told it: your business objective, the scene of use, products that do the same job, and the subject's own world. Each direction then carries one of those cards, picked at random. The directions are not the model's own picks, and that is deliberate. In the author's rendered comparisons, a model choosing its own alternatives returned the same three looks on five different briefs. On the one brief where both were tried, the reviewer preferred the dealt set. That is one reviewer's judgment on a handful of briefs, not a benchmark.

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

- **UI Design Brainstorm needs an image tool.** It uses the host's own, or reaches Codex's built-in image tool through the `codex` CLI when the host has none, for example in Claude Code with Codex installed and logged in. Those calls count against your ChatGPT plan. With neither, it prepares a written brief and reports generation as blocked. It never asks for an API key and does not switch providers silently.
- **Design Artifact Studio needs the appropriate renderer for verified output.** For web artifacts, that means browser access. When rendering or a particular check is unavailable, the result must identify what remains unverified.
- **HTML is the default for portable interactive web prototypes.** Existing projects keep their framework and design system. Static studies and critiques need not become applications.
- **Generated UI images are concepts.** They do not demonstrate working interactions, responsive behavior, accessibility, or correct data. The implementation handoff records errors to correct and choices to preserve.
- **The direction round needs Python 3** to deal its directions. If the script cannot run, the skill says so and labels its options as chosen, not dealt.
- These are instructions authored for Codex and also exercised in Claude Code, packaged in the agent-skills folder format. Compatibility with other agents depends on their tools and instruction support; universal host compatibility and improved design quality are not claimed.

## Maintain the collection

Each skill lives in `skills/<name>/`, with its instructions in `SKILL.md` and supporting material loaded only when relevant. Add reusable principles to the skill; keep project-specific taste, generated artifacts, and benchmark fixtures outside it.

Run the packaging checks with Python 3.10 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

The same checks run in GitHub Actions. They check metadata, local file references, that files carried by both skills are identical, and that the direction deal keeps its constraints. They do not check heading anchors, visual taste, accessibility conformance, or behavior on unseen briefs. Evaluation across briefs is a separate activity from validating an individual artifact.

To see what an agent produces with these skills, run a brief through Codex or Claude Code with [evals/run.py](evals/README.md). It renders the three directions onto one sheet for you to judge, and checks that the recorded deal is the one the script dealt:

```sh
python3 evals/run.py run --runner codex --brief video-agent
```

## Acknowledgments

The collection structure is inspired by [Matt Pocock's skills repository](https://github.com/mattpocock/skills). Its skill implementations are not copied here.

Design Artifact Studio's [research provenance](skills/design-artifact-studio/references/provenance.md) records the upstream projects and exact versions studied. Their runtimes, databases, and research snapshots are not bundled in this repository.

## License

[MIT](LICENSE).
