# Portable HTML delivery

## Choose the smallest suitable package

For a standalone prototype, prefer `index.html` containing semantic markup, embedded CSS, and small inline JavaScript. It should open directly without a build or account. Avoid module imports, runtime CDN frameworks, and `fetch()` of adjacent files if direct file opening is promised. Embed fixture data or use a conventional script.

When actual imagery or font files materially improve the result, ship a folder containing the HTML and local assets, plus a ZIP if useful. Check every referenced path. Preserve asset licenses and attribution where applicable. Do not advertise a self-contained single file when it requires a network connection or neighboring assets.

A working application repository is a different delivery context: use the established stack and start instructions. Do not install a second framework just to produce a design preview. Use browser print/PDF or SVG only when they suit the requested decision; do not trade away required interactions for a static screenshot.

## Implementation choices

- Include a language, descriptive title, viewport metadata, sensible landmarks, and heading hierarchy.
- Use semantic CSS custom properties for color, spacing, type, controls, and layers. Give components meaningful classes. Keep local edits from accidentally changing unrelated components.
- Use content-driven Grid/Flex layouts with shrinkable text children (`min-width: 0`) and wrapping for long values. Avoid fixed page widths and blanket overflow suppression.
- Keep essential content visible without entrance animation. Reserve image dimensions to avoid reflow. Use system fonts intentionally or load bundled fonts with a fallback.
- Use inline SVG for simple diagrams, charts, maps, or icons when it is the correct medium. Label informative SVG; hide decorative icons from assistive technology. Do not substitute an abstract diagram for a photographic deliverable the user requested.
- Use explicit local state for filters, selection, form results, and counters. Insert user-provided strings as text, not HTML. Native controls are often sufficient and easier to verify.
- If storage is useful, describe whether changes survive reload and handle storage being unavailable. Avoid unnecessary persistence for a one-off interaction study.
- Offer export only when it produces an actual useful file. If exporting CSV from arbitrary text, preserve quoting and neutralize spreadsheet formula-like input; do not attach an export button merely as decoration.
- Scope print styles to the reading/export need. Remove controls that make no sense on paper while keeping essential content and any sample-data disclosure.

## Keep review tools outside the product

A separate review page may contain viewport controls, direction switching, rationale, and validation notes. Inside the prototype, use the language of its actual users. Add only the prototype disclosure needed to avoid confusion about sample data or simulated actions. Do not turn internal terms such as “semantic token system” into product copy.

## Handoff

Use a real absolute file link and show the artifact in the available viewer. If a local server was needed for inspection, the final artifact should still meet its promised portability. State how to open it and which interactions are implemented. A screenshot is supporting evidence, not a replacement for a requested HTML file.
