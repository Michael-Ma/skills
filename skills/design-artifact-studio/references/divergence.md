# Diverge before choosing

Use this when the visual direction is open and a person will choose it: a new surface with no existing system, selected concept or supplied target. A single pass produces a single answer, and for a given subject it is nearly always the same answer. Asked to pick its own alternatives, a model also returns the same few every time. Choosing needs real alternatives, so the distance between them is dealt, not chosen, and what makes each one belong to this brief is written down before the deal.

1. **Write down the default.** State what you would build without thinking further: its governing metaphor, and the value you would reach for on each axis in the table below. This is direction zero. It is a reference point and is not one of the options.
2. **Write the subject cards.** Before dealing, write four to six cards. A card is one value for one axis that comes from this brief and is not listed in the table, with a note of its source. Draw on, in this order: the business objective the person stated; the scene of use; products or categories that do the same job for their users, in this market or another; and the subject's own world of artifacts, notation, materials and conventions. Write at least one card from each of these that the brief provides. Products and conventions the person names are sources to write cards from; a value the person asks for outright goes in as a card unchanged. From a comparable product take a convention, never a brand's look, and say whether the card comes from inspecting the product or from memory. Cards are written before the deal so that none is shaped to fit a set you have already seen.
3. **Deal.** Run `python3 scripts/draw_axes.py --card "<axis>=<value>"` from this skill's folder, with one `--card` for each card, and keep what it prints with the design record: the seed and the cards, in that order, reproduce the deal. It deals three sets of values for the axes below. No two sets share more than two values, the three never share a structure or a canvas, and each set carries one of your cards, picked at random, in place of the dealt value on that card's axis. Cards that are not dealt sit this round out. Build each direction from its set as dealt. The deal exists to land somewhere you would not have chosen, so treat an unexpected combination as that direction's brief and find the version of it that serves the scene. With fewer than three cards, a set without one shows `open` on one axis; write a card for that axis then, from the subject's own world.

| Axis | Values in the deal |
|---|---|
| Structure of the primary object | list or table · grid of tiles · a continuous timeline or chart that is the interface · one focal item with the rest subordinate · map or diagram |
| Canvas | light neutral · dark · a saturated color field · white with one vivid hue |
| Type | condensed or signage sans · geometric or humanist sans · serif-led · monospace or tabular-led |
| Scale and density | compact reference · comfortable · poster-scale with few elements |
| Shape language | ruled and square · soft and rounded · heavy blocks and fills · fine line and diagram |
| Color | status only · one brand color carrying identity · several hues carrying categories |
| Source world | the subject's own print tradition · an instrument or control surface · signage and wayfinding · editorial or magazine · a consumer product from an unrelated category |

Reading a deal:

- The subject is the work on the screen and the world of the people doing it, more than the product's brand or its technology.
- Dealt values set emphasis and never remove required content. Poster-scale means one element dominates and the rest is subordinate.
- Canvas is the ground; Color is what hue is allowed to mean on it. A saturated canvas can itself carry the status.
- “-led” names the face that carries the identity; a supporting face is allowed.
- An unrelated consumer product lends its conventions, such as packaging, labelling and tone, and never a brand's look.
- A card changes what is seen. Renaming a listed value does not count. A card may sit on any axis, Source world included.
- The subject's own print tradition is what this work looks like on paper: its forms, labels, slips, tables and notices.
- When comparing a set with direction zero, an axis where the default has no listed value does not match, and neither does a card's axis.
- Every direction takes its wording and detail from the subject on every axis, not only on its card's.

4. **Keep each one honest.** Every direction serves the same audience, scene, content and task, with the same representative content and state. When one dealt value cannot serve the scene at all, such as a canvas unreadable in the stated light, redraw that single axis once with `--axis "<name>" --exclude "<value>"` and note it. Cards are not redrawn. If a set matches direction zero on five or more axes, deal again with the same cards. Never write a deal by hand. If the script cannot run, say so; the options you then show are chosen, not dealt, and are labelled that way.
5. **Show each at sketch cost.** Present each direction as one static view of the representative moment, without behavior: a rendered study, or a generated concept image when working from the image workflow. Name each in a few words. List the values it was dealt, its card and where the card came from, and any redraw, and add one sentence on what it gains and what it risks.
6. **Let the person choose.** Present the set and stop. They may pick one, combine several, redirect, add or strike cards, or ask for another deal. Record the seed, the cards, the three directions, what they chose and what they said in the project's design record. A later deal for the same project starts from that record and leaves out combinations they have already seen.
7. **Build from the choice.** Where the chosen study is code, start the build from it. Carry its structure and visual language into the working result, and keep direction zero's choices out of the places where they picked something else. Say where the working result departs from the study and why.

When nobody is available to choose, as in an unattended run, deal as above, build the direction that best serves the scene, and record that the choice was yours.

Skip this for refinements, extensions of an existing system, briefs that already fix the direction, and requests for one quick result. In the last case, say that a direction round is available.
