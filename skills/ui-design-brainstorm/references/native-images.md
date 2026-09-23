# Native image workflow

Use the current native image tool schema and tool instructions. In this environment it is `image_gen.imagegen` (or `tools.image_gen__imagegen` through orchestration). Do not invent model, quality, seed or destination arguments. No API key is required; usage/cost is unknown unless the tool reports it, not zero. If native generation is unavailable, deliver the written brief and report the image stage blocked rather than silently switching providers.

For independent concepts, send the shared product prompt plus one direction paragraph, omitting reference-image fields. If the user supplied visual references, use the live tool's supported mechanism and state each reference's role. For an edit, inspect the actual local target first, name the defect to change and the properties to preserve, and use that image as the target. Never supply both reference mechanisms or silently use an unrelated recent image.

Request a flat app screen for human review, without device hardware or a promotional presentation board unless asked. Preserve functional sample data across alternatives. Save prompts exactly as submitted; do not rewrite the saved prompt to match the output afterward.

Before each call append an attempt to `run.json`: id, kind, status=submitted, prompt path, parent/reference image roles if any. Update with actual result location, copied relative path, dimensions and status. Record unknown model/usage/cost as null. Resume pending calls on timeout; do not resubmit simply because generation is slow. Copy returned project images into the output folder and retain the originals.

Display the native result through its supported renderer. Inspect actual images before critique. Text and fine details may be uncertain; say so rather than manufacturing exact measurements. Keep every attempted concept and its findings. A quick static gallery can show originals and expand exact prompts; building an interactive product is outside this skill.
