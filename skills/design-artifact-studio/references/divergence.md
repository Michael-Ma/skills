# Diverge before choosing

Use this when the visual direction is open and a person will choose it: a new surface with no existing system, selected concept or supplied target. A single pass produces a single answer, and for a given subject it is nearly always the same answer. Asked to pick its own alternatives, a model also returns the same few every time. Choosing needs real alternatives, so the distance between them is dealt, not chosen.

1. **Write down the default.** In five lines, state what you would build without thinking further: the governing metaphor, the canvas and ink, the type classification, the shape of the primary object, and how color is used. This is direction zero. It is a reference point and is not one of the options.
2. **Deal the axes.** Run `python3 scripts/draw_axes.py` from this skill's folder and record the seed it prints. It deals three sets of values for the axes below. No two sets share more than two values, and two positions come up `open`. Build each direction from its set as dealt. The deal exists to land somewhere you would not have chosen, so treat an unexpected combination as that direction's brief and find the version of it that serves the scene.
3. **Fill the open positions from the subject.** Where a set says `open`, supply a value that is not in the table and comes from this subject's own world: an artifact, notation, material, place or convention its audience already knows. Name it and say in one line why it belongs. This is where a direction gains something no other brief would have.

| Axis | Values in the deal |
|---|---|
| Structure of the primary object | list or table · grid of tiles · a continuous timeline or chart that is the interface · one focal item with the rest subordinate · map or diagram |
| Canvas | light neutral · dark · a saturated color field · white with one vivid hue |
| Type | condensed or signage sans · geometric or humanist sans · serif-led · monospace or tabular-led |
| Scale and density | compact reference · comfortable · poster-scale with few elements |
| Shape language | ruled and square · soft and rounded · heavy blocks and fills · fine line and diagram |
| Color | status only · one brand color carrying identity · several hues carrying categories |
| Source world | the subject's own print tradition · an instrument or control surface · signage and wayfinding · editorial or magazine · a consumer product from an unrelated category |

4. **Keep each one honest.** Every direction serves the same audience, scene, content and task, with the same representative content and state. When one dealt value cannot serve the scene at all, such as a canvas unreadable in the stated light, redraw that single axis once with `--axis "<name>" --exclude "<value>"` and note it. If a set matches direction zero on five or more axes, deal again. Never write a deal by hand. If the script cannot run, say so; the options you then show are chosen, not dealt, and are labelled that way.
5. **Show each at sketch cost.** Present each direction as one static view of the representative moment, without behavior: a rendered study, or a generated concept image when working from the image workflow. Name each in a few words. List the values it was dealt, the open values you supplied and any redraw, and add one sentence on what it gains and what it risks.
6. **Let the person choose.** Present the set and stop. They may pick one, combine several, redirect, or ask for another deal. Record the seed, the three directions, what they chose and what they said in the project's design record. A later deal for the same project starts from that record and leaves out combinations they have already seen.
7. **Build from the choice.** Where the chosen study is code, start the build from it. Carry its structure and visual language into the working result, and keep direction zero's choices out of the places where they picked something else. Say where the working result departs from the study and why.

When nobody is available to choose, as in an unattended run, deal as above, build the direction that best serves the scene, and record that the choice was yours.

Skip this for refinements, extensions of an existing system, briefs that already fix the direction, and requests for one quick result. In the last case, say that a direction round is available.
