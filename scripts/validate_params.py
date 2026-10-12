#!/usr/bin/env python3
"""Check request-parameter claims in vault notes against the official OpenAPI spec.

For every note with a "Key parameters" section, each field named there must be
a request property of an endpoint the note references (or, failing that, of
some endpoint in the same API module). Stated caps ("max 1000", "up to 700")
next to a field are compared with the maximums the spec's field description
gives for those endpoints.

Ground truth: .raw/sources/dataforseo-openapi/openapi_specification.yaml.
Exit 0 = clean, 1 = findings.
"""
from __future__ import annotations
import os

import argparse
import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_endpoints import ENDPOINT_RE, SPEC_REL, normalise, resolve  # noqa: E402

DEFAULT_VAULT = Path(os.environ.get("DFS_BRAIN_VAULT") or Path.home() / "Documents" / "DataForSEO Brain" / "vault")
SECTION_RE = re.compile(r"^## Key parameters.*?$(.*?)(?=^## )", re.M | re.S)
FIELD_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z0-9_]+)*$")
# response/envelope words that notes list alongside inputs; not request fields
NOT_FIELDS = {"id", "tasks", "data", "result", "items", "cost", "status_code", "status_message", "tasks_error", "tasks_count", "tag", "postback_url",
              "pingback_url", "postback_data", "true", "false", "null", "post", "get", "live", "task_post", "task_get",
              "advanced", "html", "regular", "array", "string", "integer", "object", "boolean"}
CAP_RE = re.compile(r"(?:max(?:imum)?|up to|cap(?:s|ped)? at|at most|limit(?:ed)? (?:of|to))\D{0,12}([\d][\d,]*)", re.I)
SPEC_MAX_RE = re.compile(r"(?:maximum|max)[^:<]{0,80}:\s*([\d][\d,]*)", re.I)


def load_request_fields(spec_path: Path) -> dict[str, dict[str, str]]:
    """normalised path -> {field: plain-text description} for every POST endpoint."""
    import yaml  # optional dependency: only needed when the vault ships the OpenAPI spec

    spec = yaml.load(spec_path.read_text(encoding="utf-8"), Loader=getattr(yaml, "CBaseLoader", yaml.BaseLoader))  # all scalars as strings: the spec has invalid dates and bare "="
    schemas = spec["components"]["schemas"]
    out: dict[str, dict[str, str]] = {}
    for path, ops in spec["paths"].items():
        body = ((ops.get("post") or {}).get("requestBody") or {}).get("content", {}).get("application/json", {})
        items = (body.get("schema") or {}).get("items") or {}
        refs = [o.get("$ref", "") for o in items.get("oneOf", [])] + [items.get("$ref", "")]
        props: dict[str, str] = {}
        for ref in filter(None, refs):
            collect(schemas.get(ref.rsplit("/", 1)[-1], {}), schemas, props, 0)
        if props:
            out[normalise(path)] = props
    return out


def collect(schema: dict, schemas: dict, props: dict[str, str], depth: int) -> None:
    """Top-level fields keep their description; nested object/array-item fields (target[].search_scope) are added too."""
    if depth > 8 or not isinstance(schema, dict):
        return
    if "$ref" in schema:
        collect(schemas.get(schema["$ref"].rsplit("/", 1)[-1], {}), schemas, props, depth + 1)
    for sub in schema.get("oneOf", []) + schema.get("anyOf", []) + schema.get("allOf", []):
        collect(sub, schemas, props, depth + 1)
    for ref in ((schema.get("discriminator") or {}).get("mapping") or {}).values():
        collect({"$ref": ref}, schemas, props, depth + 1)
    if isinstance(schema.get("items"), dict):
        collect(schema["items"], schemas, props, depth + 1)
    for name, p in (schema.get("properties") or {}).items():
        if not isinstance(p, dict):
            continue
        props.setdefault(name, re.sub(r"<[^>]+>", " ", str(p.get("description", ""))) if depth == 0 else "")
        collect(p, schemas, props, depth + 1)


def spec_caps(desc: str) -> set[int]:
    return {int(n.replace(",", "")) for n in SPEC_MAX_RE.findall(desc)}


def note_fields(section: str) -> set[str]:
    fields = set()
    for line in section.splitlines():
        cell = line.split("|")[1] if line.startswith("|") and line.count("|") >= 3 else ""
        cell = cell if not set(cell.strip()) <= set("-: ") else ""
        candidates = re.split(r"[\s/,]+|\bor\b", cell.replace("`", " ")) + re.findall(r"^\s*[-*] `([a-z][a-z0-9_.]*)`", line)
        fields |= {c.strip() for c in candidates if FIELD_RE.match(c.strip() or "-") and "_" in c or c.strip() in {"limit", "offset", "filters", "target", "targets", "keywords", "keyword", "depth", "url", "device", "os"}}
    return {f for f in fields if f not in NOT_FIELDS}


def audit(vault: Path, stats: dict[str, int] | None = None) -> list[str]:
    stats = {} if stats is None else stats
    req = load_request_fields(vault / SPEC_REL)
    spec_n = set(req)
    findings = []
    for md in sorted((vault / "wiki").rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        m = SECTION_RE.search(text)
        if not m:
            continue
        clean = re.sub(r"https?://\S+", "", text)
        eps = set()
        for ep in ENDPOINT_RE.findall(clean):
            hits, _ = resolve(normalise(ep), spec_n)
            eps |= {h for h in hits if h in req}
        if not eps:
            continue
        modules = {e.split("/")[2] for e in eps}
        near = {f: d for e in eps for f, d in req[e].items()}
        wide = {f for e, props in req.items() if e.split("/")[2] in modules for f in props}
        rel = md.relative_to(vault).as_posix()
        fields = note_fields(m.group(1))
        stats["notes"] = stats.get("notes", 0) + 1
        stats["fields"] = stats.get("fields", 0) + len(fields)
        for field in sorted(fields):
            root = field.split(".")[0]
            if root not in near and root not in wide:
                findings.append(f"{rel}: field `{field}` is not a request field of any {'/'.join(sorted(modules))} endpoint")
        for line in m.group(1).splitlines():
            named = note_fields(line)
            for field in named if len(named) == 1 else ():
                if field not in near:
                    continue
                stated = {int(n.replace(",", "")) for n in CAP_RE.findall(line)}
                allowed = set().union(*(spec_caps(req[e][field]) for e in eps if field in req[e]))
                wrong = {s for s in stated if allowed and s not in allowed}
                if wrong:
                    findings.append(f"{rel}: `{field}` cap {sorted(wrong)} vs spec {sorted(allowed)}")
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    args = ap.parse_args(argv)
    stats: dict[str, int] = {}
    findings = audit(args.vault.expanduser().resolve(), stats)
    for f in findings:
        print(f"PARAM {f}")
    print(f"checked {stats.get('fields', 0)} fields in {stats.get('notes', 0)} notes; parameter findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
