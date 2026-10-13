---
id: agent-review
title: Tern, AI agent review screen
width: 1440
height: 900
frame: Each study must show the whole decision, including the proposed action, the draft reply, both points of uncertainty and the reviewer actions, within one 1440×900 view.
must_contain: £84.00 | Dana Whitlock | HW-20931 | keep the casserole | 2 April
---
"Tern" is a fictional AI agent that handles customer-support tickets for small online shops. It works through a ticket on its own and pauses when an action needs a person's approval. This is the Review screen: one paused run, waiting for a decision.

Audience and scene: a support lead at a desk with a large monitor, reviewing paused runs many times a day. Each decision should take 20 to 30 seconds. They need to see what the agent wants to do, why, what it checked, and where it is unsure, then approve, change or stop it. A wrong approval sends money and a message to a real customer.

Business objective: fewer wrong approvals without slower ones. Reviewers skim under time pressure and miss the agent's doubts; the shop wants each decision made in under 30 seconds and no refund paid that should not have been.

What these reviewers already use every day: a code review tool, and their bank's screen for approving payments.

Content (fictional; use exactly, and do not add data):
- Shop: Hallam & Wren, kitchenware. 4 runs are waiting for approval. This one has waited 6 minutes.
- Ticket #4127 from Dana Whitlock: "My enamel casserole arrived with a chip on the lid. Order HW-20931. I'd like a replacement lid, or a refund if that's not possible."
- Goal of the run: resolve ticket #4127.
- Steps so far, in order:
  1. Read the ticket. Done.
  2. Looked up order HW-20931: enamel casserole 24 cm, £84.00, delivered 9 March. Done.
  3. Checked the returns policy: damaged on arrival within 30 days allows a replacement part or a full refund; a photo is required. Done.
  4. Checked the customer's attachment: 1 photo, showing a chip on the rim of the lid. Done.
  5. Checked stock for the replacement lid, part L-24: out of stock, next delivery 2 April. Done.
  6. Proposed action, waiting for approval: refund £84.00 to the original payment method and send the reply below.
  7. Planned after approval: close the ticket and tag it "damaged on arrival".
- Why it paused: refunds over £50 need approval.
- Draft reply: "Hi Dana, I'm sorry the lid arrived chipped. We don't have a replacement lid in stock until 2 April, so I've refunded the full £84.00 to your original payment method. It should reach you in 3 to 5 working days. You're welcome to keep the casserole. Hallam & Wren support"
- Where the agent says it is unsure, two points:
  a. "The customer asked for a replacement lid first. It is out of stock until 2 April. I chose the refund instead of asking her to wait."
  b. "Telling her to keep the casserole is not covered by the policy. I added it because return shipping would cost more than the lid."
- Run facts: started 14:02, 41 seconds of work, 6 lookups.
- Reviewer actions: approve; edit the reply; change the action (for example, offer to wait for the lid); reject with a note; take over the ticket.
- Do not invent metrics, satisfaction scores, confidence percentages, model names or other tickets' details. The customer's photo is not supplied and must not be faked; it may be shown as a labelled placeholder.

Representative state for every study: nothing decided yet.
