# ai-agent-crashcourse

A conversational agent that can answer questions about any GitHub repository.  
Think of it as your personal AI assistant for documentation and code.  

---

## 📂 Repository Structure

This repository has two main parts:

- **`aihero/`**  
  The main project folder was developed step by step following the [AI Hero course](https://alexeygrigorev.com/aihero/).  
  - **`project/`** 
  Contains the code for ingestion, chunking, search, and the final agent, along with CLIs and system prompts.  
  This `README.md` documents progress day by day.

  - **`course/`**  
  Contains the course notebooks and personal experiments. This is a sandbox area for testing ideas outside of the main project pipeline.

---

## 🚀 Features (built day by day in `aihero/project/`)

- **Day 1**: Ingest GitHub repos → extract Markdown + frontmatter  
- **Day 2**: Chunk documents → simple, sliding, paragraph, section-based  
- **Day 3**: Search → text, vector, and hybrid search  
- **Day 4**: Agent and Tools → function calling, system prompts, and interactive QA  

---

## ▶️ How to Use

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
