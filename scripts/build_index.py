#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Justin Douglas
# SPDX-License-Identifier: MIT
"""
build_index.py — regenerate a chapter's INDEX.md from file frontmatter.

    build_index.py library/projects
    build_index.py library/people --force

Walks a chapter directory and writes an INDEX.md listing every file
with its frontmatter description and status. Directories become
sub-rows; files become table rows.

By default this will NOT overwrite an existing INDEX.md — a
hand-written index carries information the generator can't infer (why
a file exists, what was tried and rejected). Pass --force to replace
one anyway, or --dry-run to see what would be written.

Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Files that are part of the structure, not content.
SKIP_NAMES = {"INDEX.md", "README.md", ".DS_Store", "__pycache__"}


def parse_frontmatter(path: Path) -> dict:
    """Return the frontmatter mapping of a markdown file, or {}."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    data: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and key:
            # Continuation of a list value.
            value = line.strip()
            if value.startswith("-"):
                data.setdefault(key, [])
                if isinstance(data[key], list):
                    data[key].append(value.lstrip("- ").strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("\"'")
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip().strip("\"'") for v in value[1:-1].split(",")]
            data[key] = [i for i in items if i]
        else:
            data[key] = value
    return data


def first_paragraph(path: Path) -> str:
    """First non-heading, non-empty paragraph after the frontmatter."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "<!--", "**", "|", "---")):
            continue
        return s
    return ""


def describe(path: Path) -> tuple[str, str]:
    """Return (description, status) for a markdown file."""
    fm = parse_frontmatter(path)
    desc = fm.get("description") or fm.get("summary") or ""
    if not desc:
        desc = first_paragraph(path)
    status = fm.get("status", "")
    return desc, status


def humanize(name: str) -> str:
    """`CURRENT_STATE.md` -> `CURRENT STATE`."""
    stem = name[:-3] if name.endswith(".md") else name
    return stem.replace("_", " ").replace("-", " ").strip()


def collect(chapter: Path) -> tuple[list, list]:
    """Return (files, subdirectories) for a chapter."""
    files, dirs = [], []
    for entry in sorted(chapter.iterdir(), key=lambda p: p.name.lower()):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            if entry.name in SKIP_NAMES:
                continue
            dirs.append(entry)
        elif entry.is_file() and entry.suffix == ".md":
            if entry.name in SKIP_NAMES:
                continue
            files.append(entry)
    return files, dirs


def render(chapter: Path, files: list, dirs: list) -> str:
    chapter_name = chapter.name.upper()
    rel = chapter.as_posix()
    today = _dt.date.today().isoformat()

    out = [
        f"# {chapter_name} — chapter index",
        "",
        f"**Chapter root:** `{rel}/`",
        f"**Purpose:** {first_paragraph(chapter / 'INDEX.md') if (chapter / 'INDEX.md').exists() else 'See the repository README.'}",
        f"**Last updated:** {today}",
        "",
        "---",
        "",
    ]

    if dirs:
        out += ["## Directories", "", "| Directory | What it is | Status |",
                "|---|---|---|"]
        for d in dirs:
            desc, status = describe(d / "README.md") if (d / "README.md").exists() else ("", "")
            if not desc:
                desc = first_paragraph(d / "INDEX.md") if (d / "INDEX.md").exists() else ""
            if not desc:
                desc = f"`{d.name}/`"
            out.append(f"| `{d.name}/` | {desc} | {status or '—'} |")
        out.append("")

    if files:
        out += ["## Files", "", "| File | What it is | Status |",
                "|---|---|---|"]
        for f in files:
            desc, status = describe(f)
            if not desc:
                desc = f"`{humanize(f.name)}`"
            out.append(f"| `{f.name}` | {desc} | {status or '—'} |")
        out.append("")

    out += [
        "---",
        "",
        "**Open the file, not this index, when you want the detail.**",
        "This is a map.",
        "",
    ]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Regenerate a chapter INDEX.md from file frontmatter.")
    ap.add_argument("chapter", help="Path to the chapter directory")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing INDEX.md")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the result instead of writing it")
    args = ap.parse_args()

    chapter = Path(args.chapter).expanduser().resolve()
    if not chapter.is_dir():
        print(f"error: not a directory: {chapter}", file=sys.stderr)
        return 1

    target = chapter / "INDEX.md"
    files, dirs = collect(chapter)
    content = render(chapter, files, dirs)

    if target.exists() and not args.force and not args.dry_run:
        print(f"refusing to overwrite {target} (use --force)", file=sys.stderr)
        return 1

    if args.dry_run:
        print(content)
        return 0

    target.write_text(content, encoding="utf-8")
    print(f"wrote {target}  ({len(files)} files, {len(dirs)} dirs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
