# AI Agent Crashcourse -Project

This folder contains the code developed day by day following the AI Agent Crashcourse.
Each day adds new functionality toward building an ingestion and retrieval pipeline.

---

## Table of Contents
- [Day 1 - Ingest and Index Your Data](#day-1---ingest-and-index-your-data)
- [Day 2 - Chunking Documents](#day-2---chunking-documents)
- [Day 3 - Search](#day-3---search)
- [Day 4 - Agent and Tools](#day-4---agent-and-tools)
- [Day 5 - Evaluation](#day-5---evaluation)

---

# Day 1 - Ingest and Index Your Data

## Goal
Download and parse Markdown files from a GitHub repository, extract their frontmatter and content, and make them available as Python dictionaries. This lays the foundation for later indexing and search.

## Functions Implemented

### `read_repo_data`
**Location:** `./read.py`

- Downloads a GitHub repository as a zip archive (via `https://codeload.github.com`).
- Parameters:
  - `repo_owner` -GitHub org/user
  - `repo_name` -Repository name
  - `prefix` -Download base URL (default: `https://codeload.github.com`)
  - `branch` -Branch to fetch (default: `main`)
- Extracts `.md` / `.mdx` files only.
- Parses YAML frontmatter with `python-frontmatter`.
- Returns a list of dicts with:
  - frontmatter keys
  - `content` -Markdown body
  - `filename` -path inside the repo archive

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

# Day 2 - Chunking Documents

## 📌 Goal
Split large documents into smaller, self-contained chunks so they can later be embedded and indexed effectively.

## 🛠️ Functions Implemented

### `simple_chunking`, `sliding_window_chunking`, `split_by_paragraphs`, `split_markdown_by_level`
**Location:** `./chunks.py`

- `simple_chunking` -fixed, non-overlapping windows
- `sliding_window_chunking` -overlapping windows to preserve context
- `split_by_paragraphs` -split on blank lines (`\n\n`)
- `split_markdown_by_level` -split by Markdown headers (default: `##`)

All return a list of dicts:
- `start` -start char offset
- `end` -end char offset
- `chunk` -text content

### `chunk_text` (dispatcher)
**Location:** `./chunks.py`
Selects any of the above methods via a single function.

### `io helpers`
**Location:** `./utils.py`
- `save_chunks_jsonl(chunks, path, ensure_ascii=False)`
- `load_chunks_jsonl(path)`

### `chunk_repo` (CLI)
**Location:** `./chunk_repo.py`

Args:
- `--owner`, `--repo`, `--branch`
- `--method` → `simple` | `sliding` | `paragraph` | `section`
- `--size`, `--step` (for simple/sliding)
- `--level` (for section split)
- `--save_json` (optional: if used without argument, saves to `chunks.jsonl`; if a string is provided, that is used as the filename)

Prints total chunks and first two examples.

## ▶️ Usage

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

# Save chunks (default filename chunks.jsonl)
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --save_json

# Save chunks to custom filename
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --save-json file_name.jsonl
```
---

# Day 3 - Search

## 📌 Goal
Add lexical (text), vector (semantic), and hybrid search on top of chunked documents.

## 🛠️ Functions Implemented

**Location:** `./search.py`

- `create_text_index(chunks)` -build a text index with `minsearch.Index`
- `load_embedding_model(model_name)` -load SentenceTransformer (default: `multi-qa-distilbert-cos-v1`)
- `create_vector_index(chunks, model, text_field="chunk")` -build a vector index with `minsearch.VectorSearch`
- `text_search(index, query, top_k=5)` -keyword search
- `vector_search(vindex, model, query, top_k=5)` -semantic search
- `hybrid_search(index, vindex, model, query, top_k=5)` -combine & deduplicate results

### `search_repo` (CLI)
**Location:** `./search_repo.py`

Args:
- `--chunks-file` -path to JSONL file produced by Day 2 (`--save-json`)
- `--mode` -`text` | `vector` | `hybrid`
- `--query` -search query string
- `--top-k` -number of results (default: 5)

Prints the top results with filename, snippet, and score (if available).

---

## ▶️ Usage

First, create chunks with Day 2 CLI and save them:

```bash
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --save-json
```

This produces a chunks.jsonl file.
Now, run different search strategies on those chunks:
```bash
# Text search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode text --query "your query"

# Vector search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode vector --query "your query"

# Hybrid search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode hybrid --query "your query"
```

---

🔄 Main Changes to Previous Days

Day 2 (chunk_repo.py)

- Extended chunking to cover all documents in the repository (not just the first one).
- Added saving support (--save-json) so all chunks can be persisted to disk.
- New utility functions in utils.py
  - save_chunks_jsonl and load_chunks_jsonl handle saving and loading of chunks to JSONL format.

---

🧪 Testing from Chunking to Search

1. TheAlgorthms repo
```bash
# Create chunks (use level 1 has most markdowns have only level 1 and refs in levels 2)
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --level 1 --save-json algo_chunks.jsonl
# Run vector search
python aihero/project/search_repo.py --chunks-file algo_chunks.jsonl --mode vector --query "What are the main sorting orders?"
```

2. LangChain repo
```bash
# Create chunks
python aihero/project/chunk_repo.py --owner langchain-ai --repo langchain --branch master --method section --level 2 --save-json langchain_chunks.jsonl

# Run vector search
python aihero/project/search_repo.py --chunks-file langchain_chunks.jsonl --mode vector --query "What are the main chunking methods available?"~
```
# Day 4 - Agent and tools

## 📌 Goal
Build an agent that uses the search tools to answer questions strictly from repository documentation.

## 🛠️ Functions Implemented

### `make_agent_tools`
**Location:** `./agent_tools.py`
Wraps the search functions (`text_search`, `vector_search`, `hybrid_search`) so they are agent-ready with dependencies bound (indexes + model).

### `create_agent` / `run_agent`
**Location:** `./agent.py`
- `create_agent(system_prompt_path, model_name, tools)` -builds a Pydantic AI agent with a system prompt and the selected tool(s).
- `run_agent(agent, user_question)` -runs the agent with the given query.

### System Prompts
**Location:** `./prompts/`
- `system_prompt.yml` - answers only from repo docs, otherwise replies with `"I don't know based on the repository documentation."`
- `system_prompt_multitry.yml`- allows multiple search tries.

### `agent_repo` (CLI)
**Location:** `./agent_repo.py`

Args:
- `--chunks-file` - path to JSONL file with chunks
- `--query` - user query string
- `--prompt` - YAML file with system prompt (default: strict)
- `--model` - LLM model name (default: gpt-4o-mini)
- `--tool` - which search tool to expose: `text`, `vector`, `hybrid`

Answers are printed in Markdown, with a **Sources** section listing filenames.

---

## ▶️ Usage

Example with LangChain repo:

```bash
python aihero/project/agent_repo.py \
  --chunks-file langchain_chunks.jsonl \
  --tool vector \
  --query "What are the main chunking methods available?" \
  --prompt prompts/system_prompt_strict.yml \
  --model gpt-4o-mini
```

# Day 5 - Evaluation

## 📌 Goal
Introduce systematic evaluation of the agent:
- Define an evaluation set of queries.
- Run the agent with different tools (text, vector, hybrid).
- Collect and inspect results.
- Log interactions for later review and analysis.
- Add helper functions to streamline evaluation.

This step helps identify failure modes (hallucinations, missed answers) and decide how to improve prompts, chunking, and search strategies.

---

## 🛠️ Functions Implemented

### Logging
**Location:** `./log.py`

- Creates a `logs/` directory if not present.
- `log_interaction_to_file(agent, messages, source="user")`
  - Saves a full agent interaction (agent, messages, metadata) to a uniquely named JSON file.
  - Filenames include timestamp + random hex for uniqueness.
  - Custom serializer handles `datetime` → ISO format.

### Evaluation Helpers
**Location:** `./eval.py`

- `generate_questions_from_chunks(chunks, model, template)`
  Uses an LLM + a prompt template to automatically generate candidate evaluation questions from your repo chunks.

- `simplify_log_messages(messages)`
  Cleans up raw agent message logs into a simplified, human-readable format.

- `extract_question_answer(log_record)`
  Extracts the user’s question and the agent’s answer from a saved log record.

- `evaluate_log_record(log_path, eval_agent)`
  Loads a single saved interaction log (one question), then calls an **LLM-based evaluation agent** to judge the quality of the answer against expectations.
  This allows automated, qualitative assessment.

### Prompts & Templates
**Location:** `./prompts/templates/`

- Prompt templates for generating evaluation questions and for guiding the evaluation agent.
- System prompts for strict vs. permissive agent behavior.

### Evaluation Notebook
**Location:** `./notebooks/agent_eval.ipynb`

Exploratory steps:
1. Load chunks from repo (`algo_chunks.jsonl` / `langchain_chunks.jsonl`).
2. Build text and vector indexes.
3. Generate questions from repository chunks
4. Run agent with different tools (`text`, `vector`, `hybrid`) on generated questions.
5. Collect answers and evaluate using LLM as a judge

---

## ▶️ Usage

Run evaluation interactively in the notebook:

```bash
jupyter notebook notebooks/agent_eval.ipynb
