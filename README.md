# file-rename

A command-line tool for batch renaming files — either **sequentially** (numbered) or **randomly** (generated names). No dependencies beyond Python 3.

```
╔══════════════════════════════════════════════╗
║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║
╚══════════════════════════════════════════════╝

  Folder:  /Users/simon/photos
  Mode:    sequential
  Filter:  .jpg  (extension: keep)
  Options: prefix='img_'  suffix=''  start=1  step=1  pad=4
  Example: img_0001.jpg

  📁 16 file(s) ready to rename
```

## Usage

```bash
./file-rename                              # Interactive mode
./file-rename ./input                      # Pre-set folder, interactive
./file-rename ./input --seq                # Quick sequential rename
./file-rename ./input --rand               # Quick random rename
./file-rename ./input --seq --preview      # Preview without renaming
```

Or directly with Python:

```bash
python3 file_rename.py [folder] [options]
```

## Interactive commands

Once inside the tool, type `/help` to see all commands:

| Command | Description |
|---------|-------------|
| `/folder <path>` | Set working folder |
| `/seq` | Switch to sequential mode |
| `/rand` | Switch to random mode |
| `/prefix <text>` | Name prefix — e.g. `/prefix photo_` |
| `/suffix <text>` | Name suffix — e.g. `/suffix _final` |
| `/start <n>` | Start number (sequential, default `1`) |
| `/step <n>` | Step size (sequential, default `1`) |
| `/pad <n>` | Zero-pad width (sequential, default `4` → `0001`) |
| `/length <n>` | Name length (random, default `8`) |
| `/charset <name>` | `alphanum` \| `hex` \| `alpha` \| `digits` \| `custom` |
| `/chars <chars>` | Set custom charset characters |
| `/filter [.ext]` | Limit to a file extension — blank resets to all files |
| `/ext keep\|strip` | Preserve or drop the original extension |
| `/preview` | Show old → new mapping without touching files |
| `/go` | Apply renames (confirmation required) |
| `/status` | Show current configuration |
| `/quit` | Exit |

## Non-interactive flags

```
--seq            Sequential mode
--rand           Random mode
--prefix TEXT    Name prefix
--suffix TEXT    Name suffix
--start N        Start number (default 1)
--step N         Step size (default 1)
--pad N          Zero-pad width (default 4)
--length N       Name length for random mode (default 8)
--charset NAME   alphanum | hex | alpha | digits | custom
--chars TEXT     Custom charset characters
--filter .EXT    Only rename files with this extension
--strip-ext      Remove the original extension from new names
--preview        Show preview only, do not rename
--version        Show version and exit
```

## Examples

**Sequential with a prefix:**
```bash
./file-rename ./input --seq --prefix shot_ --pad 3
# Screenshot 2026-04-03.jpg  →  shot_001.jpg
```

**Random 12-character hex names:**
```bash
./file-rename ./input --rand --length 12 --charset hex
# photo.jpg  →  3a9fe1c04b2d.jpg
```

**JPEGs only, preview first:**
```bash
./file-rename ./input --seq --filter .jpg --preview
```

## Version

See [CHANGELOG.md](CHANGELOG.md) for release history.
