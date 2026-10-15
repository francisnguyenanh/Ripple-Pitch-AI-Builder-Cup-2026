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
- **Action** <span class="tag t-judge">Judge action</span>: open Ripple (button at the top), sign in with the judge account you were given, pick the workspace, open **Changes**.
- **Expected:** "No change is selected" and your My work list (a chooser).
- **Observed** <span class="tag t-live">Recorded live result</span>: chooser visible on first load.
- **Caveat** <span class="tag t-lim">Limitation</span>: if AI steps are refused with "evaluation window", the service is not open; nothing is charged.

### Step 2 - Type the request and read the preview
- **Role:** judge. **AI:** yes, one metered reply.
- **Action** <span class="tag t-judge">Judge action</span>: copy the request above, paste it into the chat box and press **Send**.
- **Expected:** a card "This is what I understood": subject = standard manager approval threshold, current 500,000, new 800,000, JPY; the first line says nothing is recorded until you confirm.
- **Observed** <span class="tag t-live">Recorded live result</span>: exact request → READY card in about 18 s (worker already warm); the earlier, different request needed about 41 s including a cold worker start and two clarifications.
- **Caveat** <span class="tag t-lim">Limitation</span>: the "limit this change to approval.yaml" sentence is **recorded only, not enforced**.
- **If the AI asks a question:** answer with real data (for example "The current value is 500,000 JPY"). Do not restate a value you have not checked. Each reply is metered.
- **Fallback:** if the AI cannot settle it, **Edit the details myself** → current 500000, new 800000 → **Check my edits**. Deterministic, no AI; a fallback, not the intended path.

### Step 3 - Confirm
- **Role:** judge. **AI:** no.
- **Action** <span class="tag t-judge">Judge action</span>: tick the acknowledgement, **Yes, this is what I mean**, then **Confirm intent**.
- **Expected:** a saved request; stage 1 shows done.
- **Observed** <span class="tag t-live">Recorded live result</span>: preview confirmed (exact request, conversation CONFIRMED). **Confirm intent** and later steps come from the earlier run: confirmed within seconds.

### Step 4 - Generate the draft
- **Role:** judge. **AI:** yes, one metered job.
- **Action** <span class="tag t-judge">Judge action</span>: stage 2 *AI draft with citations* → **Generate GenAI draft**.
- **Expected:** PARTIAL or COMPLETE; **one supported edit** (500,000 → 800,000); open points listed; no raw source text for your role.
- **Observed** <span class="tag t-live">Recorded live result</span> (earlier run): 15 s; PARTIAL; one edit; open items for `approval_matrix.xlsx` (shown as **potentially affected**), `workflow.yaml`, `procurement_policy.md`, `requisition_sop.md`.
- **Check:** nothing that the AI left out disappears; each open item has a kind (unresolved, potentially affected, outside this request).
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
- **Action** <span class="tag t-judge">Judge action</span>: stage 4 → tick the proposed edit → **Prepare the proposal with the ticked edits**.
- **Expected:** the exact diff of `approval.yaml`; "Left for people" lists the open items (not resolved by the proposal).
- **Observed** <span class="tag t-live">Recorded live result</span>: 5 s (earlier run).

### Step 8 - Stop: waiting for the approver
- **Role:** judge. **AI:** no.
- **Action:** none - read who is next.
- **Expected:** My work shows "Needs the check that must hold after the change - an approver (not the requester)". No review, approve or apply button is offered.
- **Observed** <span class="tag t-live">Recorded live result</span>: exactly that (earlier run). **End of the guide.** To see what happens after a proposal, read the [recorded four-role case](VERIFIED_FOUR_ROLE_CASE.md) (a different change with its own baseline).

## How to verify, independent of the AI's wording
Scope and values match your words; each claim has a status; sources you did not touch stay visible; numbers come from the measured simulation and the interpretation is labelled; raw quotes are hidden for your role; nothing after the proposal is offered to you.

## Supporting references
Measured timings are single samples, not guarantees: worker start about 6 s after a request; 14-23 s for a simple job; the Scheduler backstop recovered a missed wake-up in 178 s in one sample.
