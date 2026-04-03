# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026-04-03

### Changed
- Full rewrite as a voxbox-style CLI — `/command` input loop, emoji, Unicode box-drawing
- Dropped `rich` dependency — zero external dependencies, pure Python stdlib only
- Replaced menu-driven UI with a persistent interactive prompt (`▶`)

### Added
- `file-rename` bash launcher script (no `python3` prefix needed)
- Non-interactive CLI flags: `--seq`, `--rand`, `--prefix`, `--suffix`, `--start`, `--step`, `--pad`, `--length`, `--charset`, `--chars`, `--filter`, `--strip-ext`, `--preview`
- `/status` command shows live config and file count
- `/filter` command with live count feedback
- Terminal-width-aware preview table
- Progress bar during rename using `█░` block characters
- `--version` flag

### Removed
- `rich` dependency

---

## [1.0.0] — 2026-04-03

### Added
- Interactive CLI menu powered by `rich`
- Sequential rename mode with configurable prefix, suffix, start number, step, and zero-padding
- Random rename mode with configurable name length and charset (alphanumeric, hex, letters, digits, custom)
- Extension filter to limit renaming to a specific file type
- Option to preserve or strip the original file extension
- Preview screen showing the full old → new mapping before applying
- Conflict detection — files that would collide with an existing name are skipped
- Optional positional argument to pre-set the working folder on launch
