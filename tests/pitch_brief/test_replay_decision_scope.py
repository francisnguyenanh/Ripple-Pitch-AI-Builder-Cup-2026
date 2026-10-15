"""Regression evidence for the PLANNED four-role workflow (not a live run): with no administrator, only a knowledge owner decides an open point (requester, reviewer, approver: HTTP 403);
the decision is scoped to the request (intent) it was made for, so a NEW request does not inherit it and a draft pinned before it does not use it."""
from __future__ import annotations

import pytest

from tests.pitch_brief.chain import build
from tests.pitch_brief.test_gap_decisions import ANSWER, _first_draft, _gaps
from tests.pitch_brief.test_source_data_boundary import _client


@pytest.fixture
def ch(env, monkeypatch):
    return build(env, monkeypatch)


def test_only_a_knowledge_owner_decides_an_open_point_and_the_decision_belongs_to_that_request_only(env, ch, monkeypatch):
    _model, d1, intent_id = _first_draft(env, ch, monkeypatch)
    q = next(x for x in _gaps(ch.admin, env, d1)["gaps"] if x["kind"] == "question")
    body = {"workspace_id": env.ws, "draft_job_id": d1, "gap_key": q["key"], "answer": ANSWER, "rationale": "agreed"}
    for role in ("requester", "reviewer", "change_approver"):
        r = _client(env, role).post("/v2/change/gap/confirm", json=body)
        assert r.status_code == 403, (role, r.status_code)                                   # not their decision to take
    ok = _client(env, "knowledge_owner").post("/v2/change/gap/confirm", json=body)
    assert ok.status_code == 200, ok.text
    mine = env.store.active_gap_clarifications(env.tenant, env.ws, intent_id, None)
    assert len(mine) == 1 and mine[0]["actor_id"] != env.admin and mine[0]["scope"]["kind"] == "draft_gap_answer" and mine[0]["scope"]["intent_id"] == intent_id
    other = env.store.active_gap_clarifications(env.tenant, env.ws, "intent-a-new-request", None)
    assert other == []                                                                       # a NEW request does not inherit it
    before = env.store.active_gap_clarifications(env.tenant, env.ws, intent_id, 0)
    assert before == []                                                                      # nor does a draft pinned before the decision
