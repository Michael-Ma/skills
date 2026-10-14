# Running the skills against briefs

The validator checks that the skills are well formed. These runs answer the question it cannot: what does an agent produce with them on a real brief? `run.py` hands a brief to an agent CLI together with `design-artifact-studio` from this repository, waits for it to finish a direction round, and renders the three directions onto one sheet for a person to look at.

Use it to see the same brief through Codex and through Claude Code, or to compare the skill before and after a change.

The five briefs cover different kinds of surface:

| Brief | Surface | Size |
|---|---|---|
| `video-agent` | Reviewing an AI director's keyframes in a conversational video studio before it makes video | Desktop 1440×900 |
| `b2b-order-guide` | A restaurant's late-night order in a wholesale distributor's portal | Laptop 1280×800 |
| `train-tickets` | Choosing a train in a consumer ticket app | Phone 390 wide |
| `launch-board` | Deciding which rental slots to offer, at a counter in daylight | Tablet 1180×820 |
| `landing` | A service's landing page, read by a wary office manager | Desktop 1440 wide |

The skill should deal the first four from its product deck and may choose the expressive deck for `landing`, a brand-led page. `deal.txt` records which deck it used. In the product deck two directions keep the category's usual layout and the third is a stretch; the sheet marks the stretch. Each brief names a few real products in its category, and the agent may search the web to look at them before dealing (Codex runs with `--search`, Claude with `WebSearch` and `WebFetch`).

## Run

```sh
python3 evals/run.py run --runner codex --brief video-agent
python3 evals/run.py run --runner claude --brief video-agent
python3 evals/run.py run --runner codex --all --dry-run
```

`--runner` is `codex` (uses `codex exec`) or `claude` (uses `claude -p`). `--brief` names a file in [briefs](briefs/) and can be repeated; `--all` runs every brief, one after another. `--dry-run` prints the commands and stops. `--model` asks the CLI for a specific model, and `--label` adds a suffix to the run folder's name.

Each brief gets a folder, `evals/out/<time>-<runner>/<brief>/`, which is ignored by git. The agent writes its three studies, `DESIGN.md` and `deal.txt` there. The runner adds `_eval/`:

| File | What it is |
|---|---|
| `sheet.png` | The three directions side by side. Start here. |
| `direction-1.png` … `direction-3.png` | Each study, rendered by the runner at the brief's size |
| `result.json` | Runner, model, tokens, duration, exit status and every check. For Claude it adds `cost_usd`, the CLI's estimate at API prices; on a Claude subscription nothing is billed and the run counts against the plan's usage limits |
| `agent.log`, `agent.err`, `last-message.txt`, `prompt.txt` | What the agent was told, what it printed, its warnings (Claude only) and its final reply |

It needs Python 3.9 or newer, Google Chrome or Chromium, and the chosen CLI installed and logged in. Set `CHROME` to the browser's path if it is not found.

### With any other agent

The two CLIs are a convenience. To use an agent the runner cannot start, such as a desktop app, or when a CLI's login has expired, print the prompt, give it to the agent, and check the folder afterwards:

```sh
python3 evals/run.py prompt --brief video-agent --dir /path/to/folder
python3 evals/run.py check /path/to/folder --brief video-agent --runner codex-app
```

`check` runs the same checks and renders the same sheet. An agent run this way needs to be able to start Chrome itself if it is to look at its own renders; the render queue is served only while `run` is running.

## What is checked, and what is left to you

The script checks only what a script can:

- **files**: three studies, `DESIGN.md` and `deal.txt` exist.
- **deal**: every deal recorded in `deal.txt` is exactly what `draw_axes.py` prints for the seed, deck, usual structure and cards it names. A deal written by hand, or sets edited after the fact, fail here. So does a deal made with an earlier version of the script, since a seed reproduces only under the version that dealt it.
- **calibration**: `DESIGN.md` names at least one of the products on the brief's "Products in this category" line.
- **content**: each study contains the strings listed in the brief's `must_contain`.
- **self-contained**: a study loads nothing from outside except Google Fonts.
- **renders**: each study renders at the brief's size.
- **distinct**: no two studies read as one layout. The skill runs [likeness.py](../skills/design-artifact-studio/scripts/likeness.py) on its own renders before showing a set; the eval runs it again on the runner's renders. It maps where each render's content sits, ignoring color and tone, aligns the two pages band by band so looser or tighter spacing still matches, and scores 0 to 1. A pair at 0.86 or more fails. The threshold comes from the author's own runs: it caught five of eight pairs judged to be one layout and wrongly flagged one of 45 judged distinct. Treat a failure as a prompt to look, and a pass as no guarantee.

Whether the directions are any good, whether they differ, and which one you would pick are for a person to judge from the sheet. A run that passes every check can still be dull.

## Compare runs

```sh
python3 evals/run.py compare evals/out/<run-a>/video-agent evals/out/<run-b>/video-agent --blind
```

This puts the directions from several runs on one sheet. With `--blind` they are shuffled and labelled A, B, C, and the mapping is written to `mapping.txt` without being printed. Judge first, then open it.

## Cost and safety

- A direction round takes an agent roughly twenty to thirty minutes per brief. Codex runs count against your ChatGPT plan and Claude runs against your Claude plan.
- Codex runs in its `workspace-write` sandbox, where Chrome cannot start. The agent still gets to look at its work: `tools/shot.sh` leaves a request in the run folder's `.render-queue`, and `run.py`, outside the sandbox, renders it and writes the image back. The runner renders only files inside that run folder.
- The Claude runner allows shell commands, file edits and web lookups without asking (`--permission-mode acceptEdits` with `Bash`, `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebSearch` and `WebFetch`). Codex runs with live web search. Run only briefs you trust.
- The agent is told to use the skill copy in this repository and to ignore any installed copy. An installed older copy with the same name can still be picked up by the CLI; check `agent.log` if a result looks like the old behavior.

## Add a brief

A brief is a Markdown file in [briefs](briefs/) with front matter and the brief itself:

```text
---
id: video-agent
title: Cutline, video agent clip review
width: 1440
height: 900
frame: Each study must show the clip preview, the edit timeline, both points of uncertainty and the reviewer actions within one 1440×900 view.
must_contain: Daniel Kraus | merino | 14:18
---
(product, audience and scene, business objective, what the audience already uses, products in this category, exact content, representative state)
```

`width` and `height` are the size each study is rendered at. `frame` is the sentence that tells the agent what must fit in that frame. `must_contain` lists exact strings, separated by `|`, that every study has to show. State a business objective, the scene of use and what the audience already uses: the skill writes its subject cards from those. Add a line `Products in this category: A, B, C` naming real products that present the same screen; the skill calibrates against them, and the calibration check looks for them in `DESIGN.md`. Say that standard app chrome is allowed, or "do not add data" can read as forbidding a navigation bar. Keep the product and its content fictional.
