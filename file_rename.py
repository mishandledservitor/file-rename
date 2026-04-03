#!/usr/bin/env python3
"""
file_rename.py — Batch file renamer

Usage:
    python3 file_rename.py [folder]

Pattern syntax:
    NN / NNN / NNNN  →  sequential number  (N count = zero-pad width)
    RND              →  random 8-char alphanumeric string

Examples:
    image-NN         →  image-01.jpg, image-02.jpg …
    shot_NNNN        →  shot_0001.jpg, shot_0002.jpg …
    img-RND          →  img-a8f3k2xq.jpg …
"""

__version__ = "3.0.0"

import os
import random
import re
import shutil
import string
import sys

RAND_CHARS = string.ascii_lowercase + string.digits
RAND_LENGTH = 8


# ── Core ─────────────────────────────────────────────────────────────────────

def get_files(folder):
    return sorted(
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and not f.startswith(".")
    )


def make_stem(pattern, index, rand):
    result = re.sub(r"N{2,}", lambda m: str(index).zfill(len(m.group())), pattern)
    result = result.replace("RND", rand)
    return result


def build_plan(folder, files, pattern):
    used: set[str] = set()
    plan = []
    for i, fname in enumerate(files, 1):
        _, ext = os.path.splitext(fname)
        if "RND" in pattern:
            for _ in range(100_000):
                r = "".join(random.choices(RAND_CHARS, k=RAND_LENGTH))
                if r not in used:
                    used.add(r)
                    break
            else:
                print("  ⚠  Could not generate enough unique names — try a longer RND length")
                return []
        else:
            r = ""
        plan.append((fname, make_stem(pattern, i, r) + ext))
    return plan


def validate_pattern(pattern):
    """Return a warning string, or None if the pattern looks valid."""
    has_seq = bool(re.search(r"N{2,}", pattern))
    has_rnd = "RND" in pattern
    if not has_seq and not has_rnd:
        return "pattern has no NN or RND placeholder — all files would get the same name"
    if has_seq and has_rnd:
        return "pattern has both NN and RND — that works, just checking you meant it"
    return None


# ── Display ───────────────────────────────────────────────────────────────────

def tw():
    return shutil.get_terminal_size((80, 20)).columns


def show_preview(plan, folder):
    col = min(48, (tw() - 8) // 2)
    conflicts = 0
    rows = []
    for old, new in plan:
        trunc = (old[: col - 1] + "…") if len(old) > col else old
        new_path = os.path.join(folder, new)
        old_path = os.path.join(folder, old)
        conflict = "  ⚠ conflict" if os.path.exists(new_path) and new_path != old_path else ""
        if conflict:
            conflicts += 1
        rows.append((trunc, new, conflict))

    print()
    # Compact view for large sets: first 5 … last 1
    if len(rows) > 12:
        display = rows[:5] + [None] + rows[-1:]
    else:
        display = rows

    for row in display:
        if row is None:
            print(f"  {'  …  ' + str(len(rows) - 6) + ' more …':>{col}}  →")
        else:
            trunc, new, conflict = row
            print(f"  {trunc:<{col}}  →  {new}{conflict}")

    print()
    if conflicts:
        print(f"  ⚠  {conflicts} conflict(s) will be skipped\n")


def apply_plan(plan, folder):
    ok = skipped = 0
    for old, new in plan:
        op = os.path.join(folder, old)
        np = os.path.join(folder, new)
        if os.path.exists(np) and np != op:
            skipped += 1
            continue
        try:
            os.rename(op, np)
            ok += 1
        except Exception as e:
            print(f"  ⚠  {old}: {e}")
    msg = f"  ✅ Done!  {ok} renamed"
    if skipped:
        msg += f",  {skipped} skipped"
    print(msg + "\n")


def print_header(folder, files):
    count = f"  ({len(files)} files)" if files is not None else ""
    print("\n╔══════════════════════════════════════════════╗")
    print("║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\n  Folder: {folder or 'not set'}{count}\n")
    print("  Type a pattern — NN = sequential,  RND = random:\n")
    print("    image-NN      →  image-01.jpg, image-02.jpg …")
    print("    shot_NNNN     →  shot_0001.jpg, shot_0002.jpg …")
    print("    file-RND      →  file-a8f3k2xq.jpg …\n")
    print("  /folder <path>   change folder     /quit   exit\n")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Batch file renamer — type a pattern like image-NN")
    ap.add_argument("folder", nargs="?", help="Folder to rename files in")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args()

    folder = None
    files = None

    if args.folder:
        p = os.path.abspath(os.path.expanduser(args.folder))
        if not os.path.isdir(p):
            print(f"⚠  Not a directory: {p}")
            sys.exit(1)
        folder = p
        files = get_files(folder)

    print_header(folder, files)

    while True:
        try:
            text = input("  ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋 Goodbye!\n")
            break

        if not text:
            continue

        # ── Builtins ─────────────────────────────────────────────────────────

        if text.lower() in ("/quit", "/exit", "/q"):
            print("\n  👋 Goodbye!\n")
            break

        if text.lower().startswith("/folder"):
            arg = text[7:].strip()
            if not arg:
                print(f"  ℹ  Folder: {folder or 'not set'}\n")
                continue
            p = os.path.abspath(os.path.expanduser(arg))
            if not os.path.isdir(p):
                print(f"  ⚠  Not a directory: {p}\n")
            else:
                folder = p
                files = get_files(folder)
                print(f"  ✅ Folder: {folder}  ({len(files)} files)\n")
            continue

        # Bare directory path → change folder
        if os.path.isdir(text):
            folder = os.path.abspath(os.path.expanduser(text))
            files = get_files(folder)
            print(f"  ✅ Folder: {folder}  ({len(files)} files)\n")
            continue

        if text.startswith("/"):
            print("  ⚠  Unknown command. Try a pattern like  image-NN  or  file-RND\n")
            continue

        # ── Pattern ───────────────────────────────────────────────────────────

        if not folder:
            print("  ⚠  Set a folder first:  /folder <path>\n")
            continue

        warn = validate_pattern(text)
        if warn:
            print(f"  ⚠  {warn}")
            try:
                ok = input("  Continue anyway? [y/N]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                continue
            if ok != "y":
                print()
                continue

        plan = build_plan(folder, files, text)
        if not plan:
            print("  📭 No files found.\n")
            continue

        show_preview(plan, folder)

        try:
            confirm = input(f"  {len(plan)} files  →  apply? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.\n")
            continue

        if confirm == "y":
            apply_plan(plan, folder)
            files = get_files(folder)
        else:
            print("  Cancelled.\n")


if __name__ == "__main__":
    main()
