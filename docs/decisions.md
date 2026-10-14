# Decisions

| # | Decision | Who, when |
|---|---|---|
| 1 | The project is published as a fresh public repository whose history starts with a single commit, and the earlier repository is archived. | Owner, 2026-10-14 |
| 2 | `CLAUDE.md` is self-contained. It no longer carries a block synced from the owner's private template repository, and every rule in it describes how this repository actually works. | Owner, 2026-10-14 |
| 3 | The project has a small test suite written with the standard library's `unittest`, run in CI, and changes are made test-first from now on. Spec Kit is not used here. | Owner, 2026-10-14 |
| 4 | The version stays at 4.0.0, and the existing release history is kept in `CHANGELOG.md` in Keep a Changelog form. | Owner, 2026-10-14 |
