"""DataForSEO response adapters - importer, synthesis, and renderer.

Read-only, no network, no credentials. Normalizes a DataForSEO v3 API response
envelope (the JSON returned by any /v3/... endpoint) into flat records, summarizes
their cost, and renders a sourced markdown report. Used by the scripts/ CLIs and tests.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DataForSEOFormatError(ValueError):
    """Raised when input is not a valid DataForSEO v3 response envelope."""


def load_response(path: str | Path) -> dict[str, Any]:
    """Load and validate a DataForSEO v3 response envelope from a JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"response file not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DataForSEOFormatError(f"invalid JSON: {exc}") from exc
    return validate_envelope(data)


def validate_envelope(data: Any) -> dict[str, Any]:
    """Validate the minimal DataForSEO envelope shape and return it."""
    if not isinstance(data, dict):
        raise DataForSEOFormatError("envelope must be a JSON object")
    for key in ("status_code", "tasks"):
        if key not in data:
            raise DataForSEOFormatError(f"envelope missing required key: {key}")
    if not isinstance(data.get("tasks"), list):
        raise DataForSEOFormatError("envelope 'tasks' must be a list")
    return data


def normalize_records(resp: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten a response envelope into one record per task.

    Each record carries the endpoint path, the task and envelope status codes,
    the billed cost, the result_count, and the keyword/target the task ran on
    (when present). No private data is retained.
    """
    resp = validate_envelope(resp)
    env_cost = float(resp.get("cost") or 0.0)
    records: list[dict[str, Any]] = []
    for task in resp.get("tasks") or []:
        if not isinstance(task, dict):
            continue
        data = task.get("data") or {}
        target = None
        if isinstance(data, dict):
            target = data.get("keyword") or data.get("target") or data.get("url")
        records.append(
            {
                "endpoint": (data.get("function") if isinstance(data, dict) else None)
                or task.get("path") and "/".join(task.get("path"))
                or "unknown",
                "envelope_status_code": resp.get("status_code"),
                "task_status_code": task.get("status_code"),
                "cost": round(float(task.get("cost") or 0.0), 6),
                "result_count": task.get("result_count"),
                "target": target,
            }
        )
    if not records and env_cost:
        records.append({"endpoint": "unknown", "cost": round(env_cost, 6),
                        "task_status_code": resp.get("status_code"), "result_count": 0, "target": None})
    return records


def synthesize_cost_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize normalized records into a deterministic cost report."""
    total = round(sum(float(r.get("cost") or 0.0) for r in records), 6)
    ok = sum(1 for r in records if r.get("task_status_code") == 20000)
    by_endpoint: dict[str, float] = {}
    for r in records:
        ep = str(r.get("endpoint") or "unknown")
        by_endpoint[ep] = round(by_endpoint.get(ep, 0.0) + float(r.get("cost") or 0.0), 6)
    return {
        "schema": "dataforseo.cost-summary-v1",
        "calls": len(records),
        "ok_calls": ok,
        "total_cost_usd": total,
        "by_endpoint": dict(sorted(by_endpoint.items())),
    }


def render_report(summary: dict[str, Any], records: list[dict[str, Any]]) -> str:
    """Render a sourced markdown cost scorecard with wikilinks and a rollback note."""
    lines = [
        "---",
        "type: deliverable",
        'title: "DataForSEO Cost Scorecard"',
        "domain: dataforseo",
        "status: generated",
        "created: 2026-06-26",
        "tags: [dataforseo, deliverable, cost]",
        "---",
        "",
        "# DataForSEO Cost Scorecard",
        "",
        f"Calls: {summary['calls']} ({summary['ok_calls']} ok). "
        f"Total billed: ${summary['total_cost_usd']:.6f}.",
        "",
        "## Cost by endpoint",
        "| endpoint | cost (USD) |",
        "| --- | ---: |",
    ]
    for ep, cost in summary["by_endpoint"].items():
        lines.append(f"| {ep} | {cost:.6f} |")
    lines += [
        "",
        "## Context",
        "Billing model: [[cap-queue-priority-cost-model]]. Lower cost via "
        "[[dec-cost-control-strategy]] and [[dec-live-vs-standard-vs-priority]].",
        "",
        "## Rollback",
        "This report is generated and read-only. To revert, delete the output file; "
        "no source data is modified.",
        "",
        "## Sources",
        "- DataForSEO user_data (cost fields) - https://docs.dataforseo.com/v3/appendix/user_data/ - retrieved 2026-06-26",
        "",
    ]
    return "\n".join(lines)
