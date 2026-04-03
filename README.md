# file-rename

Batch rename files by typing a pattern. No menus, no options — just type what you want and confirm.

```
╔══════════════════════════════════════════════╗
║    📂  FILE RENAME — BATCH FILE RENAMER  📂    ║
╚══════════════════════════════════════════════╝

  Folder: /Users/simon/photos  (16 files)

  Type a pattern — NN = sequential,  RND = random:

    image-NN      →  image-01.jpg, image-02.jpg …
    shot_NNNN     →  shot_0001.jpg, shot_0002.jpg …
    file-RND      →  file-a8f3k2xq.jpg …

  /folder <path>   change folder     /quit   exit

  ▶ shot_NNNN

  Screenshot 2026-04-03 at 16.49.46.jpg  →  shot_0001.jpg
  Screenshot 2026-04-03 at 16.49.48.jpg  →  shot_0002.jpg
  …
  Screenshot 2026-04-03 at 16.50.27.jpg  →  shot_0016.jpg

  16 files  →  apply? [y/N]: y
  ✅ Done!  16 renamed
```

## Usage

```bash
./file-rename             # interactive (set folder inside)
./file-rename ./input     # interactive with folder pre-set
```

Or directly:

```bash
python3 file_rename.py [folder]
```

No dependencies — pure Python stdlib.

## Pattern syntax

| Pattern | Result |
|---------|--------|
| `image-NN` | `image-01.jpg`, `image-02.jpg` … |
| `shot_NNN` | `shot_001.jpg`, `shot_002.jpg` … |
| `photo_NNNN` | `photo_0001.jpg`, `photo_0002.jpg` … |
| `file-RND` | `file-a8f3k2xq.jpg`, `file-9xmq71bk.jpg` … |
| `img-NN-RND` | `img-01-a8f3k2xq.jpg` … |

- **`NN`** — sequential number. The number of `N`s sets the zero-padding width (`NN` = 2 digits, `NNNN` = 4 digits).
- **`RND`** — random 8-character alphanumeric string, unique per file.
- The original file extension is always preserved.

## Commands

| Input | Action |
|-------|--------|
| `image-NN` | Preview + apply a rename pattern |
| `/folder <path>` | Change the working folder |
| `./path/to/folder` | Also changes folder (bare path works too) |
| `/quit` | Exit |

## Version

See [CHANGELOG.md](CHANGELOG.md).
