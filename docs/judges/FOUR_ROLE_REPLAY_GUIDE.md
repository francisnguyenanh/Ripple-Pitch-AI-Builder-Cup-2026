# Four-role workflow (optional): do it yourself with four accounts

> **Starting point.** This walkthrough uses a specific starting baseline. If earlier changes have been applied in this workspace, the sample values and expected results may no longer match. Check the current source revision and values before starting. For subsequent runs, follow the same workflow using the latest data.

You switch between **four accounts that you receive separately** (never written in this guide): a **Requester**, an **Approver**, a **Reviewer** and an **Admin** account. They all work in the **same workspace as the one-role demo**, on the same system. Applying a change here **edits the stored source file**, so the starting value, the history and the results change for everyone who comes after you. That is accepted and expected: read the current value first (Part II).

Your recommended path is still the [one-role demo](one-role-guide.html). The [recorded case](four-role-case.html) is the read-only evidence of an earlier run of this same workflow (a different rule and baseline).

## Shared AI limits - read this first
All AI steps use **one shared budget**. An extra allowance for this path was added on **2026-10-16**, aimed at about **one to two** four-role runs. **The number of runs that complete is not guaranteed.** Clarifications, a revised draft, extra questions and a wide re-read use it up faster. When a limit is reached Ripple shows the reason and charges nothing. Do not switch accounts or try to reset anything to get around it; if you cannot continue, read the stored results or the [recorded case](four-role-case.html) (reference material, not a completed run of yours). Details are in Part IV.

## Part I - Guided example (the same change as in the one-role guide)
**Snapshot used for this example:** read on 2026-10-16 (server, by the project team): source revision `rev-apply-ui-apply-dfcd1335eef248c0`, decision epoch 3, 13 files, rule `routing_rules.standard_manager_threshold_jpy` = **500,000**. If you read a different value, skip to Part II: the steps stay the same.

Each line names the **account**, what it does and who is next. "Wait" means: the page updates by itself; continue only when the stated sign appears.

| # | Account | Where and what | Sign that it is done | Next |
|---|---|---|---|---|
| 1 | Requester | **Explorer**, search `approval.yaml`, open the rule whose title reads like "Routing rules standard manager threshold jpy". **Value** must be the value you plan to change (no currency is shown there). | you have read the current value | Requester |
| 2 | Requester | Left menu **Overview**, then **Changes** (always from another page, so the conversation is new). In stage 1, paste the request text from the section "The request to type" of the [one-role guide](one-role-guide.html) (if your value differs, write the same sentence with your current and new values). Click **Send** (Enter also sends). | card "This is what I understood" with current and new values you intended | Requester |
| 3 | Requester | If a check box appears (assumptions / left out), tick it. Click **Yes, this is what I mean**, then **Confirm intent**. | stage 1 status **Confirmed** | Requester |
| 4 | Requester | Stage 2: **Generate GenAI draft**. Wait. Read "Draft status" (Partly processed is normal), the **Proposed edit** for `approval.yaml` and the open points. | job Done, one Proposed edit | Requester |
| 5 | Requester | Stage 3: **Run impact analysis**, then **Run simulation**. Read the numbers of **this** run. Optional: **Ask the AI to read this simulation (uses the paid model)**. | simulation Done | Requester |
| 6 | Requester | Stage 4: check the `approval.yaml` edit is ticked (it is by default), click **Prepare the proposal with the ticked edits**. | diff shown; Next card: "Waiting for: An approver (not the requester)" | **Approver** |
| 7 | Approver | Sign in with the Approver account. **Overview**, in **My work** open the item (or use the Requester's **Copy request link** from the "Your request" card). Stage 5 "Check after the change": read the suggested check, click **Confirm these checks**. | stage 5 shows the check confirmed | **Requester** |
| 8 | Requester | Stage 6: **Run review**. Wait. | review Done | Requester (Reviewer may add a note) |
| 9 | Reviewer (optional) | Open the same change. In the review area, write a note and click **Mark ready for approval**, or **Ask for changes** (this blocks the approval until the Reviewer marks it ready again). | no open "asked for changes" | Requester |
| 10 | Requester | Stage 7: **Prepare approval bundle**. Wait. | bundle Done | **Approver** |
| 11 | Approver | Stage 7: read the decision basis, type a **Decision reason**, click **Approve** (or **Reject**). Approving applies nothing. | decision Approved | **Requester** |
| 12 | Requester | Stage 8: **Apply approved change**. Wait. This is the first step that edits the source file. | apply Done; the source revision changed | System, then Admin and Approver |
| 13 | (system) | Stage 9 re-reads the changed file and updates the knowledge. See **Current limits** above: it may not complete. | "Where this change stands" | Admin |
| 14 | Admin | Stage 9: **Accept knowledge candidate** when it is offered. | knowledge accepted | **Approver** |
| 15 | Approver | Stage 10: choose for every group shown, give reasons where asked, click **Accept result** (or **Request changes** / **Reject result**). The result is complete only when a person decides. | result decision recorded | Requester |
| 16 | Requester | Stage 11: type a question, click **Ask on the new revision** (limited, see above). | answered, or refused with the allocation message | - |

Optional extra step 4b (Admin): in stage 2, the **Open points to answer**: type the answer and a reason, click **Confirm this answer as a decision**. This marks the draft out of date; the Requester then clicks **Revise this draft with confirmed feedback (uses the paid model)** and repeats steps 5 and 6. A decision belongs to the request it was made for; a new request does not inherit it.

You do not type keys, YAML or ids anywhere: the pages prefill them. Nobody can approve a request they made themselves; the server checks accounts, not roles.

## Part II - Continued exploration (any later run, any starting value)
1. **Check the baseline first**, even on your first visit: someone may already have applied a change. Explorer, search `approval.yaml`, open the rule, read **Value**. In the Technical view (top right) the header shows the current **Source revision**.
2. Start a **new request** from **Changes** reached from another page. Do not open a request that is not yours: **My work** lists the items waiting for the account you are signed in with.
3. Write the request with the **current** value and a new value you choose. Read the AI's preview before you confirm; the AI may ask a question or word things differently, and you must not confirm a preview that has a wrong number.
4. Read the simulation of **this** run as it is. How many cases change depends on the current value; do not expect the numbers of any example.
5. Follow the same accounts and steps as in Part I.
6. **Out of date:** if the source changed after your draft or proposal (someone applied), the page says so and an old approval cannot be used. Ask for a new draft ("Generate GenAI draft" again, or "Revise this draft…") instead.
7. **Partly processed (PARTIAL):** not a failure. It means some sources stay with people; they remain listed as unresolved or potentially affected and are **not** treated as resolved.
8. **Verification and acceptance:** an apply is not "done" until stage 9 has re-read the changed file and a person has accepted the knowledge and the result.
9. **Several people at once:** each request has its own chain. If one change is applied, the others become out of date and need a new draft. If the page says jobs are waiting up to the workspace limit, wait and press the button again.
10. **Do not restore** an earlier version to match an example. Restore is a separate administration step with its own approval and is not part of this workflow.

## Part III - Administrator checks (optional; not part of the business workflow)
The Admin account can also try the administration functions. They are **shared**: the same system, workspace and service serve every judge and every other account.
- **AI and processing switches** (Support & Access, card "AI and processing switches"). Two switches: **New AI starts** and **Job processing**. They are **service-wide**, not per workspace or per account.
  - *Switch OFF* "New AI starts": every new AI action of every user is refused with "AI actions are switched off on this server (by the operator)". Nothing is started or charged; saved results stay readable.
  - *Switch OFF* "Job processing": queued jobs wait and are not lost; jobs already running finish.
  - The header banner shows "New AI starts: ON/OFF - Job processing: ON/OFF" for every signed-in user, and the switch history lists who changed it and why.
  - **To turn it back on:** Support & Access, same card, type a reason of at least 10 characters, click **Switch ON** for each switch that is OFF. The banner returns to ON (it refreshes about every 30 seconds) and waiting jobs are picked up within seconds; a job left waiting is recovered by the periodic wake-up within a few minutes.
  - Switching off blocks every other judge until you switch it on again. At the end of the evaluation window the system closes the switches itself.
- **Members** (Support & Access): reading the member list, and per-member AI use. A change affects that account for everyone using it.
- Allocation and budget are **not** something a screen can raise; do not treat a refusal as a step to work around.

## Part IV - The limits in detail
- **Per account:** at most 12 AI jobs per day; a chat conversation at most 6 AI replies.
- **Per step (allowances, shared):** the re-read of the changed file after an apply (`extraction`) and the "Ask on the new revision" answer (`gap.answer`) each have a small allowance; the draft, the simulation reading and the chat have larger ones. The project budget caps everything together.
- **Re-read after an apply:** normally one file (the changed one). It can cover all 13 files when the earlier readings lack their relation coverage, and it did so once in this workspace. A wide re-read is **not** covered by the extra allowance: the first files are read and the rest are refused.
- **If the allowance runs out after you applied:** the source file **is** already changed (an apply is not undone). Say what the page shows, no more and no less: if the machine check of the changed file passed but the re-read did not finish, the state is **"Applied and machine-verified; knowledge refresh incomplete"**; the knowledge is then not fully updated and the result still needs a person's decision. Do not call it rolled back, fully verified or fully updated.
- **While something is pending:** a job shows "Waiting to run" or "Running" and the page updates by itself; a refused action shows the reason (for example "The approved allocation for this kind of AI action is used up"). Saved results stay readable.
- **Also shared:** the number of jobs allowed to run at once in the workspace, the administrator switches (Part III) and the evaluation window (open until **2026-11-06 23:59:59 SGT** = 15:59:59 UTC).

## Follow the recorded case (read-only)
With any account you can read and follow the evidence of [the recorded case](VERIFIED_FOUR_ROLE_CASE.md); you do not repeat its approve and apply steps.

| To follow | Where | What to check |
|---|---|---|
| The request and the draft | Changes, with the ids from the case (draft, intent) | One supported edit; open points listed; carried items marked with their origin |
| The decision on the open point | Draft stage, *Clarifications used* | The person's own words kept exactly; files named with role; "Recorded by the server" |
| The measures | stage 3 *Impact and simulation* | 240 cases, baseline reproduced 240/240; the AI reading is labelled as interpretation |
| The proposal | stage 4 *Proposal* | exact diff; *Left for people* |
| Approval and apply history | History, Changes (Technical view) | who approved which fingerprint; verification PASSED |
| The post-change answer | stage 11 *Ask again on the new revision* (stored) | ABSTAINED with the conflicting sources |

Opening a stored result never starts an AI job. If the page shows "not started" you opened it without the full link: use **My work** or the Changes chooser instead of typing ids.

## What this guide does and does not claim
Steps and labels come from the pages of the deployed version. **Not verified by a live run of all four accounts**: the exact on-screen wording at each step, and whether stages 9 and 11 complete under the current allocation. Offline tests with stub providers show the wiring and the permission rules only; they are not evidence of live results. The recorded case remains a past run whose **final acceptance is still pending**.
