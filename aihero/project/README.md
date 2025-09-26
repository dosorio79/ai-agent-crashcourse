# Day 1 — Ingest and Index Your Data

## 📌 Goal
Download and parse Markdown files from a GitHub repository, extract their frontmatter and content, and make them available as Python dictionaries.
This sets the foundation for indexing and querying the docs in later steps.

---

## 🛠️ Functions Implemented

### `read_repo_data`
Located in [`read.py`](./read.py).

- Downloads a GitHub repository as a zip archive (using **codeload.github.com**).
- Supports configurable:
  - `repo_owner` → GitHub organization/user
  - `repo_name` → Repository name
  - `prefix` → Base URL for downloads (default: `https://codeload.github.com`)
  - `branch` → Branch to fetch from (default: `main`)
- Extracts only `.md` and `.mdx` files.
- Parses [YAML frontmatter](https://jekyllrb.com/docs/front-matter/) with [`python-frontmatter`](https://github.com/eyeseast/python-frontmatter).
- Returns a list of dictionaries with:
  - All frontmatter keys
  - `content`: Markdown body
  - `filename`: Path inside the repository archive

### `read_algo_python`
Located in [`read_algo_python.py`](./read_algo_python.py).

- CLI wrapper around `read_repo_data`.
- Uses `argparse` for command-line parameters:
  - `--owner` → Repository owner (required)
  - `--repo` → Repository name (required)
  - `--branch` → Branch (default: `main`)
- Prints the number of parsed Markdown documents and pretty-prints the first two entries.
- For Day 1, the script **only prints** the results as a demo.  
  (Later will return and save the data for indexing.)

---

## ▶️ Usage

For this exercise, the chosen repository is
👉 [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python)

⚠️ Note: its default branch is `master`.

```bash
python aihero/project/read_algo_python.py --owner TheAlgorithms --repo Python --branch master
