# AI Agent Crashcourse — Project

This folder contains the code developed day by day following the AI Agent Crashcourse.
Each day adds new functionality toward building an ingestion and retrieval pipeline.

---

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
```
---

# Day 2 — Chunking Documents

## 📌 Goal
Split large documents into smaller, self-contained chunks so they can later be embedded and indexed effectively.

---

## 🛠️ Functions Implemented

### `simple_chunking`, `sliding_window_chunking`, `paragraph_chunking`, `markdown_section_chunking`
Located in [`chunks.py`](./chunks.py).

- `simple_chunking`: Fixed non-overlapping windows.
- `sliding_window_chunking`: Overlapping windows to preserve context.
- `paragraph_chunking`: Split by paragraphs (`\n\n`).
- `markdown_section_chunking`: Split by Markdown headers (default: `##`).

All chunking functions return a list of dictionaries with:
- `start`: start character offset
- `end`: end character offset
- `chunk`: text content

### `chunk_text`
Dispatcher function in [`chunks.py`](./chunks.py).
Allows selecting the chunking method with a single parameter.

### `chunking_repo`
Located in [`chunking_repo.py`](./chunking_repo.py).

- CLI wrapper to demo chunking strategies on ingested docs. Uses the first ingested doc as example.
- Uses `argparse` for command-line parameters:
  - `--method` → `simple`, `sliding`, `paragraph`, or `section`
  - `--size` and `--step` → used in simple/sliding
  - `--level` → used in section-based splitting
- Prints the total number of chunks and the first two as examples.

---

## ▶️ Usage

Example with [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) (branch `master`):

```bash
# Simple chunking
python aihero/project/chunking_repo.py --owner TheAlgorithms --repo Python --branch master --method simple --size 1000 --step 500

# Sliding window
python aihero/project/chunking_repo.py --owner TheAlgorithms --repo Python --branch master --method sliding --size 1000 --step 500

# Paragraphs
python aihero/project/chunking_repo.py --owner TheAlgorithms --repo Python --branch master --method paragraph

# Sections by headers (##)
python aihero/project/chunking_repo.py --owner TheAlgorithms --repo Python --branch master --method section --level 2
