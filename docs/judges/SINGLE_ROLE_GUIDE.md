# One-role guide: raise a manager approval threshold

This scenario is **A. Try it yourself**. It is independent of the recorded four-role case (a different rule, baseline and run).

## Scenario summary
<dl class="summary">
<dt>Business objective</dt><dd>Let a requester raise the standard manager approval threshold in plain words and see, before anything is applied, what would change and what stays unresolved.</dd>
<dt>Baseline</dt><dd>Live <code>approval.yaml</code>: <code>standard_manager_threshold_jpy</code> = <strong>500,000 JPY</strong> (read 2026-10-13).</dd>
<dt>Proposed change</dt><dd>500,000 → <strong>800,000 JPY</strong>, in <code>approval.yaml</code> only. <strong>Proposed, not applied</strong>; a judge can never apply it.</dd>
<dt>Still unresolved</dt><dd><code>workflow.yaml</code>, <code>procurement_policy.md</code> (they state a manager limit of 1,000,000), <code>approval_matrix.xlsx</code> (rows around 500,000) and <code>requisition_sop.md</code> stay open as unresolved or potentially affected.</dd>
<dt>Measured (simulation, deterministic)</dt><dd>35 of 240 sample requisitions change, all NEEDS_MANAGER → AUTO. Separate from the AI's reading, which is an interpretation, not a measurement.</dd>
<dt>Verification status</dt><dd>
<span class="tag t-live">Recorded live result</span> exact request → confirmed understanding (1 AI job, no clarification).<br>
<span class="tag t-lim">Limitation</span> draft → proposal evidence comes from an <strong>earlier run with different wording and a manual fallback</strong>.<br>
<span class="tag t-nv">Not yet verified</span> the exact request through draft → proposal.</dd>
<dt>Acceptance</dt><dd>None. The run ends at <strong>Waiting for the approver</strong>; nothing is approved or applied.</dd>
</dl>

## Business problem
Harbor sends a standard purchase requisition to a **manager** only above a threshold. The configuration the program reads (`approval.yaml`) says **500,000 JPY**; `workflow.yaml` and `procurement_policy.md` say manager approval starts at **1,000,000 JPY**, and `approval_matrix.xlsx` has its own rows around 500,000. Changing the number is easy to say and hard to do safely: which requisitions change route, and which other statements disagree?

## Your mission
Act as a requester. State the change in plain words, make Ripple restate it, confirm it, and take it to a **proposal that waits for a reviewer and an approver**. You never apply anything.

## Baseline
> **Starting point.** This walkthrough uses a specific starting baseline. If earlier changes have been applied in this workspace, the sample values and expected results may no longer match. Check the current source revision and values before starting. For subsequent runs, follow the same workflow using the latest data.

**Snapshot used for the guided example:** read on **2026-10-16** from the server by the project team: source revision `rev-apply-ui-apply-dfcd1335eef248c0` (decision epoch 3, 13 files, no accepted knowledge revision), rule `routing_rules.standard_manager_threshold_jpy` = **500,000**, `routing_rules.capex_finance_threshold_jpy` = 1,000,000. This is a reading of that day, not a promise about the moment you start: check it yourself first (below).

This guide does **not** apply anything (a judge cannot), so following it never changes the source. The values here are the **guided example**. If the value you read in the Explorer is no longer 500,000, keep the same workflow, use the value you read as the "current value" in your request and a new value you choose; the simulation and the AI's wording will then differ from the example, which is expected.

- <span class="tag t-live">Recorded live result</span> `standard_manager_threshold_jpy` = **500,000**, `capex_finance_threshold_jpy` = 1,000,000 (read on 2026-10-13 through the AI's comparison with stored rules and the simulation's baseline check, and re-read before the exact-request check).
- <span class="tag t-lim">Limitation</span> The statements in `workflow.yaml` and `procurement_policy.md` (1,000,000) come from the Harbor bundle copy of those files, not from a fresh live read.
- Before you start, the page re-checks the baseline; if the workspace has moved, trust the numbers on screen.

## The request to type
@@REQUEST:Please raise the standard manager approval threshold from 500,000 JPY to 800,000 JPY in the approval configuration. Keep this change limited to approval.yaml and keep any other source that states a manager threshold visible as unresolved.@@

This is a **raise**: fewer requisitions will need a manager.

## Proposed change and simulated effect
@@BEFOREAFTER:manager@@

## What was run, and what was not
- <span class="tag t-live">Recorded live result</span> A judge account walked the whole path on the deployed UI on 2026-10-13: request → clarification → confirm → draft → impact → simulation → AI reading → proposal. It stopped at "waiting for the approver"; direct calls for extraction, review and apply were refused (403); no review/approve/apply button was shown; another judge account could not read the chat.
- <span class="tag t-lim">Limitation</span> That run typed a **different request** ("lower ... from 1,000,000 to 800,000") that used a wrong baseline. The AI correctly pointed out that the stored value is 500,000 and asked which is current; the second metered reply of that run repeated the wrong value, so the run used **"Edit the details myself"** (manual fallback) to continue. The fallback proves the rest of the path; it does **not** prove that the AI understands the request above.
- <span class="tag t-live">Recorded live result</span> The **exact request above** was then run through the AI by a second judge account (fresh conversation, 1 AI job, 1 provider call, 0.0155 USD, about 18 s). The AI returned a **READY** understanding with no clarification: subject standard manager approval threshold, **current 500,000 and new 800,000, both quoted from your words**, JPY. The sentence about limiting the change to `approval.yaml` and keeping other sources unresolved was **recorded as a note only - the system does not enforce it** (the page said "Applies to: not known yet"). The preview was confirmed and the run stopped there.
- <span class="tag t-nv">Not yet verified</span> Draft, impact, simulation, AI reading and proposal were **not** repeated with this exact request.

## Steps
Each card shows what to do and what to expect. Open **Observed result, evidence and caveats** for the recorded result of that step. Steps marked **AI** use the metered quota.

### Step 1 - Open Ripple and choose a change
- **Role:** judge (requester-like). **AI:** no.
- **Action** <span class="tag t-judge">Judge action</span>: open Ripple (button at the top), sign in with the judge account you were given, pick the workspace, then in the left menu open **Changes**. To start a **new** conversation arrive at **Changes from another page** (for example Overview, then Changes): there is no "New request" button, and clicking **Changes** while you are already on it only reloads the change that is open.
- **Expected:** the page shows "No change is selected" and your My work list (a chooser); the card **1. Request and confirmation** has an empty chat box and **Send**; there is no **Where this change is** card and no **Your request** card.
- **Continue when:** the address ends with `#/ws/<workspace>/changes` (no `chat=`, `intent=` or `draft=`). If an older change is shown, go to another page and back to **Changes**. Do not use **Open** in My work: it reopens an existing change.
- **Optional check of the baseline:** left menu → **Explorer** → type `approval.yaml` in **Search** → open the file, then the rule about the standard manager threshold. Its title reads like "Routing rules standard manager threshold jpy" (the AI named it after the key in the file, so wording can differ); recognise it by **Taken from: approval.yaml** and **Value** (500,000 expected; the Explorer shows no currency for it because the rule carries no unit: JPY is a separate rule of the same file, `currency`, and the key name ends in `_jpy`). "Applies to: unresolved: true" is normal. Technical view (top right) shows the current **Source revision** in the header. Quotes under "Where it came from" are hidden for a judge by design.
- **Observed** <span class="tag t-live">Recorded live result</span>: chooser visible on first load.
- **Caveat** <span class="tag t-lim">Limitation</span>: if AI steps are refused with "evaluation window", the service is not open; nothing is charged.

### Step 2 - Type the request and read the preview
- **Role:** judge. **AI:** yes, one metered reply.
- **Action** <span class="tag t-judge">Judge action</span>: copy the request above, paste it into the chat box and click **Send** (Enter in the box also sends at once; Shift+Enter adds a line).
- **Expected:** a card "This is what I understood": subject = standard manager approval threshold, current 500,000, new 800,000, JPY; the first line says nothing is recorded until you confirm.
- **Observed** <span class="tag t-live">Recorded live result</span>: exact request → READY card in about 18 s (worker already warm); the earlier, different request needed about 41 s including a cold worker start and two clarifications.
- **Caveat** <span class="tag t-lim">Limitation</span>: the "limit this change to approval.yaml" sentence is **recorded only, not enforced**.
- **Continue when:** the card heading is "This is what I understood" and current/new values read 500,000 and 800,000. Check the "from your words" lines under each value.
- **Optional branches (not the main path; each AI reply is metered):** if the heading is "I still need some details", answer with real data (for example "The current value is 500,000 JPY") in the **Your answer** box. If the AI cannot settle it, **Edit the details myself** → current 500000, new 800000 → **Check my edits** is deterministic (no AI) but is a fallback, not the intended path.

### Step 3 - Confirm
- **Role:** judge. **AI:** no.
- **Action** <span class="tag t-judge">Judge action</span>: two separate confirmations. (1) In the chat card click **Yes, this is what I mean**; a check box ("I have checked what the AI assumed and what is left out of this request") appears **only** when the AI listed assumptions or "not covered" items, and then must be ticked first. (2) The saved request has the status "Saved - waiting for the person who made it to confirm the request"; click **Confirm intent** in stage 1.
- **Expected:** after (1) a **Your request** card and a **Where this change is** card appear; after (2) stage 1 shows **Confirmed**.
- **Continue when:** the status reads **Confirmed**.
- **Observed** <span class="tag t-live">Recorded live result</span>: preview confirmed (exact request, conversation CONFIRMED). **Confirm intent** and later steps come from the earlier run: confirmed within seconds.

### Step 4 - Generate the draft
- **Role:** judge. **AI:** yes, one metered job.
- **Action** <span class="tag t-judge">Judge action</span>: stage 2 *AI draft with citations* → **Generate GenAI draft**.
- **Expected:** PARTIAL or COMPLETE; **one supported edit** (500,000 → 800,000); open points listed; no raw source text for your role.
- **Observed** <span class="tag t-live">Recorded live result</span> (earlier run): 15 s; PARTIAL; one edit; open items for `approval_matrix.xlsx` (shown as **potentially affected**), `workflow.yaml`, `procurement_policy.md`, `requisition_sop.md`.
- **Continue when:** the status reads Done, and one "Proposed edit" for `approval.yaml` shows 500000 → 800000. PARTIAL is expected: it means some parts stay with people.
- **Check:** nothing that the AI left out disappears; each open item has a kind (unresolved, potentially affected, outside this request).
- **Optional paths (not needed for the main path; each can use more AI):** **Revise this draft with confirmed feedback**, **Ask the AI to suggest** (per open point) and, in stage 3, **Ask the AI to look at up to 3 files**.
- **Caveat** <span class="tag t-nv">Not yet verified</span> with the exact request.

### Step 5 - Impact and simulation
- **Role:** judge. **AI:** no (deterministic).
- **Action** <span class="tag t-judge">Judge action</span>: stage 3 → **Run impact analysis**, then **Run simulation**.
- **Expected:** 240 requisitions, baseline reproduced, a count of changed requisitions.
- **Observed** <span class="tag t-live">Recorded live result</span>: impact 18 s, simulation 4 s: **35 changed (NEEDS_MANAGER → AUTO)**, 0 emergency rows; job `ui-simulation-98fb78b9e07e49c9`. <span class="tag t-off">Offline expectation</span> the same 35 from Harbor's shipped data.
- **Caveat** <span class="tag t-lim">Limitation</span>: the simulation runs Harbor's own program only; edits to `workflow.yaml`, documents or the workbook are not simulated.

### Step 6 - Read the AI's reading
- **Role:** judge. **AI:** yes, one metered job.
- **Action** <span class="tag t-judge">Judge action</span>: **Ask the AI to read this simulation (uses the paid model)**.
- **Expected:** a reading labelled "AI interpretation, not a measured fact", shown apart from the measures.
- **Observed** <span class="tag t-live">Recorded live result</span>: 26 s (earlier run).

### Step 7 - Build the proposal
- **Role:** judge. **AI:** no.
- **Action** <span class="tag t-judge">Judge action</span>: stage 4 → check that the `approval.yaml` line is ticked (proposed edits are ticked by default; clicking a ticked line un-ticks it) → **Prepare the proposal with the ticked edits**. One proposal covers one file; press it once.
- **Expected:** the exact diff of `approval.yaml`; "Left for people" lists the open items (not resolved by the proposal).
- **Observed** <span class="tag t-live">Recorded live result</span>: 5 s (earlier run).

### Step 8 - Stop: waiting for the approver
- **Role:** judge. **AI:** no.
- **Action:** none - read who is next, on the same Changes page.
- **Expected:** the **Next** card at the top reads "Waiting for: An approver (not the requester) must state the check after the change"; row **5. Check after the change** in **Where this change is** says Waiting; stage 5 shows "Suggested check (waiting for an approver)". My work lists the same item. No review, approve or apply button is offered.
- **Continue when:** nothing more for a judge. The proposal is **not applied**; the source file is unchanged.
- **Observed** <span class="tag t-live">Recorded live result</span>: exactly that (earlier run). **End of the guide.** To see what happens after a proposal, read the [recorded four-role case](VERIFIED_FOUR_ROLE_CASE.md) (a different change with its own baseline).

## Continued exploration (any later run)
The steps above are the **guided example**. They stay the same for any later run; only the values change.
1. Check the baseline first, even on your first visit: another person may already have applied a change (the four-role workflow does). Read the **Value** in the Explorer and, in Technical view, the **Source revision**.
2. Start a **new request** from **Changes** reached from another page. **My work** lists the items waiting for the account you are signed in with; do not open one that is not yours.
3. Use the **current** value as "from" and a new value of your choice as "to". Check the AI's preview before confirming: a wrong number means do not confirm.
4. Read the simulation of this run as it is; the number of changed cases depends on the values, and nothing here promises the numbers of the example (35 of 240 was one past reading).
5. The AI may ask a question, word things differently or leave items open. "Partly processed" and unresolved items are normal and are never treated as resolved.
6. If the source changed after your draft (someone applied), the page marks the draft out of date; ask for a new draft instead of using it.
7. Do not restore an earlier version to match an example. Limits you may meet: 12 AI jobs per account per day, 6 AI replies per conversation, a workspace-wide limit on jobs running at once (wait and press again), and the evaluation window (open until 2026-11-06 15:59:59 UTC). When one is used up Ripple refuses at once and charges nothing.
8. The one-role demo never applies anything, so it does not change the source. The optional [four-role workflow](four-role-replay.html) does.

## How to verify, independent of the AI's wording
Scope and values match your words; each claim has a status; sources you did not touch stay visible; numbers come from the measured simulation and the interpretation is labelled; raw quotes are hidden for your role; nothing after the proposal is offered to you.

## Supporting references
Measured timings are single samples, not guarantees: worker start about 6 s after a request; 14-23 s for a simple job; the Scheduler backstop recovered a missed wake-up in 178 s in one sample.
