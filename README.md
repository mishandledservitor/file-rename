# file-rename

file-rename is a small command-line tool that renames a batch of files from one pattern you type. `image-NN` numbers the files `image-01.jpg`, `image-02.jpg` and so on, and `file-RND` gives each one a random 8-character name such as `file-a8f3k2xq.jpg`. It shows every old and new name before it changes anything, keeps each file's extension, and skips a file rather than overwrite one that already has the new name. It's a single Python script with no dependencies.

## What you need

| What | Why |
|---|---|
| macOS or Linux | The `file-rename` launcher is a bash script. On Windows you can run `python file_rename.py` directly, but that isn't tested. |
| Python 3.10 or later | The tool is written in Python and uses only the standard library. |

It needs no account, API key or network access.

## Quick start

1. Clone the repository and go into it:

   ```sh
   git clone https://github.com/mishandledservitor/file-rename.git
   cd file-rename
   ```

2. Create the input folder and copy the files you want to rename into it:

   ```sh
   mkdir input
   cp ~/Desktop/Screenshot*.png input/
   ```

3. Start the tool:

   ```sh
   ./file-rename
   ```

4. Type a pattern such as `shot_NNNN` and press Enter. The tool lists the new names.
5. Type `y` and press Enter to apply them. The renamed files are moved to the `output` folder, which is created if it is missing.
6. Leave with `/quit`.

```
  Input:  /path/to/file-rename/input  (16 files)
  Output: /path/to/file-rename/output

  ▶ shot_NNNN

  Screenshot 2026-04-03 at 16.49.46.png  →  shot_0001.png
  Screenshot 2026-04-03 at 16.49.48.png  →  shot_0002.png
  Screenshot 2026-04-03 at 16.49.51.png  →  shot_0003.png
  Screenshot 2026-04-03 at 16.49.55.png  →  shot_0004.png
  Screenshot 2026-04-03 at 16.49.58.png  →  shot_0005.png
  …  10 more  …
  Screenshot 2026-04-03 at 16.50.27.png  →  shot_0016.png

  16 files  →  apply? [y/N]: y
  ✅ Done!  16 moved to /path/to/file-rename/output
```

To update later, run `git pull` in the folder.

## Usage

```sh
./file-rename              # rename the files in ./input into ./output
./file-rename ~/Pictures   # use another input folder
python3 file_rename.py     # the same without the launcher
./file-rename --version    # print the version
```

### Patterns

| Pattern | Result |
|---|---|
| `image-NN` | `image-01.jpg`, `image-02.jpg`, ... |
| `shot_NNN` | `shot_001.jpg`, `shot_002.jpg`, ... |
| `photo_NNNN` | `photo_0001.jpg`, `photo_0002.jpg`, ... |
| `file-RND` | `file-a8f3k2xq.jpg`, `file-9xmq71bk.jpg`, ... |
| `NN-RND` | `01-a8f3k2xq.jpg`, `02-9xmq71bk.jpg`, ... |

- Two or more `N`s in a row become a sequential number starting at 1, and the number of `N`s sets the zero-padding. A number wider than the padding is kept in full, so the 100th file in `NN` is `100`.
- `RND` becomes 8 random lowercase letters and digits, different for every file in the batch.
- Everything else in the pattern is copied as it is, and the original extension is added at the end.
- Files are numbered in the order of their names as Python sorts them, so `file10` comes before `file2` and capital letters come before lowercase ones.
- A pattern with neither `NN` nor `RND` would give every file the same name, so the tool warns and asks whether to go on.

### Commands

| Input | What it does |
|---|---|
| a pattern | Shows the new names and asks whether to apply them. |
| `/folder <path>` | Changes the input folder. Without a path, it shows the current one. |
| a folder path on its own | Also changes the input folder. |
| `/output <path>` | Changes the output folder and turns off in-place mode. Without a path, it shows the current one. |
| `/inplace` | Switches between renaming files inside the input folder and moving them to the output folder. |
| `/quit`, `/exit` or `/q` | Leaves the tool. Ctrl+C and Ctrl+D also work. |

## Where your files go

By default the tool reads files from the `input` folder and moves the renamed files to the `output` folder, both next to the script. Both folders are ignored by git. In in-place mode the files are renamed where they are and nothing goes to `output`. The tool only moves and renames files: it never deletes or overwrites one, and it sends nothing over the network.

## Known limitations

- A rename can't be undone by the tool, so keep a copy of anything you can't replace.
- A file whose new name already exists in the destination is skipped, and the preview marks it with "⚠ conflict". This also happens in in-place mode when a new name matches a file that has not been renamed yet.
- Hidden files (names starting with a dot) and subfolders are left out.
- The random part is always 8 characters long.

## Development

```sh
python3 -m unittest -v   # run the tests
```

The tests use only the standard library and temporary folders. CI runs them on Python 3.10 and 3.13. [`CLAUDE.md`](CLAUDE.md) holds the working rules for coding agents, and [`docs/decisions.md`](docs/decisions.md) records the project's decisions. To propose a change, see [`CONTRIBUTING.md`](CONTRIBUTING.md). Release notes are in [`CHANGELOG.md`](CHANGELOG.md).

## Licence

file-rename is released under the MIT licence; see [`LICENSE`](LICENSE).
