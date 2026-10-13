# Running the skills against briefs

The validator checks that the skills are well formed. These runs answer the question it cannot: what does an agent produce with them on a real brief? `run.py` hands a brief to an agent CLI together with `design-artifact-studio` from this repository, waits for it to finish a direction round, and renders the three directions onto one sheet for a person to look at.

Use it to see the same brief through Codex and through Claude Code, or to compare the skill before and after a change.

## Run

```sh
python3 evals/run.py run --runner codex --brief agent-review
python3 evals/run.py run --runner claude --brief agent-review
python3 evals/run.py run --runner codex --all --dry-run
```

`--runner` is `codex` (uses `codex exec`) or `claude` (uses `claude -p`). `--brief` names a file in [briefs](briefs/) and can be repeated; `--all` runs every brief, one after another. `--dry-run` prints the commands and stops. `--model` asks the CLI for a specific model, and `--label` adds a suffix to the run folder's name.

Each brief gets a folder, `evals/out/<time>-<runner>/<brief>/`, which is ignored by git. The agent writes its three studies, `DESIGN.md` and `deal.txt` there. The runner adds `_eval/`:

| File | What it is |
|---|---|
| `sheet.png` | The three directions side by side. Start here. |
| `direction-1.png` … `direction-3.png` | Each study, rendered by the runner at the brief's size |
| `result.json` | Runner, model, duration, exit status and every check |
| `agent.log`, `last-message.txt`, `prompt.txt` | What the agent was told, what it printed and its final reply |

It needs Python 3.9 or newer, Google Chrome or Chromium, and the chosen CLI installed and logged in. Set `CHROME` to the browser's path if it is not found.

### With any other agent

The two CLIs are a convenience. To use an agent the runner cannot start, such as a desktop app, or when a CLI's login has expired, print the prompt, give it to the agent, and check the folder afterwards:

```sh
python3 evals/run.py prompt --brief agent-review --dir /path/to/folder
python3 evals/run.py check /path/to/folder --brief agent-review --runner codex-app
```

`check` runs the same checks and renders the same sheet. An agent run this way needs to be able to start Chrome itself if it is to look at its own renders; the render queue is served only while `run` is running.

## What is checked, and what is left to you

The script checks only what a script can:

- **files**: three studies, `DESIGN.md` and `deal.txt` exist.
- **deal**: every deal recorded in `deal.txt` is exactly what `draw_axes.py` prints for the seed and cards it names. A deal written by hand, or sets edited after the fact, fail here. So does a deal made with an earlier version of the script, since a seed reproduces only under the version that dealt it.
- **content**: each study contains the strings listed in the brief's `must_contain`.
- **self-contained**: a study loads nothing from outside except Google Fonts.
- **renders**: each study renders at the brief's size.

Whether the directions are any good, whether they differ, and which one you would pick are for a person to judge from the sheet. A run that passes every check can still be dull.

## Compare runs

```sh
python3 evals/run.py compare evals/out/<run-a>/agent-review evals/out/<run-b>/agent-review --blind
```

This puts the directions from several runs on one sheet. With `--blind` they are shuffled and labelled A, B, C, and the mapping is written to `mapping.txt` without being printed. Judge first, then open it.

## Cost and safety

- A direction round takes an agent roughly twenty to thirty minutes per brief. Codex runs count against your ChatGPT plan and Claude runs against your Claude plan.
- Codex runs in its `workspace-write` sandbox, where Chrome cannot start. The agent still gets to look at its work: `tools/shot.sh` leaves a request in the run folder's `.render-queue`, and `run.py`, outside the sandbox, renders it and writes the image back. The runner renders only files inside that run folder.
- The Claude runner allows shell commands and file edits without asking (`--permission-mode acceptEdits` with `Bash`, `Read`, `Write`, `Edit`, `Glob` and `Grep`). Run only briefs you trust.
- The agent is told to use the skill copy in this repository and to ignore any installed copy. An installed older copy with the same name can still be picked up by the CLI; check `agent.log` if a result looks like the old behavior.

## Add a brief

A brief is a Markdown file in [briefs](briefs/) with front matter and the brief itself:

```text
---
id: agent-review
title: Tern, AI agent review screen
width: 1440
height: 900
frame: Each study must show the whole decision within one 1440×900 view.
must_contain: £84.00 | Dana Whitlock | HW-20931
---
(product, audience and scene, business objective, what the audience already uses, exact content, representative state)
```

`width` and `height` are the size each study is rendered at. `frame` is the sentence that tells the agent what must fit in that frame. `must_contain` lists exact strings, separated by `|`, that every study has to show. State a business objective, the scene of use and what the audience already uses: the skill writes its subject cards from those. Keep everything fictional.
