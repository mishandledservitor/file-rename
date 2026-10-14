# file-rename

## What this repo is

A command-line batch file renamer. The user types a pattern at an interactive prompt: `NN` (two or more `N`s) becomes a zero-padded sequential number and `RND` becomes 8 random lowercase letters and digits. The tool previews every rename, asks for confirmation and then moves the files from `input/` to `output/` (or renames them in place with `/inplace`), skipping any file whose new name already exists. It is one Python 3 standard-library script plus a bash launcher. The project's decisions live in `docs/decisions.md`; what changes for users lives in `CHANGELOG.md`.

## Conventions

- `file_rename.py` uses only the Python standard library, and the tests use only `unittest`. Adding a dependency is a decision for the owner, recorded in `docs/decisions.md`.
- The version is `__version__` in `file_rename.py`, following Semantic Versioning, and every release has a dated entry in `CHANGELOG.md` (Keep a Changelog 1.1.0). User-visible changes go under `## [Unreleased]` until a release.
- Tests work only in temporary folders they create. No real personal files, photos or file names go into the repository.
- Text a user reads (prompt output, README, changelog) uses UK spelling, full sentences and no em dashes.

## Standing rules

Binding on any agent working in this repo. These are process rules, not project conventions. **This file is the only source of truth for them.** Delete one only deliberately, never because it looks like unused scaffolding.

1. **No agent memory.** Never rely on assistant-side memory, per-project memory files, or recall from a previous session. Everything durable lives in the repo: this file, `CHANGELOG.md` and `docs/decisions.md`. If something is worth remembering, write it here in the same turn you learn it. If a memory and the repo disagree, the repo wins.
2. **True TDD: red, green, refactor.** No production code without a failing test first. For every unit of work, write a test in `tests/` that fails for the right reason (red), write the minimum code to make it pass (green), then clean up with the tests still green (refactor). This applies whatever way the work arrives, whether as an issue, a chat message or the user typing at a session directly. The only exception is a small, reversible change a user cannot see, such as a typo, a comment or a note.
3. **All development happens on a branch or worktree.** Never write code, tests or docs on a checkout of the main branch. Create a worktree or branch and work there. Only repository management belongs on main: merging pull requests, reviewing, tagging, releases, branch cleanup and reading.
4. **Commit every round.** Each round (one user request plus its completion) ends with a git commit of whatever that round changed, without waiting to be asked. Stage specific paths, never `-A`; review what is staged first; make new commits only (no `--amend` unless asked); never force-push. A pure question-and-answer round that changes no files has nothing to commit.
5. **Refresh `Current status` before each commit.** Update the "Current status" section below, including its `Last updated:` date, to match reality as part of the same commit, so the summary never drifts from the repo.
6. **Don't narrate no-ops.** A check that came back empty does not need a line of output. Report what you did and what the user has to decide.
7. **Never hard-wrap text meant for a human to read.** No fixed-column line breaks in README or docs prose, changelog entries, chat messages or commit-message bodies: one paragraph is one line, and the device does the wrapping. This does not touch code: source lines, code blocks, ASCII tables and fixed-width terminal output stay as they are.
8. **Never touch a `.env` file without asking the user.** Not to untrack it, delete it, move it or rewrite it. Report what you found, say what reads the file, and ask. Reading one to classify a key is allowed, changing one is not, and no value ever appears in a report, a commit message or a prompt. This tool reads no `.env` file today, and `.gitignore` keeps one out of the repository.

## Commands

Python 3.10 or later; no install step.

```sh
./file-rename                  # interactive renamer, ./input -> ./output
./file-rename <folder>         # use another input folder
python3 file_rename.py --version
python3 -m unittest -v         # all tests (tests/test_file_rename.py)
bash -n file-rename            # syntax check of the launcher (CI runs it)
python3 -m py_compile file_rename.py
```

## Structure

- `file_rename.py`: the whole tool. `get_files`, `make_stem`, `build_plan`, `validate_pattern` and `apply_plan` hold the logic; `show_preview` and `print_header` print; `main` runs the prompt loop.
- `file-rename`: bash launcher that runs `file_rename.py` with `python3` from the script's own folder.
- `tests/`: `unittest` suite for the pattern, plan and file-moving logic.
- `input/`, `output/`: default working folders next to the script, ignored by git.
- `docs/decisions.md`: numbered decisions with who and when.

## CI/CD

- `.github/workflows/ci.yml` (`CI`): on every pull request and push to main, on ubuntu-latest with Python 3.10 and 3.13, it checks the launcher's syntax, compiles the script and runs the tests. It uses no secrets. There is no release automation.

## Current status

Last updated: 2026-10-14
- Version 4.0.0, unchanged since 2026-04-03. Prepared for a fresh public repository (decision 1).
- 18 tests cover pattern substitution, validation, plan building (including unique random names), file listing and moving, in-place renaming and conflict skipping. The interactive loop in `main` is not covered by tests.
- Open: nothing planned.
