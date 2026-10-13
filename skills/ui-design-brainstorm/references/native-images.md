# Image workflow

Check once, before writing prompts, which image medium is available, and use the first that applies:

1. The host's own image tool, with its current schema and tool instructions. In Codex this is the built-in image tool.
2. The [Codex CLI bridge](#codex-cli-bridge), when the host has no image tool and `codex login status` reports a logged-in session.

Record the medium in `run.json`. When neither is available, deliver the written brief with its directions and report the image stage blocked; design-artifact-studio can render the same directions as static studies. Do not ask for or store API keys, and do not switch image providers silently. Do not invent model, quality, seed or destination arguments. Usage and cost are unknown unless the tool reports them, not zero.

For independent concepts, send the shared product prompt plus one direction paragraph, with no reference image. If the user supplied visual references, attach them through the one mechanism the live tool documents for references, and state each reference's role in the prompt. For an edit, inspect the actual local target first, name the defect to change and the properties to preserve, and use that image as the target. Never let a call pick up an unrelated recent image.

Request a flat app screen for human review, without device hardware or a promotional presentation board unless asked. Preserve functional sample data across alternatives. Save prompts exactly as submitted; do not rewrite the saved prompt to match the output afterward.

Before each call append an attempt to `run.json`: id, kind, status=submitted, prompt path, parent/reference image roles if any. Update with actual result location, copied relative path, dimensions and status. Record unknown model/usage/cost as null. When a call is slow, check whether it is still pending or has already produced an image before submitting again. Copy returned images into the output folder and retain the originals.

Display the result through the host's supported renderer. Inspect actual images before critique. Text and fine details may be uncertain; say so rather than manufacturing exact measurements. Keep every attempted concept and its findings. A quick static gallery can show originals and expand exact prompts; building an interactive product is outside this skill.

## Codex CLI bridge

This reaches Codex's built-in image tool from a host that has none. No API key is involved, and usage counts against the person's ChatGPT plan, so make only the calls the budget allows.

1. Save the prompt to a file exactly as it will be submitted, and append the attempt to `run.json` with status `submitted`.
2. Write an instruction file that starts with `$imagegen`, asks for exactly one image from the prompt between two markers, passed as written, and asks for the reply to be only the absolute path of the PNG:

```text
$imagegen Use the built-in image_gen tool exactly once to generate one landscape image (3:2, or the closest size available) from the prompt between the markers. Pass the prompt as written, without rewriting or summarizing it. Do not run shell commands or edit files. When the image is done, reply with only the absolute path of the generated PNG.

<<<PROMPT
(the saved prompt)
PROMPT>>>
```

3. Run it with stdin closed. With stdin open the command waits for input indefinitely and generates nothing:

```sh
codex exec --skip-git-repo-check -C "<output folder>" -o "<output folder>/last-message.txt" "$(cat "<instruction file>")" < /dev/null > "<output folder>/codex.log" 2>&1
```

Add `-i <file>` to attach a reference image, and state its role in the prompt.

4. The image is written under `~/.codex/generated_images/<session id>/`; there is no destination argument. Read the path from `last-message.txt`, confirm the file exists and is new, copy it into the output folder, and keep the original.
5. Update the attempt with the copied relative path, dimensions and status. Record the driving model named in the log. Record image model, usage and cost as null unless the log reports them.

A call normally takes one to two minutes. Allow five before treating it as stalled, and look for a new image before submitting again. Each call is one attempt against the budget.
