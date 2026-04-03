# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-04-03

### Added
- Interactive CLI menu powered by `rich`
- **Sequential** rename mode with configurable prefix, suffix, start number, step, and zero-padding
- **Random** rename mode with configurable name length and charset (alphanumeric, hex, letters, digits, custom)
- Extension filter to limit renaming to a specific file type
- Option to preserve or strip the original file extension
- Preview screen showing the full old → new mapping before applying
- Conflict detection — files that would collide with an existing name are skipped
- Optional positional argument to pre-set the working folder on launch (`python3 file_rename.py ./folder`)
