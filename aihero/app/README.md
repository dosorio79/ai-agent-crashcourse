# 🤖 AI Agent Crashcourse — App

This folder contains the **Streamlit web app** and **CLI pipeline** for interacting with GitHub repository documentation using an AI-powered agent.

---

## 🚀 Features
- Ingest GitHub repositories (Markdown files)
- Multiple chunking strategies:
  - Simple
  - Sliding
  - Paragraph
  - Markdown sections
- Save & load chunks (`data/` folder, JSONL format)
- Search:
  - Text (keyword)
  - Vector (semantic)
  - Hybrid (combined)
- Conversational agent powered by **OpenAI (gpt-4o-mini)** and **Pydantic AI**
- Streamlit web interface for interactive Q&A
- CLI pipeline for terminal-based usage

---

## 📦 Installation

Move into the `app/` folder and set up with **uv**:

```bash
cd aihero/app
uv sync
```

Create a `.env` file with your API key:

```env
OPENAI_API_KEY=sk-xxxxxx
```

---

## ▶️ Running the Streamlit App

Start the app:

```bash
uv run streamlit run app.py
```

Open your browser at 👉 [http://localhost:8501](http://localhost:8501)

---

## ⚙️ Streamlit App Usage

1. In the **sidebar**, choose:
   - Repo owner, name, branch
   - Chunking strategy & parameters
   - Whether to generate or load chunks
   - Optionally save chunks to `data/`
2. Enter your question in the main panel
3. The agent will search the documentation and return an answer

---

## 🖥️ CLI — Agent Pipeline

An alternative to the Streamlit app is the **CLI pipeline**.

Run the pipeline:

```bash
uv run python cli.py --owner TheAlgorithms --repo Python --branch master --method section --level 1
```

Once loaded, you can ask multiple questions interactively:

```text
❓ Question: What are the main sorting orders?
🧾 Answer: ...
❓ Question: How is quicksort explained?
🧾 Answer: ...
```

Type `exit` or `quit` to leave.

### CLI Arguments
- `--owner` (required) → GitHub repo owner
- `--repo` (required) → GitHub repo name
- `--branch` (default: main) → Repo branch
- `--method` (default: section) → Chunking method (`simple`, `sliding`, `paragraph`, `section`)
- `--size` (default: 1000) → Chunk size (for simple/sliding)
- `--step` (default: 500) → Step size (for sliding)
- `--level` (default: 2) → Markdown header level (for section)
- `--save-json` → Save chunks to disk

---

## 🎯 Goal

The goal of this app is to demonstrate:
- How to build modular AI pipelines
- How to integrate retrieval, search, and agents into a usable application
- How to transition from Jupyter exploration to a shareable interface (web app + CLI)

This project follows the **AI Agent Crashcourse (AI Hero)** by [Alexey Grigorev](https://alexeygrigorev.com/aihero/).
