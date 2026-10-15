"""One on-demand worker serving TWO workspaces of one tenant through the allow-lists that already exist (`RIPPLE_WAKE_WORKSPACES` on the web side, the `workspaces` list of the bounded worker):
the wake-up sees work of either workspace and of no other, the worker claims only the workspaces it is given, work is never lost when a job arrives for the second workspace, and a member of one workspace
cannot read the other. Real disposable database, fake Cloud Run `post`; no provider is called, nothing is deployed."""
from __future__ import annotations

import json

import pytest

from infra.worker import job_worker, wake
from tests.pitch_brief.test_worker_wake import Post, queue, w  # noqa: F401  (fixture `w` and helpers)


def _second_workspace(env):
    r = env.admin_client().post("/v2/workspaces", json={"project_id": env.tenant.replace("t-", "p-"), "name": "replay regression workspace", "idempotency_key": "two-ws-1"})
    assert r.status_code == 200, r.text
    return r.json()["workspace_id"]


def _queue_other(env, ws2, job_id):
    with env.store._tx() as cur:
        cur.execute("INSERT INTO v2_outbox (tenant_id, workspace_id, kind, payload) VALUES (%s,%s,'JOB_QUEUED',%s)", (env.tenant, ws2, json.dumps({"job_id": job_id, "kind": "change.draft"})))


def test_the_wake_up_sees_work_of_both_allowed_workspaces_and_of_no_other(w, monkeypatch):
    ws2 = _second_workspace(w)
    _queue_other(w, ws2, "job-ws2")
    post = Post()
    monkeypatch.setenv("RIPPLE_WAKE_WORKSPACES", f"{w.tenant}:{w.ws}")                      # today's setting: the second workspace's work wakes nobody
    assert wake.kick(w.store, post=post)["reason"] == "no_work" and not post.calls
    monkeypatch.setenv("RIPPLE_WAKE_WORKSPACES", f"{w.tenant}:{w.ws},{w.tenant}:{ws2}")      # both pairs: the same one signal starts the one worker
    assert wake.kick(w.store, post=post)["reason"] == "signal_sent" and len(post.calls) == 1


def test_a_worker_claims_only_the_workspaces_it_is_given(w):
    ws2 = _second_workspace(w)
    queue(w, "job-ws1")
    _queue_other(w, ws2, "job-ws2")
    seen = []

    def claim(store, tenant, workspace, wid):
        c = store.claim_outbox(tenant, workspace, wid)
        if c is not None:
            seen.append((workspace, c.payload.get("job_id")))
        return None if c is None else type("C", (), {"kind": "SKIP"})()
    t = [0.0]
    job_worker.run_bounded_worker(w.store, [(w.tenant, w.ws)], worker_id="only-ws1", poll_seconds=1, idle_exit_seconds=2, claim_fn=claim,
                                  clock=lambda: t.__setitem__(0, t[0] + 1) or t[0], sleep=lambda s: None, heartbeat=False)
    assert seen == [(w.ws, "job-ws1")]                                                    # a worker pinned to one workspace never touches the other (the replay worker cannot claim pitch-ws1 and vice versa)
    seen.clear()
    t[0] = 0.0
    job_worker.run_bounded_worker(w.store, [(w.tenant, w.ws), (w.tenant, ws2)], worker_id="both", poll_seconds=1, idle_exit_seconds=2, claim_fn=claim,
                                  clock=lambda: t.__setitem__(0, t[0] + 1) or t[0], sleep=lambda s: None, heartbeat=False)
    assert seen == [(ws2, "job-ws2")]                                                     # the second workspace's job is claimed; the first one's was already claimed and is not claimed twice


def test_a_job_queued_for_the_second_workspace_after_the_worker_left_starts_a_new_execution(w, monkeypatch):
    ws2 = _second_workspace(w)
    monkeypatch.setenv("RIPPLE_WAKE_WORKSPACES", f"{w.tenant}:{w.ws},{w.tenant}:{ws2}")
    post = Post()
    assert wake.kick(w.store, post=post)["reason"] == "no_work"
    _queue_other(w, ws2, "job-late")
    with w.store._tx() as cur:
        cur.execute("UPDATE v2_worker_wake SET last_kick_at = NULL")
    assert wake.kick(w.store, post=post)["reason"] == "signal_sent" and len(post.calls) == 1


def test_a_member_of_one_workspace_cannot_read_the_other(w):
    ws2 = _second_workspace(w)
    r = w.req_client().get(f"/v2/workspaces/{ws2}/head")
    assert r.status_code in (403, 404), r.status_code
    r2 = w.req_client().get(f"/v2/workspace/profile", params={"workspace_id": ws2})
    assert r2.status_code in (403, 404), r2.status_code
