"""Job kind "explain", executor_id "explain.v1", role "intent.explain": plain-English wording of an already verified result (one model call).

The facts in the payload were collected by the SERVER from stored records the requesting account may read. The model only phrases
them. The server then checks the text: it is safe (no link, markup, id), short, and every number in it is a number from the facts.
Nothing here judges, extracts, decides, approves or applies. The result is stored with the snapshot it describes; the page reads it,
it never asks a model on render. Role `intent.explain` must be pinned in the budget config (no fallback), the endpoint must be the
Vertex global one and the served model must equal the pinned one.
"""
from __future__ import annotations

from infra.worker.provider_response import require_normal_finish

import hashlib
import json
import pathlib
import re

from infra import chat_safety
from infra.worker import extraction
from infra.worker.budget_config import model_for_role
from infra.worker.change_draft import _assert_global_endpoint, _canon_json, _clip
from infra.worker.execution_types import (
    ExecutionContext, ExecutionOutcome, ExecutionRequest, NonRetryableExecutionError, ProviderCallBudget,
    ProviderExecutionError, ProviderInvalidResponseError, ProviderRateLimitError, ProviderTimeoutError, is_timeout_exception,
)
from infra.worker.gap_answer import _model_object
from infra.worker.live_analysis import _client_for_model, _field, _token_count

EXECUTOR_ID = "explain.v1"
ROLE = "intent.explain"
CONFIG_PATH = pathlib.Path(__file__).resolve().parents[2] / "config" / "explain.json"
_NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
_ID = re.compile(r"\b(?:art|cand|job|rev|src|km|vc|intent|chat|dec|finding)-[0-9a-z_-]{6,}\b|\b[0-9a-f]{32,}\b")


def load_config() -> tuple[dict, str]:
    raw = CONFIG_PATH.read_bytes()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def numbers_in(value) -> set[float]:
    out: set[float] = set()
    for m in _NUM.findall(json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value):
        try:
            out.add(float(m.replace(",", "")))
        except ValueError:
            pass
    return out


def validate_payload(payload) -> str | None:
    if not isinstance(payload, dict) or not isinstance(payload.get("facts"), dict) or not payload["facts"]:
        return "facts_required"
    if not isinstance(payload.get("snapshot"), dict) or not isinstance(payload.get("subject"), str):
        return "snapshot_required"
    return None


def verify_text(text, facts: dict, max_chars: int) -> str:
    """The wording the server accepts. Raises NonRetryableExecutionError when it adds anything the facts do not carry."""
    def bad(why):
        raise NonRetryableExecutionError("explanation_rejected", why)
    if not isinstance(text, str) or not text.strip():
        bad("empty")
    t = re.sub(r"\s+", " ", text).strip()
    if len(t) > max_chars:
        bad("too_long")
    if chat_safety.unsafe_output(t) or _ID.search(t):
        bad("unsafe_or_id")
    allowed = numbers_in(facts) | set(map(float, range(0, 11)))
    extra = [n for n in numbers_in(t) if n not in allowed]
    if extra:
        bad("number_not_in_facts")
    return t


def call_pinned_json(ctx: ExecutionContext, request: ExecutionRequest, calls: ProviderCallBudget, role: str, key_set: set):
    """One pinned-role provider call returning a JSON object with exactly `key_set` keys. -> (obj, pinned_model, served_model, in, out, thought)."""
    config = ctx.config
    if role not in (getattr(config, "role_model_ids", None) or {}):
        raise NonRetryableExecutionError("role_model_not_pinned", f"role_model_ids has no {role!r} entry")
    model_id = model_for_role(config, role)
    if extraction._input_token_bound(request.prompt, request.schema) > config.max_input_tokens_per_call:
        raise NonRetryableExecutionError("budget_exceeded", "explanation request exceeds input ceiling")
    _assert_global_endpoint()
    call_config = {"max_output_tokens": ctx.max_output_tokens, "temperature": 0.0, "response_mime_type": "application/json"}
    timeout_s = getattr(config, "request_timeout_seconds", None)
    if timeout_s:
        call_config["http_options"] = {"timeout": int(timeout_s * 1000)}
    calls.consume()
    try:
        client = _client_for_model(model_id)
        response = client.models.generate_content(model=model_id, contents=request.prompt, config=call_config)
    except Exception as exc:
        code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if callable(code):
            code = code()
        if code == 429:
            raise ProviderRateLimitError("provider rate limited") from exc
        if is_timeout_exception(exc, code):
            raise ProviderTimeoutError("provider timed out") from exc
        raise ProviderExecutionError("provider request failed") from exc
    actual = _field(response, "model_version") or model_id
    if not isinstance(actual, str) or actual not in config.model_prices:
        raise NonRetryableExecutionError("unpriced_model")
    if actual != model_id:
        raise NonRetryableExecutionError("served_model_differs_from_pinned_role_model", f"{actual}")
    require_normal_finish(response, model_id=model_id, requested_cap=getattr(ctx, "max_output_tokens", None))
    usage = _field(response, "usage_metadata")
    in_t, out_t = _token_count(usage, "prompt_token_count"), _token_count(usage, "candidates_token_count")
    th_t, total = _token_count(usage, "thoughts_token_count"), _token_count(usage, "total_token_count")
    if total is not None and in_t is not None and out_t is not None:
        th_t = max(th_t or 0, total - in_t - out_t)
    try:
        text = _field(response, "text")
    except (ValueError, IndexError, AttributeError) as exc:
        raise ProviderInvalidResponseError("provider returned no text") from exc
    obj = _model_object(text)
    if set(obj) != key_set:
        raise NonRetryableExecutionError("schema_violation", "keys")
    return obj, model_id, actual, in_t, out_t, th_t


class ExplainExecutor:
    external = True
    executor_id = EXECUTOR_ID

    def prepare(self, ctx: ExecutionContext) -> ExecutionRequest:
        config = ctx.config
        if config is None or not ctx.max_output_tokens:
            raise NonRetryableExecutionError("budget_config_required")
        err = validate_payload(ctx.job["payload"])
        if err:
            raise NonRetryableExecutionError(err)
        frozen, sha = load_config()
        facts = ctx.job["payload"]["facts"]
        blob = _canon_json(facts)
        if len(blob) > frozen["limits"]["max_facts_chars"]:
            raise NonRetryableExecutionError("budget_exceeded", "facts exceed the limit")
        prompt = frozen["prompt_template"].replace("{facts}", blob)
        if extraction._input_token_bound(prompt, frozen["output_schema"]) > config.max_input_tokens_per_call:
            raise NonRetryableExecutionError("budget_exceeded", "explanation request exceeds input ceiling")
        ctx.request_context.update(ex_facts=facts, ex_limits=frozen["limits"], ex_sha=sha, ex_snapshot=ctx.job["payload"]["snapshot"],
                                   ex_subject=ctx.job["payload"]["subject"])
        return ExecutionRequest(prompt=prompt, schema=frozen["output_schema"], provider_calls_planned=1, external=True)

    def execute(self, ctx: ExecutionContext, request: ExecutionRequest, calls: ProviderCallBudget) -> ExecutionOutcome:
        obj, model_id, actual, in_t, out_t, th_t = call_pinned_json(ctx, request, calls, ROLE, {"text"})
        rc = ctx.request_context
        wording = verify_text(obj["text"], rc["ex_facts"], rc["ex_limits"]["max_text_chars"])
        result = {"text": _clip(wording, rc["ex_limits"]["max_text_chars"]), "subject": rc["ex_subject"], "snapshot": rc["ex_snapshot"],
                  "label": "AI-written wording of verified facts", "executor_id": EXECUTOR_ID, "draft_only": True, "applies_nothing": True,
                  "provider_calls": 1, "config_sha256": rc["ex_sha"],
                  "endpoint": {"backend": "vertex", "location": "global", "pinned_model": model_id, "served_model": actual}}
        result = json.loads(_canon_json(result))
        return ExecutionOutcome(result=result, model_id=actual, input_tokens=in_t, output_tokens=out_t, thought_tokens=th_t)
