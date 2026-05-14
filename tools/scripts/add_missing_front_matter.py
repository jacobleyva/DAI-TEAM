#!/usr/bin/env python3
"""Add YAML front matter to durable Markdown files that are missing it."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPDATED = "2026-04-23"

DEFAULT_TARGETS = [
    "knowledge",
    "memory",
    "projects",
    "team",
    "core",
    "templates",
]

EXCLUDED_PATH_PARTS = {
    "documents/raw-chunks",
}

EXCLUDED_FILENAMES = {
    "README.md",
}

DOMAIN_PRODUCT_MAP = {
    "dai": "DAI",
    "servicenow": "ServiceNow",
    "fiserv": "Fiserv",
    "saviynt": "Saviynt",
    "webex": "Webex",
    "granite": "Granite",
    "tenable": "Tenable",
    "hyland": "Hyland",
    "cis": "CIS Controls",
}

COLLECTION_DOMAIN_MAP = {
    "cis-controls-v8-1": ("security", "CIS Controls v8.1"),
    "granite-customer-api": ("granite", "Granite Customer API"),
    "hyland-apis": ("hyland", "Hyland APIs"),
    "saviynt-integrations": ("saviynt", "Saviynt Integrations"),
    "servicenow-yokohama-full": ("servicenow", "ServiceNow Yokohama"),
    "servicenow-yokohama-it-asset-management": ("servicenow", "ServiceNow Yokohama IT Asset Management"),
    "servicenow-yokohama-security-management": ("servicenow", "ServiceNow Yokohama Security Management"),
    "tenable-integrations": ("tenable", "Tenable Integrations"),
    "webex-integrations": ("webex", "Webex Integrations"),
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "vs",
    "with",
}


def should_skip(path: Path) -> bool:
    as_posix = path.as_posix()
    if any(part in as_posix for part in EXCLUDED_PATH_PARTS):
        return True
    if path.name in EXCLUDED_FILENAMES:
        return True
    return False


def has_front_matter(path: Path) -> bool:
    with path.open("r", encoding="utf-8") as handle:
        return handle.readline().strip() == "---"


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for target in DEFAULT_TARGETS:
        base = ROOT / target
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(ROOT)
            if should_skip(rel):
                continue
            files.append(path)
    return files


def extract_title(text: str, fallback: Path) -> str:
    if fallback.parts[:2] == ("knowledge", "collections") and fallback.name == "index.md":
        collection = fallback.parts[2]
        return f"{COLLECTION_DOMAIN_MAP.get(collection, (None, collection.replace('-', ' ').title()))[1]} Collection"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    stem = fallback.stem.replace("-", " ").replace("_", " ")
    return " ".join(word.capitalize() for word in stem.split())


def tokenize(value: str) -> list[str]:
    cleaned = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return [token for token in cleaned.split() if token and not token.isdigit()]


def infer_domain(rel: Path, text: str) -> str:
    rel_parts = [part.lower() for part in rel.parts]
    rel_text = rel.as_posix().lower()
    for candidate in ("saviynt", "fiserv", "webex", "granite", "tenable", "hyland", "servicenow", "dai"):
        if candidate in rel_parts or candidate in rel_text:
            return candidate
    if rel.parts[0] == "knowledge":
        collection = rel.parts[2] if len(rel.parts) > 2 else ""
        return COLLECTION_DOMAIN_MAP.get(collection, ("knowledge", "Knowledge"))[0]
    if rel.parts[0] in {"core", "team", "templates"}:
        return "dai"
    if rel.parts[0] == "memory":
        body = text.lower()
        for candidate in ("saviynt", "fiserv", "webex", "granite", "tenable", "hyland", "servicenow"):
            if candidate in body:
                return candidate
        return "dai"
    return "dai"


def infer_product(rel: Path, domain: str) -> str:
    if rel.parts[0] == "knowledge" and len(rel.parts) > 2:
        collection = rel.parts[2]
        if collection in COLLECTION_DOMAIN_MAP:
            return COLLECTION_DOMAIN_MAP[collection][1]
    if rel.parts[0] == "projects":
        project = rel.parts[1]
        if project == "servicenow-core":
            return "ServiceNow"
        if project == "saviynt-servicenow":
            return "ServiceNow"
        if project == "fiserv-api-servicenow":
            return "Fiserv"
        if project == "webex-api-emulator":
            return "Webex"
    return DOMAIN_PRODUCT_MAP.get(domain, "DAI")


def infer_type_and_artifact(rel: Path) -> tuple[str, str]:
    parts = rel.parts
    filename = rel.name
    if parts[0] == "knowledge":
        return "index", "knowledge-collection-index"
    if parts[0] == "memory":
        section = parts[1]
        if section == "decisions":
            return "decision", "decision-record"
        if section == "learnings":
            return "learning", "learning-record"
        if section == "session-summaries":
            return "session-summary", "session-summary"
    if parts[0] == "projects":
        return "note", "project-note"
    if parts[0] == "team":
        return "guide", "team-guide"
    if parts[0] == "core":
        if filename.endswith("-map.md"):
            return "map", "core-map"
        return "rule", "operating-rule"
    if parts[0] == "templates":
        if filename.endswith("-map.md"):
            return "map", "templates-map"
        return "template", "template"
    return "note", "document"


def infer_tags(rel: Path, title: str, doc_type: str, artifact_type: str, domain: str) -> list[str]:
    tokens: list[str] = []
    if domain not in {"knowledge", ""}:
        tokens.append(domain)
    top = rel.parts[0]
    if top == "knowledge":
        tokens.extend(["knowledge", "index"])
    elif top == "memory":
        tokens.append("memory")
        tokens.append(rel.parts[1].replace("session-summaries", "session-summary").replace("learnings", "learning"))
    elif top == "projects":
        tokens.append("project")
    elif top == "team":
        tokens.append("team")
    elif top == "core":
        tokens.append("governance")
    elif top == "templates":
        tokens.append("template")

    tokens.append(doc_type)
    if artifact_type != doc_type:
        tokens.extend(tokenize(artifact_type))

    for token in tokenize(title):
        if token in STOPWORDS:
            continue
        if token not in tokens:
            tokens.append(token)

    deduped: list[str] = []
    for token in tokens:
        if token not in deduped:
            deduped.append(token)
    return deduped[:8]


def front_matter(rel: Path, text: str) -> str:
    title = extract_title(text, rel)
    domain = infer_domain(rel, text)
    product = infer_product(rel, domain)
    doc_type, artifact_type = infer_type_and_artifact(rel)
    tags = infer_tags(rel, title, doc_type, artifact_type, domain)

    lines = [
        "---",
        f"title: {title}",
        f"type: {doc_type}",
        f"domain: {domain}",
        f"product: {product}",
        "audience: team",
        "owner: team",
        "status: active",
        f"updated: {UPDATED}",
        "tags:",
    ]
    for tag in tags:
        lines.append(f"  - {tag}")
    lines.append(f"artifact_type: {artifact_type}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    updated_paths: list[Path] = []
    for path in iter_markdown_files():
        if has_front_matter(path):
            continue
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        fm = front_matter(rel, text)
        path.write_text(fm + text, encoding="utf-8")
        updated_paths.append(rel)

    for rel in updated_paths:
        print(rel.as_posix())
    print(f"Updated {len(updated_paths)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
