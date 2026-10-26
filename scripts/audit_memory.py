#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Justin Douglas
# SPDX-License-Identifier: MIT
"""
audit_memory.py — health check for a memory library.

    audit_memory.py
    audit_memory.py --root ~/my-agent-memory
    audit_memory.py --check-links

Checks:
  * index size against the 2,000-char target / 4,000-char ceiling
  * files in the library that no index mentions (orphans)
  * pointers in any index that reference a file that doesn't exist
  * archive directories with no RECOVERY_README.md
  * library files missing frontmatter or a Last-updated header

Exit code is 0 when everything is clean, 1 when something needs
attention, 2 on a usage error. That makes it CI- and cron-friendly.

Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
PATH_REF_RE = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|txt|json|yaml|yml))`")

# Directories that hold structure rather than content.
STRUCTURE_DIRS = {"archive", "scripts"}

INDEX_TARGET = 2_000
INDEX_CEILING = 4_000

SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".obsidian"}


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def find_index(library: Path) -> Path | None:
    """Locate MEMORY.md — either beside the library or inside it."""
    for cand in (library.parent / "MEMORY.md", library / "MEMORY.md"):
        if cand.is_file():
            return cand
    return None


def check_index_size(index: Path | None, f: Findings) -> None:
    if not index:
        f.error("no MEMORY.md found (looked beside the library and inside it). "
                "Copy MEMORY.md from the repo root next to your library, or point "
                "--index at it.")
        return
    size = len(read(index))
    if size > INDEX_CEILING:
        f.error(f"index is {size} chars — over the {INDEX_CEILING} hard ceiling")
    elif size > INDEX_TARGET:
        f.warn(f"index is {size} chars — over the {INDEX_TARGET} target "
               f"(move content into the library, leave a pointer)")
    else:
        f.note(f"index is {size} chars (target {INDEX_TARGET}, "
               f"ceiling {INDEX_CEILING})")


def collect_markdown(library: Path) -> list[Path]:
    out = []
    for p in library.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def collect_index_files(library: Path) -> list[Path]:
    out = []
    for p in library.rglob("INDEX.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def check_orphans(library: Path, f: Findings) -> None:
    """Files no index mentions."""
    indices = collect_index_files(library)
    if not indices:
        f.warn("no chapter INDEX.md files found — the library is unsearchable")
        return

    indexed: set[str] = set()
    for idx in indices:
        for m in PATH_REF_RE.finditer(read(idx)):
            indexed.add(m.group(1))

    orphans = []
    for md in collect_markdown(library):
        if md.name == "INDEX.md":
            continue
        rel = md.relative_to(library).as_posix()
        if md.parent.name in STRUCTURE_DIRS:
            continue
        # The log chapter index lists eras, not every individual day.
        if md.parent.name == "log":
            continue
        if any(rel in ref or Path(ref).name == md.name for ref in indexed):
            continue
        orphans.append(rel)

    if orphans:
        f.warn(f"{len(orphans)} file(s) not mentioned in any chapter index:")
        for o in orphans[:20]:
            f.notes.append(f"    orphan: {o}")
        if len(orphans) > 20:
            f.notes.append(f"    ... and {len(orphans) - 20} more")
    else:
        f.note("every library file is referenced by a chapter index")


def check_links(library: Path, index: Path | None, f: Findings) -> None:
    """Pointers that reference files that don't exist."""
    targets = []
    if index:
        targets.append(index)
    targets.extend(collect_index_files(library))

    broken = []
    for src in targets:
        text = read(src)
        for m in PATH_REF_RE.finditer(text):
            ref = m.group(1)
            if ref.startswith("http"):
                continue
            if Path(ref).name == "RECOVERY_README.md":
                continue  # a template reference, not a real pointer
            # Try relative to the source, relative to the library, and
            # relative to the library's parent.
            cands = [
                (src.parent / ref),
                (library / ref),
                (library.parent / ref),
            ]
            if not any(c.is_file() for c in cands):
                broken.append((src.relative_to(library.parent).as_posix()
                               if library.parent in src.parents else src.name, ref))

    if broken:
        f.warn(f"{len(broken)} broken pointer(s) in indices:")
        for src, ref in broken[:20]:
            f.notes.append(f"    {src} -> {ref}")
    else:
        f.note("all pointers in indices resolve")


def check_archives(library: Path, f: Findings) -> None:
    archive = library / "archive"
    if not archive.is_dir():
        return
    problems = []
    for d in sorted(archive.iterdir()):
        if not d.is_dir():
            continue
        if not (d / "RECOVERY_README.md").exists():
            problems.append(d.name)
    if problems:
        f.warn(f"{len(problems)} archive dir(s) with no RECOVERY_README.md:")
        for p in problems[:15]:
            f.notes.append(f"    {p}")
    else:
        f.note("every archive directory has a RECOVERY_README.md")


def check_frontmatter(library: Path, f: Findings) -> None:
    """Library files missing frontmatter or a Last-updated header."""
    missing_fm, missing_hdr = [], []
    for md in collect_markdown(library):
        if md.name in ("INDEX.md", "README.md", "RECOVERY_README.md",
                       "MEMORY.md"):
            continue
        if md.parent.name in STRUCTURE_DIRS:
            continue
        # Daily logs are append-only and machine-written — they get a
        # standard section skeleton, not frontmatter. Don't demand more.
        if md.parent.name == "log":
            continue
        text = read(md)
        if not FRONTMATTER_RE.match(text):
            missing_fm.append(md.relative_to(library).as_posix())
        if "**Last updated:**" not in text:
            missing_hdr.append(md.relative_to(library).as_posix())

    if missing_fm:
        f.warn(f"{len(missing_fm)} file(s) without frontmatter:")
        for m in missing_fm[:15]:
            f.notes.append(f"    {m}")
    else:
        f.note("every library file has frontmatter")

    if missing_hdr:
        f.warn(f"{len(missing_hdr)} file(s) without a 'Last updated' header:")
        for m in missing_hdr[:15]:
            f.notes.append(f"    {m}")
    else:
        f.note("every library file has a 'Last updated' header")


def main() -> int:
    ap = argparse.ArgumentParser(description="Health check for a memory library.")
    ap.add_argument("--root", default=None,
                    help="Path to the library (default: ./library beside this script)")
    ap.add_argument("--check-links", action="store_true",
                    help="Also verify that pointers in indices resolve")
    ap.add_argument("--quiet", action="store_true",
                    help="Only print problems, not notes")
    args = ap.parse_args()

    if args.root:
        library = Path(args.root).expanduser().resolve()
    else:
        library = (Path(__file__).resolve().parent.parent / "library").resolve()

    if not library.is_dir():
        print(f"error: library not found: {library}", file=sys.stderr)
        return 2

    f = Findings()
    index = find_index(library)

    print(f"Memory library audit")
    print(f"  root:  {library}")
    print(f"  index: {index if index else '(not found)'}")
    print()

    check_index_size(index, f)
    check_orphans(library, f)
    check_archives(library, f)
    check_frontmatter(library, f)
    if args.check_links:
        check_links(library, index, f)

    if not args.quiet:
        if f.notes:
            print("Notes")
            for n in f.notes:
                if n.startswith("    "):
                    print(n)
                else:
                    print(f"  · {n}")
            print()

    if f.warnings:
        print(f"Warnings ({len(f.warnings)})")
        for w in f.warnings:
            print(f"  ⚠ {w}")
        print()

    if f.errors:
        print(f"Errors ({len(f.errors)})")
        for e in f.errors:
            print(f"  ✗ {e}")
        print()

    if not f.errors and not f.warnings:
        print("✓ Clean — no problems found.")
        return 0
    if f.errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
