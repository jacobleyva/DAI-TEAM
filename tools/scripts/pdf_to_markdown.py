#!/usr/bin/env python3
"""Convert PDF files into AI-friendly Markdown collections."""

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
from typing import Iterable

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class ExtractionResult:
    backend: str
    text: str
    page_count: int | None = None
    extracted_pages: str | None = None


@dataclass
class ConversionRecord:
    source_file: str
    source_path: str
    output_path: str
    title: str
    extractor: str
    page_count: int | None
    group: str | None = None
    extracted_pages: str | None = None
    source_sha256: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDFs into cleaned Markdown for AI workflows."
    )
    parser.add_argument("inputs", nargs="+", help="PDF file(s) or directories containing PDFs.")
    parser.add_argument("-o", "--output-dir", help="Directory to write Markdown files into.")
    parser.add_argument("--recursive", action="store_true", help="Recurse into directories.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs.")
    parser.add_argument(
        "--title-from-filename",
        action="store_true",
        help="Always derive the Markdown title from the PDF filename.",
    )
    parser.add_argument(
        "--knowledge-root",
        help="Create a knowledge-style output tree under this directory.",
    )
    parser.add_argument(
        "--collection",
        default="pdf-ingest",
        help="Collection name to use under --knowledge-root.",
    )
    parser.add_argument(
        "--extractor",
        choices=("auto", "pymupdf", "pypdf", "mdls"),
        default="auto",
        help="Preferred extractor. auto picks a sensible default.",
    )
    parser.add_argument("--start-page", type=int, default=1, help="1-based start page.")
    parser.add_argument("--max-pages", type=int, help="Maximum number of pages to extract.")
    parser.add_argument(
        "--auto-chunk-pages",
        type=int,
        help="Automatically split paged PDFs into chunks of this many pages.",
    )
    parser.add_argument(
        "--delete-source-on-success",
        action="store_true",
        help="Delete the source PDF only after all output for that PDF succeeds.",
    )
    parser.add_argument(
        "--move-source-on-success-dir",
        help="Directory to move successfully processed source PDFs into.",
    )
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_path_for_compare(path: str | Path) -> str:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = (WORKSPACE_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return str(candidate).lower()


def path_for_metadata(path: Path) -> str:
    resolved = path.expanduser().resolve()
    try:
        return resolved.relative_to(WORKSPACE_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def resolve_record_path(path: str) -> Path:
    candidate = Path(path).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (WORKSPACE_ROOT / candidate).resolve()


def derive_record_group(source_path: str | Path) -> str | None:
    candidate = Path(source_path)
    path_text = candidate.as_posix().lower()
    file_text = candidate.name.lower()
    mobile_api_reference_markers = (
        "api refrence mobile",
        "api reference mobile",
    )
    if any(marker in path_text or marker in file_text for marker in mobile_api_reference_markers):
        return "API REFERENCES Mobile"
    if "knowledge/" in path_text or path_text.startswith("knowledge"):
        return "API REFERENCES"
    return None


def already_ingested(
    existing_records: list[ConversionRecord], pdf_path: Path, source_hash: str
) -> bool:
    normalized_pdf_path = normalize_path_for_compare(pdf_path)
    for record in existing_records:
        if record.source_sha256 and record.source_sha256 == source_hash:
            return True
        if record.source_path and normalize_path_for_compare(record.source_path) == normalized_pdf_path:
            return True
    return False


def discover_pdfs(inputs: Iterable[str], recursive: bool) -> list[Path]:
    pdfs: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Input not found: {path}")
        if path.is_file():
            if path.suffix.lower() != ".pdf":
                raise ValueError(f"Expected a PDF file: {path}")
            pdfs.append(path)
            continue
        pattern = "**/*.pdf" if recursive else "*.pdf"
        pdfs.extend(sorted(path.glob(pattern)))
    seen: set[Path] = set()
    deduped: list[Path] = []
    for pdf in pdfs:
        if pdf not in seen:
            seen.add(pdf)
            deduped.append(pdf)
    return deduped


def extract_with_pymupdf(
    pdf_path: Path, start_page: int = 1, max_pages: int | None = None
) -> ExtractionResult | None:
    try:
        import fitz  # type: ignore
    except Exception:
        return None

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    first_page = max(start_page, 1)
    last_page = total_pages if max_pages is None else min(total_pages, first_page + max_pages - 1)
    pages: list[str] = []
    for index in range(first_page, last_page + 1):
        page = doc.load_page(index - 1)
        text = (page.get_text("text") or "").strip()
        pages.append(f"<!-- page {index} -->\n{text}" if text else f"<!-- page {index} -->")
    joined = "\n\n".join(pages).strip()
    extracted_pages = f"{first_page}-{last_page}" if first_page != last_page else str(first_page)
    return ExtractionResult("pymupdf", joined, total_pages, extracted_pages)


def extract_with_pypdf(
    pdf_path: Path, start_page: int = 1, max_pages: int | None = None
) -> ExtractionResult | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    first_page = max(start_page, 1)
    last_page = total_pages if max_pages is None else min(total_pages, first_page + max_pages - 1)
    pages: list[str] = []
    for index in range(first_page, last_page + 1):
        page = reader.pages[index - 1]
        text = (page.extract_text() or "").strip()
        pages.append(f"<!-- page {index} -->\n{text}" if text else f"<!-- page {index} -->")
    joined = "\n\n".join(pages).strip()
    extracted_pages = f"{first_page}-{last_page}" if first_page != last_page else str(first_page)
    return ExtractionResult("pypdf", joined, total_pages, extracted_pages)


def extract_with_mdls(pdf_path: Path) -> ExtractionResult | None:
    if sys.platform != "darwin" or shutil.which("mdls") is None:
        return None
    proc = subprocess.run(
        ["/usr/bin/mdls", "-raw", "-name", "kMDItemTextContent", str(pdf_path)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return None
    text = proc.stdout.strip()
    if not text or text == "(null)":
        return None
    return ExtractionResult("mdls", text)


def extractor_order(pdf_path: Path, preference: str) -> tuple:
    if preference == "pymupdf":
        return (extract_with_pymupdf, extract_with_pypdf, extract_with_mdls)
    if preference == "pypdf":
        return (extract_with_pypdf, extract_with_pymupdf, extract_with_mdls)
    if preference == "mdls":
        return (extract_with_mdls, extract_with_pymupdf, extract_with_pypdf)
    if pdf_path.stat().st_size > 50 * 1024 * 1024:
        return (extract_with_pymupdf, extract_with_pypdf, extract_with_mdls)
    return (extract_with_pypdf, extract_with_pymupdf, extract_with_mdls)


def extract_text(
    pdf_path: Path, preference: str, start_page: int = 1, max_pages: int | None = None
) -> ExtractionResult:
    for extractor in extractor_order(pdf_path, preference):
        if extractor in (extract_with_pypdf, extract_with_pymupdf):
            result = extractor(pdf_path, start_page=start_page, max_pages=max_pages)
        else:
            result = extractor(pdf_path)
        if result and result.text.strip():
            return result
    raise RuntimeError("No supported PDF text extractor succeeded.")


def get_total_pages(pdf_path: Path, preference: str) -> int | None:
    for extractor in extractor_order(pdf_path, preference):
        if extractor is extract_with_pymupdf:
            try:
                import fitz  # type: ignore
                return len(fitz.open(pdf_path))
            except Exception:
                continue
        if extractor is extract_with_pypdf:
            try:
                from pypdf import PdfReader  # type: ignore
                return len(PdfReader(str(pdf_path)).pages)
            except Exception:
                continue
    return None


def normalize_inline_space(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def humanize_filename(name: str) -> str:
    cleaned = re.sub(r"[_-]+", " ", name).strip()
    cleaned = cleaned.replace(".", " ")
    cleaned = re.sub(r"\brefrence\b", "reference", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", cleaned)
    cleaned = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return "Untitled Document"

    words: list[str] = []
    for token in cleaned.split(" "):
        if token.isupper():
            words.append(token)
        elif any(ch.isupper() for ch in token[1:]):
            words.append(token)
        else:
            words.append(token.capitalize())
    return " ".join(words)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "document"


def guess_title(pdf_path: Path, text: str, force_filename: bool) -> str:
    if force_filename:
        return humanize_filename(pdf_path.stem)
    for line in text.splitlines():
        candidate = normalize_inline_space(line)
        if not candidate or len(candidate) > 120 or candidate.startswith("<!-- page"):
            continue
        if re.fullmatch(r"[-_=]{5,}", candidate):
            continue
        if not any(ch.isalnum() for ch in candidate):
            continue
        return candidate
    return humanize_filename(pdf_path.stem)


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = re.sub(r"(?<!\n)\n(?!\n|[#\-*]|<!-- page)", " ", text)
    lines = [normalize_inline_space(line) for line in text.split("\n")]
    cleaned_lines: list[str] = []
    blank_streak = 0
    for line in lines:
        if not line:
            blank_streak += 1
            if blank_streak <= 1:
                cleaned_lines.append("")
            continue
        blank_streak = 0
        cleaned_lines.append(promote_heading(line))
    body = "\n".join(cleaned_lines).strip()
    return re.sub(r"\n{3,}", "\n\n", body)


def promote_heading(line: str) -> str:
    if line.startswith("<!-- page") or line.startswith(("#", "- ", "* ")):
        return line
    if len(line) <= 80 and line.isupper() and any(ch.isalpha() for ch in line):
        return f"## {line.title()}"
    if len(line) <= 90 and line.endswith(":"):
        return f"### {line[:-1]}"
    return line


def build_markdown(
    pdf_path: Path, result: ExtractionResult, force_filename_title: bool
) -> tuple[str, str]:
    body = clean_text(result.text)
    title = guess_title(pdf_path, body, force_filename_title)
    metadata = [
        f"# {title}",
        "",
        "## Source Metadata",
        f"- file: `{pdf_path.name}`",
        f"- path: `{path_for_metadata(pdf_path)}`",
        f"- extractor: `{result.backend}`",
    ]
    if result.page_count is not None:
        metadata.append(f"- pages: `{result.page_count}`")
    if result.extracted_pages is not None:
        metadata.append(f"- extracted_pages: `{result.extracted_pages}`")
    metadata.extend(["", "## Extracted Content", "", body])
    return title, "\n".join(metadata).strip() + "\n"


def output_path_for(pdf_path: Path, output_dir: Path | None, base_input: Path | None) -> Path:
    if output_dir is None:
        return pdf_path.with_suffix(".md")
    if base_input and base_input.is_dir():
        relative = pdf_path.relative_to(base_input)
        return output_dir / relative.with_suffix(".md")
    return output_dir / pdf_path.with_suffix(".md").name


def chunk_suffix(extracted_pages: str | None) -> str:
    if not extracted_pages:
        return ""
    return "-p" + extracted_pages.replace("-", "-p")


def knowledge_output_path(collection_root: Path, pdf_path: Path, seen: dict[str, int], extracted_pages: str | None = None) -> Path:
    stem = slugify(pdf_path.stem) + chunk_suffix(extracted_pages)
    count = seen.get(stem, 0)
    seen[stem] = count + 1
    filename = f"{stem}.md" if count == 0 else f"{stem}-{count + 1}.md"
    target_dir = collection_root / "documents"
    if extracted_pages:
        target_dir = target_dir / "raw-chunks"
    return target_dir / filename




def load_existing_records(collection_root: Path) -> list[ConversionRecord]:
    manifest_json = collection_root / "manifest.json"
    if not manifest_json.exists():
        return []
    try:
        raw = json.loads(manifest_json.read_text())
    except Exception:
        return []
    records: list[ConversionRecord] = []
    for item in raw:
        try:
            records.append(ConversionRecord(**item))
        except Exception:
            continue
    return records

def write_collection_index(collection_root: Path, records: list[ConversionRecord]) -> None:
    index_md = collection_root / "index.md"
    manifest_json = collection_root / "manifest.json"
    lines = ["# PDF Knowledge Collection", "", f"- documents: `{len(records)}`", ""]
    grouped_records: dict[str, list[ConversionRecord]] = {}
    for record in records:
        group_name = record.group or "Ungrouped"
        grouped_records.setdefault(group_name, []).append(record)

    for group_name in sorted(grouped_records):
        lines.extend([f"## {group_name}", ""])
        for record in grouped_records[group_name]:
            rel_path = resolve_record_path(record.output_path).relative_to(collection_root)
            lines.append(f"- [{record.title}]({rel_path.as_posix()})")
            detail = f"source: `{record.source_file}` via `{record.extractor}`"
            if record.extracted_pages:
                detail += f" pages `{record.extracted_pages}`"
            lines.append(f"  {detail}")
        lines.append("")
    index_md.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    manifest_json.write_text(json.dumps([asdict(r) for r in records], indent=2), encoding="utf-8")


def choose_base_input(input_args: list[str]) -> Path | None:
    if len(input_args) != 1:
        return None
    candidate = Path(input_args[0]).expanduser().resolve()
    return candidate if candidate.exists() else None


def iter_chunk_starts(total_pages: int, start_page: int, chunk_pages: int) -> list[int]:
    starts: list[int] = []
    page = max(start_page, 1)
    while page <= total_pages:
        starts.append(page)
        page += chunk_pages
    return starts


def process_single_output(
    pdf_path: Path,
    args: argparse.Namespace,
    collection_root: Path | None,
    output_dir: Path | None,
    base_input: Path | None,
    slug_counts: dict[str, int],
    existing_records: list[ConversionRecord],
) -> list[ConversionRecord]:
    records: list[ConversionRecord] = []
    source_hash = file_sha256(pdf_path)
    if not args.force and already_ingested(existing_records, pdf_path, source_hash):
        print(f"skipped duplicate: {pdf_path}")
        return records
    if args.auto_chunk_pages:
        total_pages = get_total_pages(pdf_path, args.extractor)
        if total_pages is None:
            raise RuntimeError("Could not determine total pages for auto-chunking.")
        starts = iter_chunk_starts(total_pages, args.start_page, args.auto_chunk_pages)
    else:
        starts = [args.start_page]

    for start in starts:
        max_pages = args.auto_chunk_pages or args.max_pages
        result = extract_text(pdf_path, args.extractor, start_page=start, max_pages=max_pages)
        title, markdown = build_markdown(pdf_path, result, args.title_from_filename)
        if collection_root is not None:
            destination = knowledge_output_path(collection_root, pdf_path, slug_counts, result.extracted_pages)
        else:
            destination = output_path_for(pdf_path, output_dir, base_input)
        if destination.exists() and not args.force:
            raise FileExistsError(f"Output exists: {destination} (use --force to overwrite)")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown, encoding="utf-8")
        if result.extracted_pages:
            title = f"{humanize_filename(pdf_path.stem)} ({result.extracted_pages})"
        records.append(
            ConversionRecord(
                source_file=pdf_path.name,
                source_path=path_for_metadata(pdf_path),
                output_path=path_for_metadata(destination),
                title=title,
                group=derive_record_group(path_for_metadata(pdf_path)),
                extractor=result.backend,
                page_count=result.page_count,
                extracted_pages=result.extracted_pages,
                source_sha256=source_hash,
            )
        )
        print(f"converted: {pdf_path} -> {destination} [{result.backend}]")
    return records


def main() -> int:
    args = parse_args()
    try:
        pdfs = discover_pdfs(args.inputs, args.recursive)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not pdfs:
        print("error: no PDFs found", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else None
    knowledge_root = Path(args.knowledge_root).expanduser().resolve() if args.knowledge_root else None
    base_input = choose_base_input(args.inputs)
    failures = 0
    records: list[ConversionRecord] = []
    slug_counts: dict[str, int] = {}

    if knowledge_root is not None:
        collection_root = knowledge_root / slugify(args.collection)
        (collection_root / "documents").mkdir(parents=True, exist_ok=True)
        records = [] if args.force else load_existing_records(collection_root)
    else:
        collection_root = None

    for pdf_path in pdfs:
        try:
            pdf_records = process_single_output(
                pdf_path, args, collection_root, output_dir, base_input, slug_counts, records
            )
            records.extend(pdf_records)
            if args.move_source_on_success_dir:
                completed_dir = Path(args.move_source_on_success_dir).expanduser().resolve()
                completed_dir.mkdir(parents=True, exist_ok=True)
                destination = completed_dir / pdf_path.name
                counter = 2
                while destination.exists():
                    destination = completed_dir / f"{pdf_path.stem}-{counter}{pdf_path.suffix}"
                    counter += 1
                shutil.move(str(pdf_path), str(destination))
                print(f"moved source: {pdf_path} -> {destination}")
            elif args.delete_source_on_success:
                pdf_path.unlink()
                print(f"deleted source: {pdf_path}")
        except Exception as exc:
            failures += 1
            print(f"failed: {pdf_path}: {exc}", file=sys.stderr)

    if collection_root is not None and records:
        write_collection_index(collection_root, records)
        print(f"collection index: {collection_root / 'index.md'}")
        print(f"collection manifest: {collection_root / 'manifest.json'}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
