#!/usr/bin/env python3
"""
file_rename.py — Batch file renamer (sequential or random)

Usage:
    python3 file_rename.py                              # Interactive mode
    python3 file_rename.py ./input                      # Pre-set folder, interactive
    python3 file_rename.py ./input --seq                # Quick sequential rename
    python3 file_rename.py ./input --rand               # Quick random rename
    python3 file_rename.py ./input --seq --preview      # Preview without renaming
    python3 file_rename.py ./input --seq --prefix img_  # Sequential with prefix
"""

__version__ = "2.0.0"

import argparse
import os
import random
import shutil
import string
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CHARSETS = {
    "alphanum": string.ascii_letters + string.digits,
    "hex":      string.hexdigits[:16],   # 0-9 a-f
    "alpha":    string.ascii_letters,
    "digits":   string.digits,
}

CHARSET_LABELS = {
    "alphanum": "a-z A-Z 0-9",
    "hex":      "0-9 a-f",
    "alpha":    "a-z A-Z",
    "digits":   "0-9",
    "custom":   "(user-defined)",
}


# ── Utilities ────────────────────────────────────────────────────────────────

def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))


def get_files(folder, filter_ext=None):
    files = sorted(
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and not f.startswith(".")
    )
    if filter_ext:
        ext = filter_ext.lower()
        files = [f for f in files if os.path.splitext(f)[1].lower() == ext]
    return files


def term_width():
    return shutil.get_terminal_size((80, 20)).columns


def draw_progress(current, total, bar_width=32):
    w = min(bar_width, term_width() - 28)
    pct = current / total if total > 0 else 0
    filled = int(w * pct)
    bar = "█" * filled + "░" * (w - filled)
    line = f"\r   ┃{bar}┃ {current}/{total}"
    sys.stdout.write(line)
    sys.stdout.flush()


# ── Plan builder ─────────────────────────────────────────────────────────────

def build_plan(folder, cfg):
    files = get_files(folder, cfg["filter_ext"])
    if not files:
        return []

    plan = []

    if cfg["mode"] == "sequential":
        num = cfg["seq_start"]
        for fname in files:
            _, orig_ext = os.path.splitext(fname)
            stem = f"{cfg['seq_prefix']}{str(num).zfill(cfg['seq_padding'])}{cfg['seq_suffix']}"
            ext = orig_ext if cfg["preserve_ext"] else ""
            plan.append((fname, stem + ext))
            num += cfg["seq_step"]

    else:  # random
        charset = CHARSETS.get(cfg["rand_charset"]) or cfg["rand_custom_chars"]
        if not charset:
            print("  ⚠  Custom charset is empty — set it with /chars <characters>")
            return []
        used: set[str] = set()
        for fname in files:
            _, orig_ext = os.path.splitext(fname)
            for _ in range(100_000):
                stem = "".join(random.choices(charset, k=cfg["rand_length"]))
                if stem not in used:
                    used.add(stem)
                    break
            else:
                print("  ⚠  Could not generate enough unique names — try a longer /length")
                return []
            ext = orig_ext if cfg["preserve_ext"] else ""
            plan.append((fname, stem + ext))

    return plan


# ── Display ──────────────────────────────────────────────────────────────────

def print_header():
    print("\n╔══════════════════════════════════════════════╗")
    print("║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║")
    print("╚══════════════════════════════════════════════╝")


def print_status(cfg):
    folder = cfg["folder"] or "not set"
    filt   = cfg["filter_ext"] or "all files"
    ext_m  = "keep" if cfg["preserve_ext"] else "strip"

    print(f"\n  Folder:  {folder}")
    print(f"  Mode:    {cfg['mode']}")
    print(f"  Filter:  {filt}  (extension: {ext_m})")

    if cfg["mode"] == "sequential":
        num_str = str(cfg["seq_start"]).zfill(cfg["seq_padding"])
        example = f"{cfg['seq_prefix']}{num_str}{cfg['seq_suffix']}.ext"
        print(f"  Options: prefix={cfg['seq_prefix']!r}  suffix={cfg['seq_suffix']!r}  "
              f"start={cfg['seq_start']}  step={cfg['seq_step']}  pad={cfg['seq_padding']}")
        print(f"  Example: {example}")
    else:
        cs = cfg["rand_charset"]
        chars = cfg["rand_custom_chars"] if cs == "custom" else CHARSETS.get(cs, "")
        label = CHARSET_LABELS.get(cs, cs)
        print(f"  Options: length={cfg['rand_length']}  charset={cs}  ({label},  {len(chars)} chars)")

    if cfg["folder"] and os.path.isdir(cfg["folder"]):
        files = get_files(cfg["folder"], cfg["filter_ext"])
        print(f"\n  📁 {len(files)} file(s) ready to rename")

    print()


def print_help():
    print("\n  Commands:")
    print("    /folder <path>        — set working folder")
    print("    /seq                  — switch to sequential mode")
    print("    /rand                 — switch to random mode")
    print("    /prefix [text]        — set name prefix       (seq, e.g. /prefix photo_)")
    print("    /suffix [text]        — set name suffix       (seq, e.g. /suffix _edit)")
    print("    /start <n>            — set start number      (seq, default 1)")
    print("    /step <n>             — set increment step    (seq, default 1)")
    print("    /pad <n>              — set zero-pad width    (seq, default 4 → 0001)")
    print("    /length <n>           — set name length       (rand, default 8)")
    print("    /charset <name>       — alphanum|hex|alpha|digits|custom  (rand)")
    print("    /chars <characters>   — set custom charset characters")
    print("    /filter [.ext]        — limit to extension    (blank = all files)")
    print("    /ext keep|strip       — preserve or drop original file extension")
    print("    /preview              — preview changes without applying")
    print("    /go                   — apply renames (asks for confirmation)")
    print("    /status               — show current settings")
    print("    /help                 — show this help")
    print("    /quit                 — exit\n")


def print_preview(plan, folder):
    if not plan:
        print("\n  📭 No files to rename.\n")
        return

    tw = term_width()
    col = min(40, (tw - 10) // 2)

    conflicts = 0
    print(f"\n  {'Original':<{col}}    New name")
    print(f"  {'─' * col}    {'─' * col}")
    for old, new in plan:
        new_path = os.path.join(folder, new)
        old_path = os.path.join(folder, old)
        conflict = ""
        if os.path.exists(new_path) and new_path != old_path:
            conflict = "  ⚠ conflict"
            conflicts += 1
        old_trunc = old[:col - 1] + "…" if len(old) > col else old
        print(f"  {old_trunc:<{col}}  →  {new}{conflict}")

    print(f"\n  {len(plan)} file(s) will be renamed", end="")
    if conflicts:
        print(f",  {conflicts} conflict(s) will be skipped", end="")
    print("\n")


# ── Apply renames ────────────────────────────────────────────────────────────

def apply_renames(plan, folder):
    total   = len(plan)
    ok      = 0
    skipped = 0

    print()
    for i, (old, new) in enumerate(plan, 1):
        draw_progress(i, total)
        old_path = os.path.join(folder, old)
        new_path = os.path.join(folder, new)
        if os.path.exists(new_path) and new_path != old_path:
            skipped += 1
            continue
        try:
            os.rename(old_path, new_path)
            ok += 1
        except Exception as e:
            print(f"\n  ⚠  {old}: {e}")

    draw_progress(total, total)
    print()
    print(f"\n  ✅ Done!  {ok} renamed", end="")
    if skipped:
        print(f",  {skipped} skipped (conflicts)", end="")
    print("\n")


# ── Interactive mode ─────────────────────────────────────────────────────────

def interactive_mode(cfg):
    print_header()
    print_status(cfg)
    print_help()

    while True:
        try:
            text = input("  ▶ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  👋 Goodbye!\n")
            break

        if not text:
            continue

        # Allow bare folder paths without a /command prefix
        if not text.startswith("/"):
            if os.path.isdir(text):
                cfg["folder"] = resolve_path(text)
                files = get_files(cfg["folder"], cfg["filter_ext"])
                print(f"  ✅ Folder: {cfg['folder']}")
                print(f"  📁 {len(files)} file(s) found")
            else:
                print("  ⚠  Commands start with /  — type /help to see options.")
            continue

        parts = text.split(maxsplit=1)
        cmd   = parts[0].lower()
        arg   = parts[1].strip() if len(parts) > 1 else ""

        # ── Navigation ──────────────────────────────────────────────────────

        if cmd in ("/quit", "/exit", "/q"):
            print("\n  👋 Goodbye!\n")
            break

        elif cmd == "/help":
            print_help()

        elif cmd == "/status":
            print_status(cfg)

        # ── Folder ──────────────────────────────────────────────────────────

        elif cmd == "/folder":
            if not arg:
                print(f"  ℹ  Folder: {cfg['folder'] or 'not set'}")
            else:
                p = resolve_path(arg)
                if not os.path.isdir(p):
                    print(f"  ⚠  Not a directory: {p}")
                else:
                    cfg["folder"] = p
                    files = get_files(p, cfg["filter_ext"])
                    print(f"  ✅ Folder: {p}")
                    print(f"  📁 {len(files)} file(s) found")

        # ── Mode ────────────────────────────────────────────────────────────

        elif cmd == "/seq":
            cfg["mode"] = "sequential"
            print("  ✅ Mode: sequential")

        elif cmd == "/rand":
            cfg["mode"] = "random"
            print("  ✅ Mode: random")

        # ── Sequential options ───────────────────────────────────────────────

        elif cmd == "/prefix":
            cfg["seq_prefix"] = arg
            print(f"  ✅ Prefix: {arg!r}")

        elif cmd == "/suffix":
            cfg["seq_suffix"] = arg
            print(f"  ✅ Suffix: {arg!r}")

        elif cmd == "/start":
            try:
                cfg["seq_start"] = int(arg)
                print(f"  ✅ Start: {cfg['seq_start']}")
            except ValueError:
                print("  ⚠  Expected an integer, e.g. /start 100")

        elif cmd == "/step":
            try:
                v = int(arg)
                if v < 1:
                    raise ValueError
                cfg["seq_step"] = v
                print(f"  ✅ Step: {v}")
            except ValueError:
                print("  ⚠  Expected a positive integer, e.g. /step 2")

        elif cmd == "/pad":
            try:
                v = int(arg)
                if v < 1:
                    raise ValueError
                cfg["seq_padding"] = v
                print(f"  ✅ Pad width: {v}  →  {str(cfg['seq_start']).zfill(v)}")
            except ValueError:
                print("  ⚠  Expected a positive integer, e.g. /pad 4")

        # ── Random options ───────────────────────────────────────────────────

        elif cmd == "/length":
            try:
                v = int(arg)
                if v < 1:
                    raise ValueError
                cfg["rand_length"] = v
                print(f"  ✅ Length: {v}")
            except ValueError:
                print("  ⚠  Expected a positive integer, e.g. /length 12")

        elif cmd == "/charset":
            valid = ("alphanum", "hex", "alpha", "digits", "custom")
            if arg in valid:
                cfg["rand_charset"] = arg
                label = CHARSET_LABELS.get(arg, "")
                print(f"  ✅ Charset: {arg}  ({label})")
            elif arg:
                print(f"  ⚠  Unknown charset. Options: {', '.join(valid)}")
            else:
                print(f"  ℹ  Charset: {cfg['rand_charset']}  ({CHARSET_LABELS.get(cfg['rand_charset'], '')})")

        elif cmd == "/chars":
            if not arg:
                print(f"  ℹ  Custom chars: {cfg['rand_custom_chars']!r}  ({len(cfg['rand_custom_chars'])} chars)")
            else:
                cfg["rand_custom_chars"] = arg
                cfg["rand_charset"] = "custom"
                print(f"  ✅ Custom charset: {arg!r}  ({len(arg)} chars)")

        # ── Filter / extension ───────────────────────────────────────────────

        elif cmd == "/filter":
            if not arg:
                cfg["filter_ext"] = None
                print("  ✅ Filter: all files")
            else:
                ext = arg if arg.startswith(".") else f".{arg}"
                cfg["filter_ext"] = ext.lower()
                print(f"  ✅ Filter: {ext}")
                if cfg["folder"] and os.path.isdir(cfg["folder"]):
                    files = get_files(cfg["folder"], cfg["filter_ext"])
                    print(f"  📁 {len(files)} matching file(s)")

        elif cmd == "/ext":
            if arg == "keep":
                cfg["preserve_ext"] = True
                print("  ✅ Extension: keep original")
            elif arg == "strip":
                cfg["preserve_ext"] = False
                print("  ✅ Extension: strip")
            else:
                print("  ⚠  Use /ext keep  or  /ext strip")

        # ── Preview / go ─────────────────────────────────────────────────────

        elif cmd == "/preview":
            if not cfg["folder"]:
                print("  ⚠  Set a folder first: /folder <path>")
            else:
                plan = build_plan(cfg["folder"], cfg)
                print_preview(plan, cfg["folder"])

        elif cmd == "/go":
            if not cfg["folder"]:
                print("  ⚠  Set a folder first: /folder <path>")
                continue
            plan = build_plan(cfg["folder"], cfg)
            if not plan:
                print("  📭 No files to rename.")
                continue
            print_preview(plan, cfg["folder"])
            try:
                confirm = input("  Apply these renames? [y/N]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n  Cancelled.")
                continue
            if confirm == "y":
                apply_renames(plan, cfg["folder"])
            else:
                print("  Cancelled.\n")

        else:
            print(f"  ⚠  Unknown command: {cmd}. Type /help for commands.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Batch file renamer — sequential or random",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                   Interactive mode
  %(prog)s ./input                           Pre-set folder, interactive
  %(prog)s ./input --seq --prefix img_ --pad 4   Quick sequential rename
  %(prog)s ./input --rand --length 12        Quick random rename
  %(prog)s ./input --seq --preview           Preview without renaming
  %(prog)s ./input --seq --filter .jpg       Sequential, JPEGs only
        """
    )
    parser.add_argument("folder",       nargs="?",          help="Folder to rename files in")
    parser.add_argument("--seq",        action="store_true", help="Sequential mode")
    parser.add_argument("--rand",       action="store_true", help="Random mode")
    parser.add_argument("--prefix",     default="",          help="Name prefix (sequential)")
    parser.add_argument("--suffix",     default="",          help="Name suffix (sequential)")
    parser.add_argument("--start",      type=int, default=1, help="Start number (sequential, default 1)")
    parser.add_argument("--step",       type=int, default=1, help="Step size (sequential, default 1)")
    parser.add_argument("--pad",        type=int, default=4, help="Zero-pad width (sequential, default 4)")
    parser.add_argument("--length",     type=int, default=8, help="Name length (random, default 8)")
    parser.add_argument("--charset",    default="alphanum",
                        choices=["alphanum", "hex", "alpha", "digits", "custom"],
                        help="Charset (random, default alphanum)")
    parser.add_argument("--chars",      default="",          help="Custom charset characters")
    parser.add_argument("--filter",     default=None,        help="Extension filter, e.g. .jpg")
    parser.add_argument("--strip-ext",  action="store_true", help="Strip original extension from new names")
    parser.add_argument("--preview",    action="store_true", help="Preview changes only, do not rename")
    parser.add_argument("--version",    action="version",    version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    cfg = {
        "folder":           None,
        "mode":             "random" if args.rand else "sequential",
        "filter_ext":       args.filter,
        "preserve_ext":     not args.strip_ext,
        "seq_prefix":       args.prefix,
        "seq_suffix":       args.suffix,
        "seq_start":        args.start,
        "seq_step":         args.step,
        "seq_padding":      args.pad,
        "rand_length":      args.length,
        "rand_charset":     args.charset,
        "rand_custom_chars": args.chars,
    }

    if args.folder:
        p = resolve_path(args.folder)
        if not os.path.isdir(p):
            print(f"⚠  Not a directory: {p}")
            sys.exit(1)
        cfg["folder"] = p

    # Non-interactive: folder + explicit mode flag given
    if cfg["folder"] and (args.seq or args.rand):
        plan = build_plan(cfg["folder"], cfg)
        print_preview(plan, cfg["folder"])
        if args.preview or not plan:
            return
        try:
            confirm = input("  Apply these renames? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Cancelled.")
            sys.exit(0)
        if confirm == "y":
            apply_renames(plan, cfg["folder"])
        return

    interactive_mode(cfg)


if __name__ == "__main__":
    main()
