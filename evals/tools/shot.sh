#!/bin/sh
# Render a local HTML file in headless Chrome and write a PNG.
# usage: sh shot.sh <absolute path to .html> <absolute path to out.png> [width=1180] [height=820] [steps]
# steps: "|"-separated, run before capture: click:<text prefix>[@n]  fill:<css>::<text>  key:<Key>  scroll:<y>
#        gray: renders the page without color
# Widths below 500 are framed at the left of a 500px-wide image (grey fills the rest).
#
# While evals/run.py is running an agent, a ".render-queue" folder exists above the output path, and
# every request goes there: run.py renders it outside the agent's sandbox. Chrome is not started
# here first, since inside a sandbox it aborts and leaves a macOS crash report behind.
here=$(cd "$(dirname "$0")" && pwd)
src="$1"; out="$2"; w="${3:-1180}"; h="${4:-820}"; steps="${5:-}"
[ -n "$src" ] && [ -n "$out" ] || { echo "usage: sh shot.sh <abs .html> <abs out.png> [width] [height] [steps]"; exit 2; }
[ -f "$src" ] || { echo "no such file: $src"; exit 1; }

chrome="${CHROME:-}"
for candidate in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome chromium chromium-browser; do
  [ -n "$chrome" ] && break
  if [ -x "$candidate" ]; then chrome="$candidate"
  elif command -v "$candidate" >/dev/null 2>&1; then chrome=$(command -v "$candidate"); fi
done
python=/usr/bin/python3; [ -x "$python" ] || python=python3

direct() {
  [ -n "$chrome" ] || return 1
  ww=$w; [ "$ww" -lt 500 ] && ww=500
  enc() { "$python" -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"; }
  prof=$(mktemp -d "${TMPDIR:-/tmp}/shot-profile.XXXXXX") || return 1
  url="file://$here/harness.html?src=$(enc "file://$src")&w=$w&h=$h&do=$(enc "$steps")"
  rm -f "$out"
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --no-first-run --disable-web-security \
    --allow-file-access-from-files --user-data-dir="$prof" --window-size="$ww,$h" \
    --virtual-time-budget=8000 --screenshot="$out" "$url" >/dev/null 2>&1
  rm -rf "$prof"
  [ -s "$out" ]
}

find_queue() {
  d=$(dirname "$out")
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    [ -d "$d/.render-queue" ] && { echo "$d/.render-queue"; return 0; }
    d=$(dirname "$d")
  done
  return 1
}

queue=""
[ -z "$SHOT_DIRECT" ] && queue=$(find_queue)
if [ -z "$queue" ]; then
  if direct 2>/dev/null; then echo "wrote $out (viewport ${w}x${h})"; exit 0; fi
  echo "render failed: Chrome could not start here and no render queue was found"; exit 1
fi

id="$$-$(date +%s)"
printf '%s\n%s\n%s\n%s\n%s\n' "$src" "$out" "$w" "$h" "$steps" > "$queue/$id.tmp" && mv "$queue/$id.tmp" "$queue/$id.req"
waited=0
while [ "$waited" -lt 120 ]; do
  if [ -f "$queue/$id.ok" ]; then rm -f "$queue/$id.ok"; echo "wrote $out (viewport ${w}x${h}, rendered outside the sandbox)"; exit 0; fi
  if [ -f "$queue/$id.err" ]; then cat "$queue/$id.err"; rm -f "$queue/$id.err"; exit 1; fi
  sleep 1; waited=$((waited + 1))
done
echo "render failed: no answer from the render queue within 120 s"; exit 1
