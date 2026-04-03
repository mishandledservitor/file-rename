# file-rename

Batch rename files by typing a pattern. Reads from `./input`, writes renamed files to `./output`.

```
╔══════════════════════════════════════════════╗
║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║
╚══════════════════════════════════════════════╝

  Input:  ./input  (16 files)
  Output: ./output

  Type a pattern — NN = sequential,  RND = random:

    image-NN      →  image-01.jpg, image-02.jpg …
    shot_NNNN     →  shot_0001.jpg, shot_0002.jpg …
    file-RND      →  file-a8f3k2xq.jpg …

  /folder <path>   change input folder
  /output <path>   change output folder
  /inplace         toggle rename-in-place (skips output folder)
  /quit            exit

  ▶ shot_NNNN

  Screenshot 2026-04-03 at 16.49.46.jpg  →  shot_0001.jpg
  Screenshot 2026-04-03 at 16.49.48.jpg  →  shot_0002.jpg
  …  10 more  …
  Screenshot 2026-04-03 at 16.50.27.jpg  →  shot_0016.jpg

  16 files  →  apply? [y/N]: y
  ✅ Done!  16 moved to ./output
```

## Usage

```bash
./file-rename            # uses ./input → ./output automatically
./file-rename ./myfolder # override the input folder
```

Or directly:

```bash
python3 file_rename.py [folder]
```

No dependencies — pure Python stdlib.

## Folders

| Folder | Default | Change with |
|--------|---------|-------------|
| Input  | `./input`  | `/folder <path>` or pass as argument |
| Output | `./output` | `/output <path>` |

Drop your files into `./input/`, run the tool, collect renamed files from `./output/`.

To rename files in place instead (no output folder), type `/inplace` to toggle the mode.

## Pattern syntax

| Pattern | Result |
|---------|--------|
| `image-NN` | `image-01.jpg`, `image-02.jpg` … |
| `shot_NNN` | `shot_001.jpg`, `shot_002.jpg` … |
| `photo_NNNN` | `photo_0001.jpg`, `photo_0002.jpg` … |
| `file-RND` | `file-a8f3k2xq.jpg`, `file-9xmq71bk.jpg` … |

- **`NN`** — sequential number. N count sets the zero-padding width (`NN` → `01`, `NNNN` → `0001`).
- **`RND`** — random 8-character alphanumeric string, unique per file.
- Original file extension is always preserved.

## Commands

| Input | Action |
|-------|--------|
| `image-NN` | Preview rename plan, then confirm to apply |
| `/folder <path>` | Change the input folder |
| `/output <path>` | Change the output folder |
| `/inplace` | Toggle rename-in-place (files stay in input folder) |
| `./path/to/dir` | Bare directory path also changes the input folder |
| `/quit` | Exit |

## Version

See [CHANGELOG.md](CHANGELOG.md).
