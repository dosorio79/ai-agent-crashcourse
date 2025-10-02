# 🧑‍💻 AI Agent Crashcourse

A conversational agent that can answer questions about any GitHub repository.
Think of it as your personal AI assistant for documentation and code.

---

## 📂 Repository Structure

This repository has two main parts:

- **`aihero/project/`**
  Step-by-step implementation following the [AI Hero course](https://alexeygrigorev.com/aihero/).
  - **`read_repo.py`** → Download & parse repo docs
  - **`chunk_repo.py`** → Split into chunks
  - **`search_repo.py`** → Text / vector / hybrid search
  - **`agent_repo.py`** → Run an agent with different tools
  - **`eval.py`** → Evaluate agent outputs
  - **`prompts/`** → System & eval prompts in YAML
  - **`utils/`** → Helper functions for saving/loading chunks

  📑 This folder also contains a **day-by-day README** documenting progress and insights.

- **`aihero/app/`**
  A standalone **Streamlit application** that exposes the pipeline as a web interface.
  - Optional chunk saving/loading
  - Interactive Q&A with the agent
  - Sidebar controls for repo/chunk settings
  - Clean modular structure (reusing the `core/` code)

- **`aihero/course/`**
  Sandbox notebooks and experiments, used to explore before modularizing into the project.

---

## 🚀 Features

- **Day 1**: Ingest GitHub repos → extract Markdown + frontmatter
- **Day 2**: Chunk documents → simple, sliding, paragraph, section-based
- **Day 3**: Search → text, vector, and hybrid search
- **Day 4**: Agent and Tools → function calling, system prompts, and interactive QA
- **Day 5**: Logging & Evaluation → record agent outputs, evaluate with LLM as judge
- **Day 6**: Web App → Streamlit frontend for the pipeline
- **Day 7**: Wrap-up & CLI → end-to-end pipeline in one command

---

## ▶️ How to Use

### CLI (project folder)
Each step provides a CLI for demonstration:

```bash
# Ingest a repository
python aihero/project/read_repo.py --owner TheAlgorithms --repo Python --branch master

# Chunk into sections
python aihero/project/chunk_repo.py --owner TheAlgorithms --repo Python --branch master --method section --save-json

# Search
python aihero/project/search_repo.py --chunks-file chunks.jsonl --mode vector --query "What are the main sorting methods?"

# Agent
python aihero/project/agent_repo.py --chunks-file chunks.jsonl --tool vector --query "What are the main sorting methods?"
```

### Streamlit App (app folder)

```bash
cd aihero/app
uv sync   # or pip install -r requirements.txt
uv run streamlit run app.py
```

This launches the interactive UI where you can:
- Enter repo owner/name/branch
- Choose chunking strategy and save/load chunks
- Ask free-form questions and get answers

---

## 🔮 Next Steps

- Improve hybrid search weighting
- Add memory to agent conversations
- Experiment with more evaluation metrics
- Explore deployment beyond local Streamlit
