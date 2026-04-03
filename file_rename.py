#!/usr/bin/env python3
"""
file_rename.py — Batch file renamer

By default reads from ./input and writes renamed files to ./output.
Type a pattern to rename — NN for sequential, RND for random.

Usage:
    python3 file_rename.py          # uses ./input → ./output
    python3 file_rename.py [folder] # override input folder

Pattern syntax:
    NN / NNN / NNNN  →  sequential number  (N count = zero-pad width)
    RND              →  random 8-char alphanumeric string

Examples:
    image-NN         →  image-01.jpg, image-02.jpg …
    shot_NNNN        →  shot_0001.jpg, shot_0002.jpg …
    img-RND          →  img-a8f3k2xq.jpg …
"""

__version__ = "4.0.0"

import os
import random
import re
import shutil
import string
import sys

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DEFAULT_IN  = os.path.join(SCRIPT_DIR, "input")
DEFAULT_OUT = os.path.join(SCRIPT_DIR, "output")

RAND_CHARS  = string.ascii_lowercase + string.digits
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


def build_plan(files, pattern):
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
    has_seq = bool(re.search(r"N{2,}", pattern))
    has_rnd = "RND" in pattern
    if not has_seq and not has_rnd:
        return "pattern has no NN or RND — all files would get the same name"
    return None


# ── Display ───────────────────────────────────────────────────────────────────

def tw():
    return shutil.get_terminal_size((80, 20)).columns


def show_preview(plan, src_folder, dst_folder):
    col = min(48, (tw() - 8) // 2)
    rows = []
    conflicts = 0
    for old, new in plan:
        trunc = (old[: col - 1] + "…") if len(old) > col else old
        dst = os.path.join(dst_folder, new)
        src = os.path.join(src_folder, old)
        conflict = "  ⚠ conflict" if os.path.exists(dst) and dst != src else ""
        if conflict:
            conflicts += 1
        rows.append((trunc, new, conflict))

    print()
    display = (rows[:5] + [None] + rows[-1:]) if len(rows) > 12 else rows
    for row in display:
        if row is None:
            print(f"  {'…  ' + str(len(rows) - 6) + ' more  …':>{col}}  →")
        else:
            trunc, new, conflict = row
            print(f"  {trunc:<{col}}  →  {new}{conflict}")
    print()
    if conflicts:
        print(f"  ⚠  {conflicts} conflict(s) will be skipped\n")


def apply_plan(plan, src_folder, dst_folder):
    inplace = src_folder == dst_folder
    if not inplace:
        os.makedirs(dst_folder, exist_ok=True)

    ok = skipped = 0
    for old, new in plan:
        src = os.path.join(src_folder, old)
        dst = os.path.join(dst_folder, new)
        if os.path.exists(dst) and dst != src:
            skipped += 1
            continue
        try:
            shutil.move(src, dst)
            ok += 1
        except Exception as e:
            print(f"  ⚠  {old}: {e}")

    msg = f"  ✅ Done!  {ok} moved to {dst_folder}" if not inplace else f"  ✅ Done!  {ok} renamed"
    if skipped:
        msg += f",  {skipped} skipped"
    print(msg + "\n")


def print_header(src, dst, files, inplace):
    count = f"  ({len(files)} files)" if files is not None else "  (folder not found)"
    dest_label = "in place" if inplace else dst
    print("\n╔══════════════════════════════════════════════╗")
    print("║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║")
    print("╚══════════════════════════════════════════════╝")
    print(f"\n  Input:  {src}{count}")
    print(f"  Output: {dest_label}\n")
    print("  Type a pattern — NN = sequential,  RND = random:\n")
    print("    image-NN      →  image-01.jpg, image-02.jpg …")
    print("    shot_NNNN     →  shot_0001.jpg, shot_0002.jpg …")
    print("    file-RND      →  file-a8f3k2xq.jpg …\n")
    print("  /folder <path>   change input folder")
    print("  /output <path>   change output folder")
    print("  /inplace         toggle rename-in-place (skips output folder)")
    print("  /quit            exit\n")


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Batch file renamer — type a pattern like image-NN")
    ap.add_argument("folder",    nargs="?", help="Input folder (default: ./input)")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args()

    # Resolve input folder
    if args.folder:
        src = os.path.abspath(os.path.expanduser(args.folder))
        if not os.path.isdir(src):
            print(f"⚠  Not a directory: {src}")
            sys.exit(1)
    else:
        src = DEFAULT_IN

    dst     = DEFAULT_OUT
    inplace = False
    files   = get_files(src) if os.path.isdir(src) else None

    print_header(src, dst, files, inplace)

    while True:
        try:
            text = input("  ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋 Goodbye!\n")
            break

        if not text:
            continue

        low = text.lower()

        # ── Builtins ─────────────────────────────────────────────────────────

        if low in ("/quit", "/exit", "/q"):
            print("\n  👋 Goodbye!\n")
            break

        if low.startswith("/folder"):
            arg = text[7:].strip()
            if not arg:
                print(f"  ℹ  Input: {src}\n")
                continue
            p = os.path.abspath(os.path.expanduser(arg))
            if not os.path.isdir(p):
                print(f"  ⚠  Not a directory: {p}\n")
            else:
                src   = p
                files = get_files(src)
                print(f"  ✅ Input: {src}  ({len(files)} files)\n")
            continue

        if low.startswith("/output"):
            arg = text[7:].strip()
            if not arg:
                print(f"  ℹ  Output: {'in place' if inplace else dst}\n")
                continue
            dst     = os.path.abspath(os.path.expanduser(arg))
            inplace = False
            print(f"  ✅ Output: {dst}\n")
            continue

        if low == "/inplace":
            inplace = not inplace
            if inplace:
                print("  ✅ Mode: rename in place (files stay in input folder)\n")
            else:
                print(f"  ✅ Mode: move to output  ({dst})\n")
            continue

        # Bare directory path → change input folder
        if os.path.isdir(text):
            src   = os.path.abspath(os.path.expanduser(text))
            files = get_files(src)
            print(f"  ✅ Input: {src}  ({len(files)} files)\n")
            continue

        if text.startswith("/"):
            print("  ⚠  Unknown command. Try a pattern like  image-NN  or  file-RND\n")
            continue

        # ── Pattern ───────────────────────────────────────────────────────────

        if not os.path.isdir(src):
            print(f"  ⚠  Input folder not found: {src}\n")
            print(f"     Create it or set another:  /folder <path>\n")
            continue

        if files is None:
            files = get_files(src)

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

        plan = build_plan(files, text)
        if not plan:
            print("  📭 No files in input folder.\n")
            continue

        effective_dst = src if inplace else dst
        show_preview(plan, src, effective_dst)

        try:
            confirm = input(f"  {len(plan)} files  →  apply? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.\n")
            continue

        if confirm == "y":
            apply_plan(plan, src, effective_dst)
            files = get_files(src) if os.path.isdir(src) else []
        else:
            print("  Cancelled.\n")


if __name__ == "__main__":
    main()
