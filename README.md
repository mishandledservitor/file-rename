# file-rename

A small interactive CLI tool for renaming files in a folder — either **sequentially** (numbered) or **randomly** (generated names).

## Requirements

Python 3.8+ and one library:

```
pip install rich
```

## Usage

```
python3 file_rename.py [folder]
```

Pass an optional folder path to pre-fill it, or set it from the interactive menu.

## Features

### Two rename modes

**Sequential** — produces ordered, numbered filenames:
```
photo_0001.jpg
photo_0002.jpg
photo_0003.jpg
```
Options: prefix, suffix, start number, step size, zero-pad width.

**Random** — produces unique random filenames:
```
a3Fx9Kqz.jpg
bT7mWnPs.jpg
xQ2rLmVn.jpg
```
Options: name length, charset (alphanumeric / hex / letters / digits / custom).

### Common options

- **Extension filter** — limit renaming to a specific file type (e.g. `.jpg`, `.txt`), or process all files.
- **Preserve extension** — keep the original file extension in the new name (on by default).
- **Preview** — see the full old → new mapping before anything is touched.
- **Conflict detection** — files that would overwrite an existing name are skipped automatically.

## Interactive menu

```
╭─ File Renamer ─ sequential or random ─╮
│                                        │

  Configuration
  ┌──────────────────────────────────┐
  │ Folder    /path/to/my/images     │
  │ Mode      sequential             │
  │ …                                │
  └──────────────────────────────────┘

  Main Menu
    1  Set folder
    2  Choose mode          (sequential / random)
    3  Configure mode options
    4  Extension filter
    5  Preview changes
    6  Apply renames
    q  Quit
```

## Example workflow

1. Run `python3 file_rename.py ./input`
2. Pick **2 → Sequential**
3. Pick **3** and set prefix to `photo_`, padding to `4`
4. Pick **5** to preview the changes
5. Pick **6** and confirm — done

## Version

See [CHANGELOG.md](CHANGELOG.md) for release history.
