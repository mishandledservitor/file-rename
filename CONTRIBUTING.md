# Contributing to file-rename

Bug reports, fixes and new features are all welcome.

## Before you start

- For a security problem, do not open a public issue. Report it privately from the repository's **Security** tab with **Report a vulnerability**.
- For a bug, open an issue that says what you typed, what you expected and what happened instead. Include your operating system and Python version, and the file names involved if they matter. Never paste names of private files you would not want to publish.
- For a new feature or a change in behaviour, open an issue first and describe the problem it solves. Agreeing on the idea before you write code saves you from building something that won't be merged.
- For a typo or a small fix, go straight to a pull request.

## Setting up

You need Python 3.10 or later and nothing else.

```sh
git clone https://github.com/<your-account>/file-rename.git
cd file-rename
python3 -m unittest -v
```

To try a change by hand, put some throwaway files in `input/` and run `./file-rename`. The `input/` and `output/` folders are ignored by git.

## How changes are made here

Tests come first. Write a test in `tests/` that fails because the behaviour is missing, then write the code that makes it pass, then tidy up with the tests still passing. A pull request that changes behaviour without a test for it will be asked for one.

The tool stays a single script with no dependencies. `file_rename.py` uses only the Python standard library, and the tests use only `unittest`. A change that needs a third-party package should be discussed in an issue first.

Tests never touch real files. They work in temporary folders created by the test itself. Never add real photos, documents or other personal files to the repository.

Decisions are recorded. A decision that changes how the project works goes in [`docs/decisions.md`](docs/decisions.md).

## Before you open a pull request

Run the same checks as CI:

```sh
bash -n file-rename
python3 -m py_compile file_rename.py
python3 -m unittest -v
```

Then open the pull request against `main`:

- Keep it to one change, and say in the description what it does and why. Link the issue it closes.
- If it changes what a user sees, add a line under `## [Unreleased]` in [`CHANGELOG.md`](CHANGELOG.md), written for the people who use the tool.
- CI must pass. On your first pull request, CI starts once a maintainer approves the run.
- Expect review comments; a maintainer merges the pull request once it is ready.

## Using coding agents

[`CLAUDE.md`](CLAUDE.md) holds the working rules for AI coding agents. Contributions written with an agent are welcome on the same terms as any other: the tests and the checks above all apply, and you are responsible for what you submit.

## Licence

file-rename is released under the MIT licence. By opening a pull request, you agree that your contribution is released under the same licence.
