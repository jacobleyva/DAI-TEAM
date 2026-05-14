#!/usr/bin/env python3
"""Convert DOCX files into local knowledge collection Markdown."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class ConversionRecord:
    source_file: str
    source_path: str
    output_path: str
    title: str
    extractor: str
    group: str
    line_start: int
    line_end: int
    source_sha256: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert DOCX files into a knowledge collection.")
    parser.add_argument("input_dir", help="Directory containing DOCX files.")
    parser.add_argument(
        "--knowledge-root",
        default=str(WORKSPACE_ROOT / "knowledge" / "collections"),
        help="Knowledge collections root.",
    )
    parser.add_argument("--collection", default="best-practices", help="Collection slug/name.")
    parser.add_argument("--chunk-lines", type=int, default=350, help="Maximum cleaned lines per chunk.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing collection.")
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_for_metadata(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "document"


def humanize_filename(name: str) -> str:
    cleaned = re.sub(r"[_-]+", " ", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    words: list[str] = []
    for token in cleaned.split(" "):
        if token.isupper():
            words.append(token)
        elif any(ch.isupper() for ch in token[1:]):
            words.append(token)
        else:
            words.append(token.capitalize())
    return " ".join(words) or "Untitled Document"


def yaml_value(value: object) -> str:
    return json.dumps(value, ensure_ascii=True)


def front_matter(fields: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_value(item)}")
        else:
            lines.append(f"{key}: {yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines)


def discover_docx(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    return sorted(
        path
        for path in input_dir.glob("*.docx")
        if path.is_file() and not path.name.startswith("~$")
    )


def extract_text_with_textutil(path: Path) -> str:
    textutil = shutil.which("textutil")
    if textutil is None:
        raise RuntimeError("textutil is required for DOCX extraction on this machine.")
    proc = subprocess.run(
        [textutil, "-convert", "txt", "-stdout", str(path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "textutil extraction failed")
    return proc.stdout


def clean_lines(raw_text: str) -> list[str]:
    raw_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    raw_text = raw_text.replace("\x0c", "\n\n<!-- page break -->\n\n")
    lines: list[str] = []
    blank_streak = 0
    for raw_line in raw_text.split("\n"):
        line = raw_line.replace("\u00a0", " ").strip()
        line = re.sub(r"[ \t]+", " ", line)
        if not line:
            blank_streak += 1
            if blank_streak <= 1:
                lines.append("")
            continue
        blank_streak = 0
        lines.append(line)
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def chunk_lines(lines: list[str], chunk_size: int) -> list[tuple[int, int, list[str]]]:
    chunks: list[tuple[int, int, list[str]]] = []
    start = 0
    total = len(lines)
    while start < total:
        end = min(start + chunk_size, total)
        if end < total:
            search_start = max(start + int(chunk_size * 0.65), start)
            for candidate in range(end, search_start, -1):
                if lines[candidate - 1] == "" or lines[candidate - 1].startswith("<!-- page break"):
                    end = candidate
                    break
        chunk = lines[start:end]
        chunks.append((start + 1, end, chunk))
        start = end
    return chunks


def chunk_title(base_title: str, start: int, end: int) -> str:
    return f"{base_title} (lines {start}-{end})"


def build_chunk_markdown(
    source_path: Path,
    base_title: str,
    source_hash: str,
    start: int,
    end: int,
    body_lines: list[str],
) -> str:
    title = chunk_title(base_title, start, end)
    fields = {
        "title": title,
        "type": "source-chunk",
        "domain": "servicenow",
        "product": "ServiceNow Best Practices",
        "audience": "team",
        "owner": "team",
        "status": "active",
        "updated": "2026-04-27",
        "tags": ["knowledge", "best-practices", "servicenow", "process-guide"],
        "artifact_type": "knowledge-source-chunk",
        "source_file": source_path.name,
        "source_path": path_for_metadata(source_path),
        "source_sha256": source_hash,
        "line_start": start,
        "line_end": end,
    }
    body = "\n".join(body_lines).strip()
    return (
        f"{front_matter(fields)}\n\n"
        f"# {title}\n\n"
        "## Source Metadata\n\n"
        f"- file: `{source_path.name}`\n"
        f"- path: `{path_for_metadata(source_path)}`\n"
        "- extractor: `textutil-docx`\n"
        f"- lines: `{start}-{end}`\n\n"
        "## Extracted Content\n\n"
        f"{body}\n"
    )


def write_collection_index(collection_root: Path, records: list[ConversionRecord]) -> None:
    fields = {
        "title": "Best Practices Collection",
        "type": "index",
        "domain": "servicenow",
        "product": "ServiceNow Best Practices",
        "audience": "team",
        "owner": "team",
        "status": "active",
        "updated": "2026-04-27",
        "tags": ["knowledge", "best-practices", "index", "collection"],
        "artifact_type": "knowledge-collection-index",
    }
    lines = [
        front_matter(fields),
        "",
        "# Best Practices Collection",
        "",
        f"- documents: `{len(records)}`",
        "",
        "## Process Guides",
        "",
    ]
    for record in records:
        rel_path = Path(record.output_path)
        if rel_path.is_absolute():
            rel_path = rel_path.relative_to(collection_root)
        else:
            rel_path = (WORKSPACE_ROOT / rel_path).resolve().relative_to(collection_root)
        lines.append(f"- [{record.title}]({rel_path.as_posix()})")
        lines.append(
            f"  source: `{record.source_file}` via `{record.extractor}` lines `{record.line_start}-{record.line_end}`"
        )
    (collection_root / "index.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_topic(collection_root: Path, source_titles: list[str]) -> None:
    fields = {
        "title": "Best Practices Topic",
        "type": "topic",
        "domain": "servicenow",
        "product": "ServiceNow Best Practices",
        "audience": "team",
        "owner": "team",
        "status": "active",
        "updated": "2026-04-27",
        "tags": ["knowledge", "best-practices", "servicenow", "process-guide"],
        "artifact_type": "knowledge-topic",
    }
    lines = [
        front_matter(fields),
        "",
        "# Best Practices Topic",
        "",
        "This topic bridges into the ingested ServiceNow best-practice process guides.",
        "",
        "## Included Guides",
        "",
    ]
    for title in source_titles:
        lines.append(f"- {title}")
    lines.extend(
        [
            "",
            "## Navigation",
            "",
            "- [Generated Collection Index](../index.md)",
            "- [Best Practices Collection](../best-practices-collection.md)",
            "",
            "## Suggested Use",
            "",
            "- start here when comparing ServiceNow process guidance across ITSM, DEX, release, request, and workforce practices",
            "- use the generated index for exact source chunks and line ranges",
            "- promote local implementation decisions into `projects/` or `memory/` after validating them against the relevant guide",
        ]
    )
    topic_path = collection_root / "documents" / "best-practices-topic.md"
    topic_path.parent.mkdir(parents=True, exist_ok=True)
    topic_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def write_collection_page(collection_root: Path) -> None:
    fields = {
        "title": "Best Practices Collection",
        "type": "collection",
        "domain": "servicenow",
        "product": "ServiceNow Best Practices",
        "audience": "team",
        "owner": "team",
        "status": "active",
        "updated": "2026-04-27",
        "tags": ["knowledge", "best-practices", "servicenow", "collection"],
        "artifact_type": "knowledge-collection",
    }
    lines = [
        front_matter(fields),
        "",
        "# Best Practices Collection",
        "",
        "This collection captures ServiceNow best-practice process guides provided from the local `Best Practices` source folder.",
        "",
        "## Main Topic",
        "",
        "- [Best Practices Topic](./documents/best-practices-topic.md)",
        "",
        "## Main Index",
        "",
        "- [Generated Collection Index](./index.md)",
        "",
        "## Suggested Use",
        "",
        "- use this collection for ServiceNow process design, implementation alignment, and operating model comparisons",
        "- use topic and index pages before dropping into raw chunks",
        "- cite specific raw chunks when extracting process roles, state models, governance metrics, or scoping considerations",
    ]
    (collection_root / "best-practices-collection.md").write_text(
        "\n".join(lines).strip() + "\n", encoding="utf-8"
    )


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir).expanduser().resolve()
    knowledge_root = Path(args.knowledge_root).expanduser().resolve()
    collection_root = knowledge_root / slugify(args.collection)

    try:
        docx_files = discover_docx(input_dir)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not docx_files:
        print("error: no DOCX files found", file=sys.stderr)
        return 1
    if collection_root.exists() and args.force:
        shutil.rmtree(collection_root)
    elif collection_root.exists():
        print(f"error: collection already exists: {collection_root} (use --force)", file=sys.stderr)
        return 1

    raw_chunks_dir = collection_root / "documents" / "raw-chunks"
    raw_chunks_dir.mkdir(parents=True, exist_ok=True)

    records: list[ConversionRecord] = []
    source_titles: list[str] = []
    for docx_path in docx_files:
        base_title = humanize_filename(docx_path.stem)
        source_titles.append(base_title)
        source_hash = file_sha256(docx_path)
        lines = clean_lines(extract_text_with_textutil(docx_path))
        chunks = chunk_lines(lines, args.chunk_lines)
        for start, end, body_lines in chunks:
            title = chunk_title(base_title, start, end)
            filename = f"{slugify(base_title)}-l{start}-l{end}.md"
            output_path = raw_chunks_dir / filename
            output_path.write_text(
                build_chunk_markdown(docx_path, base_title, source_hash, start, end, body_lines),
                encoding="utf-8",
            )
            records.append(
                ConversionRecord(
                    source_file=docx_path.name,
                    source_path=path_for_metadata(docx_path),
                    output_path=path_for_metadata(output_path),
                    title=title,
                    extractor="textutil-docx",
                    group="BEST PRACTICES",
                    line_start=start,
                    line_end=end,
                    source_sha256=source_hash,
                )
            )
        print(f"converted: {docx_path} -> {len(chunks)} chunk(s)")

    write_topic(collection_root, source_titles)
    write_collection_page(collection_root)
    write_collection_index(collection_root, records)
    (collection_root / "manifest.json").write_text(
        json.dumps([asdict(record) for record in records], indent=2), encoding="utf-8"
    )
    print(f"collection index: {collection_root / 'index.md'}")
    print(f"collection manifest: {collection_root / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
