# Changelog

What changes in file-rename from one release to the next, for people who use it. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [4.0.0] - 2026-04-03

### Added

- The tool reads from an `input` folder next to the script by default, so it no longer needs a folder argument.
- Renamed files are moved to an `output` folder next to the script by default instead of being renamed where they are.
- `/output <path>` changes the output folder.
- `/inplace` switches between renaming files inside the input folder and moving them to the output folder.
- The output folder is created the first time files are moved into it.

## [3.0.0] - 2026-04-03

### Changed

- A single pattern replaces the whole command system: type `image-NN` or `file-RND` and press Enter.
- `NN`, `NNN` or `NNNN` numbers the files in sequence, and the number of `N`s sets the zero-padding.
- `RND` puts a random 8-character string of lowercase letters and digits into each name, different for every file.
- The preview of a large batch shows the first five renames, the last one and a count of the rows in between.
- A pattern without `NN` or `RND` triggers a warning, because every file would get the same name.

### Removed

- The `/prefix`, `/suffix`, `/start`, `/step`, `/pad`, `/length`, `/charset`, `/chars`, `/filter`, `/ext`, `/preview` and `/go` commands are gone.
- All command-line flags except `--version` are gone.

## [2.0.0] - 2026-04-03

### Added

- A `file-rename` launcher script runs the tool without typing `python3`.
- Command-line flags allow a rename without the prompt: `--seq`, `--rand`, `--prefix`, `--suffix`, `--start`, `--step`, `--pad`, `--length`, `--charset`, `--chars`, `--filter`, `--strip-ext` and `--preview`.
- `/status` shows the current settings and the number of files.
- `/filter` narrows the files and shows how many still match.
- The preview table fits the width of the terminal.
- A progress bar shows while files are renamed.
- `--version` prints the version.

### Changed

- The tool was rewritten as a persistent prompt (`▶`) that takes `/command` input, replacing the menus.
- The tool uses only the Python standard library.

### Removed

- The `rich` dependency is gone.

## [1.0.0] - 2026-04-03

### Added

- An interactive menu, built with `rich`, drives the tool.
- Sequential renaming takes a prefix, a suffix, a start number, a step and a zero-padding width.
- Random renaming takes a name length and a character set (letters and digits, hexadecimal, letters, digits or your own characters).
- An extension filter limits renaming to one file type.
- The original file extension can be kept or dropped.
- A preview shows every old and new name before anything is renamed.
- A file whose new name already exists is skipped instead of overwritten.
- A folder passed on the command line becomes the working folder at launch.
