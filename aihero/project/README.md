# AI Agent Crashcourse — Project

This folder contains the code developed day by day following the AI Agent Crashcourse.
Each day adds new functionality toward building an ingestion and retrieval pipeline.

---

## Table of Contents
- [Day 1 - Ingest and Index Your Data](#day-1--ingest-and-index-your-data)
- [Day 2 - Chunking Documents](#day-2--chunking-documents)

---

# Day 1 — Ingest and Index Your Data

## Goal
Download and parse Markdown files from a GitHub repository, extract their frontmatter and content, and make them available as Python dictionaries. This lays the foundation for later indexing and search.

## Functions Implemented

### `read_repo_data`
**Location:** `./read.py`

- Downloads a GitHub repository as a zip archive (via `https://codeload.github.com`).
- Parameters:
  - `repo_owner` — GitHub org/user
  - `repo_name` — Repository name
  - `prefix` — Download base URL (default: `https://codeload.github.com`)
  - `branch` — Branch to fetch (default: `main`)
- Extracts `.md` / `.mdx` files only.
- Parses YAML frontmatter with `python-frontmatter`.
- Returns a list of dicts with:
  - frontmatter keys
  - `content` — Markdown body
  - `filename` — path inside the repo archive

### `read_repo` (CLI)
**Location:** `./read_repo.py`

- CLI wrapper around `read_repo_data`.
- Args:
  - `--owner` (required)
  - `--repo` (required)
  - `--branch` (default: `main`)
- Prints the number of parsed Markdown documents and the first two entries (demo only).

## Usage

Using **TheAlgorithms/Python** (default branch is `master`):

```bash
python aihero/project/read_repo.py --owner TheAlgorithms --repo Python --branch master
```
---

# Day 2 — Chunking Documents

## Goal
Split large documents into smaller, self-contained chunks so they can later be embedded and indexed effectively.

## Functions Implemented

### `simple_chunking`, `sliding_window_chunking`, `split_by_paragraphs`, `split_markdown_by_level`
**Location:** `./chunks.py`

- `simple_chunking` — fixed, non-overlapping windows
- `sliding_window_chunking` — overlapping windows to preserve context
- `split_by_paragraphs` — split on blank lines (`\n\n`)
- `split_markdown_by_level` — split by Markdown headers (default: `##`)

All return a list of dicts:
- `start` — start char offset
- `end` — end char offset
- `chunk` — text content

### `chunk_text` (dispatcher)
**Location:** `./chunks.py`
Selects any of the above methods via a single function.

### `io helpers` (optional)
**Location:** `./io.py`
- `save_chunks_jsonl(chunks, path, ensure_ascii=False)`
- `load_chunks_jsonl(path)`

### `chunk_repo` (CLI)
**Location:** `./chunk_repo.py`

Args:
- `--owner`, `--repo`, `--branch`
- `--method` → `simple` | `sliding` | `paragraph` | `section`
- `--size`, `--step` (for simple/sliding)
- `--level` (for section split)
- `--save-json` (optional: save chunks as JSONL)

Prints total chunks and first two examples.

## Usage

Using **TheAlgorithms/Python** (branch `master`):

```bash
# Simple chunking
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method simple --size 1000

# Sliding window
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method sliding --size 1000 --step 500

# Paragraphs
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method paragraph

# Sections (## level)
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --level 2

# Save chunks for Day 3
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --level 2 --save-json chunks.jsonl
```
---

# Day 3 — Search

## Goal
Add lexical (text), vector (semantic), and hybrid search on top of chunked documents.

## Functions Implemented

**Location:** `./search.py`

- `create_text_index(chunks)` — build a text index with `minsearch.Index`
- `load_embedding_model(model_name)` — load SentenceTransformer (default: `multi-qa-distilbert-cos-v1`)
- `create_vector_index(chunks, model, text_field="chunk")` — build a vector index with `minsearch.VectorSearch`
- `text_search(index, query, top_k=5)` — keyword search
- `vector_search(vindex, model, query, top_k=5)` — semantic search
- `hybrid_search(index, vindex, model, query, top_k=5)` — combine & deduplicate results (by filename)

## CLI

### `search_repo` (CLI)
**Location:** `./search_repo.py`

Args:
- `--chunks-file` — path to JSONL produced on Day 2
- `--mode` — `text` | `vector` | `hybrid`
- `--query` — query string
- `--top-k` — number of results (default: 5)

Prints filename, snippet, and score (if available).

## Usage

```bash
# Text search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode text --query "binary search"

# Vector search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode vector --query "binary search"

# Hybrid search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode hybrid --query "binary search"
```
