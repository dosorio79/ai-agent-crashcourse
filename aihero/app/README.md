# Day 6 — Building the App

## 📌 Goal
Turn the ingestion, chunking, search, and agent pipeline into an interactive application.
We use **Streamlit** to provide a simple web UI for asking questions against repository documentation.

---

## 🛠️ Features Implemented

### Streamlit Q&A App
**Location:** `./app/app.py`

- Sidebar inputs for repo owner, name, branch, and chunking strategy.
- Support for all chunking strategies (`simple`, `sliding`, `paragraph`, `section`).
  - `section` mode includes adjustable header level.
  - `simple/sliding` allow numeric `size` and `step` parameters.
- Option to **save chunks** to disk with structured filenames via `utils.save_chunks_jsonl`.
- Option to **load previously saved chunks** (`utils.list_chunks`).
- Automatic construction of text and vector indexes (`minsearch`).
- Tools created for **text, vector, and hybrid search** (from `core.agent_tools`).
- Agent created with a system prompt (`prompts/system_prompt.yml`) and toolset.
- User can enter a question and trigger the **full pipeline** → answer displayed in Markdown.

### Utilities
- `utils.utils` now also handles:
  - Structured chunk saving (`owner_repo_branch_strategy_timestamp.jsonl`).
  - Chunk listing and metadata parsing.
- Chunks and logs stored locally in `data/` and `logs/`.

---

## ▶️ Usage

### Run the app locally
```bash
cd aihero/app
streamlit run app.py
