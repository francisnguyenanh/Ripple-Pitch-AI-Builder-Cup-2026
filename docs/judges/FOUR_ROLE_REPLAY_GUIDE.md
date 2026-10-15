# Four-role replay (optional) - available on request

> **Starting point.** This walkthrough uses a specific starting baseline. If earlier changes have been applied in this workspace, the sample values and expected results may no longer match. Check the current source revision and values before starting. For subsequent runs, follow the same workflow using the latest data.

**Status: assisted, on request.** A hands-on four-role run (request, review, approval, apply) is **not self-service**. This guide does not give you accounts for it and nothing on this page lets you start it. If you want one, ask the team; it is arranged separately, and the one-role demo is not used for it.

Your main path stays the [one-role demo](one-role-guide.html) (recommended). To see what four people did, read the [recorded case](four-role-case.html) (read-only evidence of a past run, with its own rule and baseline).

## What an assisted replay involves
Four different people take one change from request to an applied change:

| Person | What they do |
|---|---|
| Requester | states the change, confirms it, asks for the draft and the analysis, builds the proposal, runs the review, prepares the approval bundle and applies the approved change |
| Knowledge owner | decides open points and accepts the updated knowledge |
| Reviewer | reads the proposal and its evidence and may add a note |
| Approver | states the check that must hold after the change, approves, and accepts the result |

Nobody can approve their own request; the server checks that. Applying changes the source of the workspace used, so the values you start from are whatever that workspace holds at the time.

## Guided example and continued exploration
- **Guided example:** one specific starting value and request, as in the [one-role guide](one-role-guide.html), used while the workspace is still at that value.
- **Continued exploration:** after a change has been applied, follow the same workflow with the current value and a new request; the numbers will differ from any example. Nothing is reset between runs, and earlier requests, decisions and history stay visible.

## Starting a further run
1. Read the current value first (**Explorer**, then the rule; its **Value** and **Taken from** tell you what it is now). The Technical view shows the current source revision.
2. Open **Changes** from another page, so the conversation is new. Your own earlier requests are listed in **My work**; do not open someone else's.
3. Write the request with the **current** value and the new value you want. Check the AI's preview ("This is what I understood") before confirming.
4. Read the simulation of this run as it is; do not expect numbers from an earlier run.
5. A draft or proposal made before the source changed is marked out of date. Ask for a new draft instead of using it.
6. The **Next** card at the top of the Changes page and the row **Where this change is** name the person who has to act next.

## Follow the recorded case in the meantime (read-only)
With a judge account you can read and follow the evidence of [the recorded case](VERIFIED_FOUR_ROLE_CASE.md); you do not repeat its approve and apply steps.

| To follow | Where | What to check |
|---|---|---|
| The request and the draft | Changes, with the ids from the case (draft, intent) | One supported edit; open points listed; carried items marked with their origin |
| The decision on the open point | Draft stage, *Clarifications used* | The person's own words kept exactly; files named with role; "Recorded by the server" |
| The measures | stage 3 *Impact and simulation* | 240 cases, baseline reproduced 240/240; the AI reading is labelled as interpretation |
| The proposal | stage 4 *Proposal* | exact diff; *Left for people* |
| Approval and apply history | History, Changes (Technical view) | who approved which fingerprint; verification PASSED |
| The post-change answer | stage 11 *Ask again on the new revision* (stored) | ABSTAINED with the conflicting sources |

Opening a stored result never starts an AI job. If the page shows "not started" you opened it without the full link: use **My work** or the Changes chooser instead of typing ids.
