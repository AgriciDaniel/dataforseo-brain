#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_prices  # noqa: E402
import validate_params  # noqa: E402
import validate_endpoints  # noqa: E402

# Files other tools write into the session folder that are not notes; the PreCompact
# continuity hook drops CONTINUITY.md wherever a session runs, the vault included.
NOT_NOTES = {"continuity.md"}
# Shell escaping turned "\reports\2026" into a CR plus 0x82 and "\b" into a backspace (2026-10-02); none
# of these bytes belongs in a note. Checked on the raw bytes (text mode hides a lone \r); once proper
# \r\n pairs are folded, any \r left (a lone CR, or \r\r\n from a doubled conversion) is damage.
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]|\r")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint a brain vault.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--template", action="store_true")
    args = parser.parse_args(argv)
    vault = Path(args.vault).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    for rel in ["CODEX.md", "README.md", "shipping-rules.md", ".raw/.manifest.json", "wiki/hot.md", "wiki/index.md", "wiki/overview.md", "wiki/log.md", "wiki/meta/Start Here.md", "wiki/meta/dashboard.md"]:
        if not (vault / rel).exists():
            errors.append(f"missing {rel}")
    check_raw_manifest(vault, errors)
    for canvas in sorted((vault / "wiki").rglob("*.canvas")) if (vault / "wiki").exists() else []:
        errors.extend(canvas_issues(vault, canvas))
    graph = vault / ".obsidian" / "graph.json"
    if graph.exists():
        data = json.loads(graph.read_text(encoding="utf-8"))
        if len(data.get("colorGroups") or []) < 4:
            errors.append("graph.json has fewer than 4 color groups")
    notes = [p for p in (vault / "wiki").rglob("*.md") if p.name.lower() not in NOT_NOTES] if (vault / "wiki").exists() else []
    stems = {p.stem.lower(): p for p in notes}
    rels = {p.relative_to(vault).with_suffix("").as_posix().lower(): p for p in notes}
    incoming = {p: 0 for p in notes}
    outgoing = {p: 0 for p in notes}
    duplicate_stems: dict[str, list[str]] = {}
    for path in notes:
        duplicate_stems.setdefault(path.stem.lower(), []).append(path.relative_to(vault).as_posix())
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"missing frontmatter: {path.relative_to(vault)}")
        raw = path.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n")
        damage = CONTROL_RE.search(raw)
        if damage:
            line = raw.count("\n", 0, damage.start()) + 1
            errors.append(f"control character {damage.group()!r} (escape damage?) in {path.relative_to(vault)}:{line}")
        if re.search(r"\{\{(?!date|owner|client_slug|client_name)[^}]+\}\}|__[A-Z0-9_]+__|\bTODO\b", text):
            errors.append(f"unresolved placeholder in {path.relative_to(vault)}")
        if any(part in {"deliverables", "reports"} for part in path.parts) and "[[" not in text and ".raw/" not in text and "sha256" not in text.lower():
            errors.append(f"deliverable/report lacks source citation: {path.relative_to(vault)}")
        for raw in re.findall(r"!?\[\[([^\]]+)\]\]", text):
            raw_target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            target = raw_target.replace(".md", "").replace(".canvas", "").strip()
            if not target:
                continue
            outgoing[path] += 1
            key = target.lower()
            if key in stems:
                incoming[stems[key]] += 1
            elif key in rels:
                incoming[rels[key]] += 1
            elif any(r.endswith("/" + key) for r in rels):
                # Obsidian resolves a partial path ([[platforms/_index]]) by suffix match.
                incoming[next(rels[r] for r in rels if r.endswith("/" + key))] += 1
            elif not (vault / raw_target).exists() and not any(vault.rglob(raw_target)):
                errors.append(f"dead wikilink in {path.relative_to(vault)}: {raw}")
    zero_in = [p.relative_to(vault).as_posix() for p in notes if incoming[p] == 0]
    zero_out = [p.relative_to(vault).as_posix() for p in notes if outgoing[p] == 0]
    if zero_in:
        warnings.append("zero incoming wiki notes: " + ", ".join(zero_in[:20]))
    if zero_out:
        warnings.append("zero outgoing wiki notes: " + ", ".join(zero_out[:20]))
    for stem, paths in duplicate_stems.items():
        if stem != "_index" and len(paths) > 1:
            errors.append(f"duplicate note stem {stem}: {', '.join(paths)}")
    errors.extend(f"price drift: {f}" for f in check_prices.check(vault))
    errors.extend(f"retired API described as live: {f}" for f in validate_endpoints.retired_refs(vault))
    errors.extend(f"costly routing: {f}" for f in validate_endpoints.routing_issues(vault))
    errors.extend(f"unknown item type: {f}" for f in validate_endpoints.item_type_issues(vault))
    errors.extend(f"price model: {f}" for f in validate_endpoints.flat_price_claims(vault))
    errors.extend(f"price model: {f}" for f in validate_endpoints.per_row_price_gaps(vault))
    errors.extend(f"live endpoint called retired: {f}" for f in validate_endpoints.false_retirements(vault))
    stale = None if args.template else stale_hook_copy()   # an operator's install, not the template's concern
    if stale:
        errors.append(stale)
    if not args.template:   # instruction files agents read before calling DataForSEO, outside the vault
        docs = operator_docs()
        errors.extend(f"agent instructions: {f}" for f in validate_endpoints.flat_price_claims(vault, files=docs))
        errors.extend(f"agent instructions: {f}" for f in validate_endpoints.per_row_price_gaps(vault, files=docs))
    if (vault / validate_params.SPEC_REL).exists():
        errors.extend(f"parameter claim: {f}" for f in validate_params.audit(vault))
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print("Vault lint passed" if not errors else "Vault lint failed")
    return 1 if errors else 0


INSTALLED_GUARD = Path.home() / ".claude" / "hooks" / "dfs_guard.py"


def operator_docs(home: Path | None = None) -> list[Path]:
    """Rules, agent briefs and SEO skills that tell agents how to call DataForSEO. A flat-price claim survived
    in the spend rule and the guard's own message after the vault was clean (2026-10-04/05)."""
    home = home or Path(os.environ.get("DFS_OPERATOR_HOME") or Path.home())   # tests point this at a temp dir
    c = home / ".claude"
    found = list((c / "rules").glob("dataforseo*.md")) + list((c / "agents").glob("seo-dataforseo*.md"))
    found += [p for p in (c / "skills").glob("seo*/**/*.md") if "dataforseo" in p.read_text(encoding="utf-8", errors="replace").lower()]
    return sorted(p for p in found if p.suffix == ".md")


def stale_hook_copy(installed: Path = INSTALLED_GUARD) -> str | None:
    """The guard hook runs from a copy in ~/.claude/hooks; a repo update that isn't copied leaves the old rules live."""
    repo = Path(__file__).resolve().parent / "dfs_guard.py"
    if installed.exists() and repo.exists() and installed.read_bytes() != repo.read_bytes():
        return f"installed guard hook {installed} differs from {repo}: copy the repo version over it"
    return None


def canvas_issues(vault: Path, canvas: Path) -> list[str]:
    """Canvas cards point at notes by path, which the wikilink check never sees; a renamed or deleted note breaks them silently."""
    rel = canvas.relative_to(vault)
    try:
        data = json.loads(canvas.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"invalid canvas {rel}: {exc}"]
    nodes = data.get("nodes") or []
    ids = {n.get("id") for n in nodes}
    out = [f"canvas card in {rel} points at a missing note: {n.get('file')}"
           for n in nodes if n.get("type") == "file" and not (vault / str(n.get("file") or "")).is_file()]
    out += [f"canvas edge {e.get('id')} in {rel} joins a missing card"
            for e in data.get("edges") or [] if e.get("fromNode") not in ids or e.get("toNode") not in ids]
    return out


def check_raw_manifest(vault: Path, errors: list[str]) -> None:
    manifest_path = vault / ".raw" / ".manifest.json"
    if not manifest_path.exists():
        return
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        errors.append(f"invalid raw manifest: {exc}")
        return
    sources = data.get("sources", [])
    if not isinstance(sources, list):
        errors.append("raw manifest sources must be a list")
        return
    seen_paths: set[str] = set()
    for index, entry in enumerate(sources, start=1):
        label = f"raw manifest source #{index}"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        rel = entry.get("path")
        expected = entry.get("sha256")
        if not isinstance(rel, str) or not rel.strip():
            errors.append(f"{label} missing path")
            continue
        rel = rel.strip()
        if rel in seen_paths:
            errors.append(f"duplicate raw manifest path: {rel}")
        seen_paths.add(rel)
        if rel.startswith("/") or ".." in Path(rel).parts:
            errors.append(f"{label} has unsafe path: {rel}")
            continue
        source = vault / rel
        if not source.is_file():
            errors.append(f"{label} missing file: {rel}")
            continue
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            errors.append(f"{label} missing valid sha256")
            continue
        if sha256_file(source) != expected:
            errors.append(f"{label} sha256 mismatch: {rel}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
