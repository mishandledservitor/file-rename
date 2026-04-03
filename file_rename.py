#!/usr/bin/env python3
"""
file_rename.py — Rename files in a folder sequentially or randomly.

Usage:
    python file_rename.py [folder]
    pip install rich  (only dependency)
"""

__version__ = "1.0.0"

import os
import random
import string
import sys
from pathlib import Path

try:
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm, IntPrompt, Prompt
    from rich.table import Table
except ImportError:
    print("Missing dependency — install with:  pip install rich")
    sys.exit(1)

console = Console()

# ─── Defaults ─────────────────────────────────────────────────────────────────

DEFAULT_CONFIG: dict = {
    "folder": None,
    "mode": "sequential",       # "sequential" | "random"
    "filter_ext": None,         # None = all files, else e.g. ".jpg"
    "preserve_ext": True,
    # Sequential
    "seq_prefix": "",
    "seq_suffix": "",
    "seq_start": 1,
    "seq_step": 1,
    "seq_padding": 4,
    # Random
    "rand_length": 8,
    "rand_charset": "alphanum",  # alphanum | hex | alpha | digits | custom
    "rand_custom_chars": "",
}

CHARSETS = {
    "alphanum": string.ascii_letters + string.digits,
    "hex":      string.hexdigits[:16],  # 0-9 a-f
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

# ─── Helpers ──────────────────────────────────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg: str = "  Press Enter to continue"):
    Prompt.ask(msg, default="")


def header():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]File Renamer[/bold cyan]  [dim]— sequential or random[/dim]",
        border_style="cyan",
    ))
    console.print()


def show_config(cfg: dict):
    t = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    t.add_column(style="dim", no_wrap=True)
    t.add_column()

    folder_display = str(cfg["folder"]) if cfg["folder"] else "[red]not set[/red]"
    t.add_row("Folder", folder_display)
    t.add_row("Mode", f"[yellow]{cfg['mode']}[/yellow]")
    t.add_row(
        "Filter ext",
        cfg["filter_ext"] if cfg["filter_ext"] else "[dim]all files[/dim]",
    )
    t.add_row("Preserve ext", "[green]yes[/green]" if cfg["preserve_ext"] else "[red]no[/red]")

    if cfg["mode"] == "sequential":
        prefix = cfg["seq_prefix"] or "[dim](none)[/dim]"
        suffix = cfg["seq_suffix"] or "[dim](none)[/dim]"
        num_str = str(cfg["seq_start"]).zfill(cfg["seq_padding"])
        example = f"{cfg['seq_prefix']}{num_str}{cfg['seq_suffix']}.ext"
        t.add_row("Prefix", prefix)
        t.add_row("Suffix", suffix)
        t.add_row("Start / Step", f"{cfg['seq_start']} / {cfg['seq_step']}")
        t.add_row("Zero-pad width", str(cfg["seq_padding"]))
        t.add_row("Example", f"[green]{example}[/green]")
    else:
        charset = cfg["rand_charset"]
        if charset == "custom":
            chars_label = cfg["rand_custom_chars"] or "[red]not set[/red]"
        else:
            chars_label = CHARSET_LABELS[charset]
        t.add_row("Name length", str(cfg["rand_length"]))
        t.add_row("Charset", f"{charset}  [dim]({chars_label})[/dim]")

    console.print(Panel(t, title="[bold]Configuration[/bold]", border_style="blue"))


# ─── Sub-menus ────────────────────────────────────────────────────────────────

def menu_set_folder(cfg: dict):
    console.print("[bold]Enter folder path[/bold] (Enter = current directory):")
    raw = Prompt.ask("  Path", default=str(Path.cwd()))
    p = Path(raw).expanduser().resolve()
    if not p.is_dir():
        console.print(f"[red]Not a directory:[/red] {p}")
        pause()
        return
    cfg["folder"] = p
    console.print(f"[green]Folder set:[/green] {p}")
    pause()


def menu_choose_mode(cfg: dict):
    console.print("\n[bold]Rename mode[/bold]")
    console.print("  [cyan]1[/cyan]  Sequential  — file_0001.jpg, file_0002.jpg …")
    console.print("  [cyan]2[/cyan]  Random      — a3Fx9Kqz.jpg, bT7mWnPs.jpg …")
    choice = Prompt.ask("  Select", choices=["1", "2"], default="1")
    cfg["mode"] = "sequential" if choice == "1" else "random"
    console.print(f"[green]Mode:[/green] {cfg['mode']}")
    pause()


def menu_configure_sequential(cfg: dict):
    console.print("\n[bold]Sequential options[/bold]")
    cfg["seq_prefix"]  = Prompt.ask("  Prefix",         default=cfg["seq_prefix"])
    cfg["seq_suffix"]  = Prompt.ask("  Suffix",         default=cfg["seq_suffix"])
    cfg["seq_start"]   = IntPrompt.ask("  Start number", default=cfg["seq_start"])
    cfg["seq_step"]    = IntPrompt.ask("  Step",         default=cfg["seq_step"])
    cfg["seq_padding"] = IntPrompt.ask("  Zero-pad width (4 → 0001)", default=cfg["seq_padding"])
    pause()


def menu_configure_random(cfg: dict):
    console.print("\n[bold]Random options[/bold]")
    cfg["rand_length"] = IntPrompt.ask("  Name length (characters)", default=cfg["rand_length"])
    console.print("  Charset:")
    console.print("    [cyan]1[/cyan]  Alphanumeric  (a-z A-Z 0-9)")
    console.print("    [cyan]2[/cyan]  Hex           (0-9 a-f)")
    console.print("    [cyan]3[/cyan]  Letters only  (a-z A-Z)")
    console.print("    [cyan]4[/cyan]  Digits only   (0-9)")
    console.print("    [cyan]5[/cyan]  Custom")
    c = Prompt.ask("  Select", choices=["1", "2", "3", "4", "5"], default="1")
    cfg["rand_charset"] = {"1": "alphanum", "2": "hex", "3": "alpha", "4": "digits", "5": "custom"}[c]
    if cfg["rand_charset"] == "custom":
        cfg["rand_custom_chars"] = Prompt.ask("  Enter your custom character set")
    pause()


def menu_configure_filter(cfg: dict):
    console.print("\n[bold]Extension filter[/bold]")
    console.print("  Leave blank to rename [italic]all[/italic] files.")
    console.print("  Or enter an extension to limit scope, e.g. [dim].jpg[/dim]  [dim].txt[/dim]")
    raw = Prompt.ask("  Extension", default=cfg["filter_ext"] or "").strip()
    if raw and not raw.startswith("."):
        raw = f".{raw}"
    cfg["filter_ext"] = raw or None
    cfg["preserve_ext"] = Confirm.ask("  Preserve the file's original extension?", default=True)
    pause()


# ─── Plan builder ─────────────────────────────────────────────────────────────

def build_plan(cfg: dict) -> list[tuple[Path, Path]]:
    folder: Path = cfg["folder"]
    files = sorted(f for f in folder.iterdir() if f.is_file())

    if cfg["filter_ext"]:
        ext = cfg["filter_ext"].lower()
        files = [f for f in files if f.suffix.lower() == ext]

    if not files:
        return []

    plan: list[tuple[Path, Path]] = []

    if cfg["mode"] == "sequential":
        num = cfg["seq_start"]
        for f in files:
            stem = f"{cfg['seq_prefix']}{str(num).zfill(cfg['seq_padding'])}{cfg['seq_suffix']}"
            ext  = f.suffix if cfg["preserve_ext"] else ""
            plan.append((f, folder / (stem + ext)))
            num += cfg["seq_step"]

    else:  # random
        charset = CHARSETS.get(cfg["rand_charset"]) or cfg["rand_custom_chars"]
        if not charset:
            console.print("[red]Custom charset is empty — configure it first.[/red]")
            return []
        used: set[str] = set()
        for f in files:
            for _ in range(10_000):
                stem = "".join(random.choices(charset, k=cfg["rand_length"]))
                if stem not in used:
                    used.add(stem)
                    break
            else:
                console.print("[red]Could not generate enough unique names. Try a longer length or larger charset.[/red]")
                return []
            ext = f.suffix if cfg["preserve_ext"] else ""
            plan.append((f, folder / (stem + ext)))

    return plan


def preview_plan(plan: list[tuple[Path, Path]]):
    if not plan:
        console.print("[yellow]No files match — nothing to rename.[/yellow]")
        return

    t = Table(box=box.SIMPLE_HEAD)
    t.add_column("Original",  style="dim",   no_wrap=True)
    t.add_column("",          justify="center", style="cyan")
    t.add_column("New name",  style="green", no_wrap=True)
    t.add_column("",          style="red")

    for old, new in plan:
        conflict = "conflict!" if new.exists() and new != old else ""
        t.add_row(old.name, "→", new.name, conflict)

    console.print(Panel(
        t,
        title=f"[bold]Preview — {len(plan)} file(s)[/bold]",
        border_style="green",
    ))


def apply_plan(plan: list[tuple[Path, Path]]) -> int:
    ok = 0
    for old, new in plan:
        try:
            old.rename(new)
            ok += 1
        except Exception as exc:
            console.print(f"[red]  Error:[/red] {old.name} → {exc}")
    return ok


# ─── Main menu ────────────────────────────────────────────────────────────────

def main_menu(cfg: dict):
    while True:
        clear_screen()
        header()
        show_config(cfg)

        console.print("[bold]Main Menu[/bold]")
        console.print("  [cyan]1[/cyan]  Set folder")
        console.print("  [cyan]2[/cyan]  Choose mode          (sequential / random)")
        console.print("  [cyan]3[/cyan]  Configure mode options")
        console.print("  [cyan]4[/cyan]  Extension filter")
        console.print("  [cyan]5[/cyan]  Preview changes")
        console.print("  [cyan]6[/cyan]  [bold green]Apply renames[/bold green]")
        console.print("  [cyan]q[/cyan]  Quit")
        console.print()

        choice = Prompt.ask("  Select", choices=["1", "2", "3", "4", "5", "6", "q"])

        if choice == "1":
            menu_set_folder(cfg)

        elif choice == "2":
            menu_choose_mode(cfg)

        elif choice == "3":
            if cfg["mode"] == "sequential":
                menu_configure_sequential(cfg)
            else:
                menu_configure_random(cfg)

        elif choice == "4":
            menu_configure_filter(cfg)

        elif choice == "5":
            if not cfg["folder"]:
                console.print("[red]Set a folder first.[/red]")
                pause()
                continue
            plan = build_plan(cfg)
            preview_plan(plan)
            pause()

        elif choice == "6":
            if not cfg["folder"]:
                console.print("[red]Set a folder first.[/red]")
                pause()
                continue
            plan = build_plan(cfg)
            if not plan:
                pause()
                continue
            preview_plan(plan)
            conflicts = [(o, n) for o, n in plan if n.exists() and n != o]
            if conflicts:
                console.print(f"[red]⚠  {len(conflicts)} conflict(s) detected — those files will not be renamed.[/red]")
                plan = [(o, n) for o, n in plan if not (n.exists() and n != o)]
            if not plan:
                console.print("[yellow]Nothing left to rename after removing conflicts.[/yellow]")
                pause()
                continue
            if Confirm.ask(f"  Rename [bold]{len(plan)}[/bold] file(s)?", default=False):
                count = apply_plan(plan)
                console.print(f"[bold green]Done — {count} file(s) renamed.[/bold green]")
            else:
                console.print("[dim]Cancelled.[/dim]")
            pause()

        elif choice == "q":
            console.print("[dim]Goodbye.[/dim]")
            break


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(
        description="Rename files in a folder sequentially or randomly.",
        epilog="All options can also be set interactively via the menu.",
    )
    ap.add_argument("folder", nargs="?", help="Folder to operate on (optional)")
    args = ap.parse_args()

    cfg = dict(DEFAULT_CONFIG)

    if args.folder:
        p = Path(args.folder).expanduser().resolve()
        if not p.is_dir():
            console.print(f"[red]Not a directory:[/red] {p}")
            sys.exit(1)
        cfg["folder"] = p

    main_menu(cfg)
