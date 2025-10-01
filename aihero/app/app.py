import streamlit as st
from pathlib import Path

from core.read import read_repo_data
from core.chunks import chunk_text
# from core.log import log_interaction_to_file
from utils.utils import save_chunks_jsonl, load_chunks_jsonl, list_chunks
from core.search import create_text_index, create_vector_index, load_embedding_model
from core.agent import create_agent, run_agent
from core.agent_tools import make_agent_tools


# --- Streamlit App ---
st.set_page_config(page_title="AI Agent Crashcourse", layout="wide")

st.title("🤖 AI Agent Crashcourse — Github repo Q&A App")


# --- Sidebar Settings ---
st.sidebar.header("⚙️ Settings")

owner = st.sidebar.text_input("Repo owner", "TheAlgorithms")
repo = st.sidebar.text_input("Repo name", "Python")
branch = st.sidebar.text_input("Branch", "master")
strategy = st.sidebar.selectbox("Chunking strategy", ["simple", "sliding", "paragraph", "section"])
level = st.sidebar.number_input("Markdown header level (for section)", min_value=1, max_value=6, value=2)
size = st.sidebar.number_input("Chunk size (for simple/sliding)", min_value=50, max_value=5000, value=1000, step=50)
step = st.sidebar.number_input("Chunk step (for sliding)", min_value=10, max_value=5000, value=500, step=10)
# add button to save chunks

# Add title for this part
st.sidebar.subheader("🛠️ Advanced settings")
save_chunks = st.sidebar.checkbox("Save chunks to disk", value=False)
mode = st.sidebar.radio("Mode", ["Generate new chunks", "Load existing chunks"])
# Existing chunks list
chunks_files = list_chunks()
chunks_choice = None
if mode == "Load existing chunks" and chunks_files:
    chunks_labels = [f"{c['meta']['owner']}/{c['meta']['repo']} ({c['meta']['strategy']})" for c in chunks_files]
    chunks_choice = st.sidebar.selectbox("Select chunks file", range(len(chunks_files)), format_func=lambda i: chunks_labels[i])


# --- Main Q&A Section ---
st.subheader("Ask a Question")

question = st.text_input("Enter your question", "")

if st.button("Go fetch!") and question:
    with st.spinner("Agent in action..."):
        # Step 1. Load or create chunks
        if mode == "Generate new chunks":
            docs = read_repo_data(owner, repo, branch=branch)
            all_chunks = []
            for doc in docs:
                if strategy == "section":
                    doc_chunks = chunk_text(doc.get("content", ""), method="section", level=level)
                else:
                    doc_chunks = chunk_text(doc.get("content", ""), method=strategy, size=size, step=step)
                # Add metadata
                for c in doc_chunks:
                    c.update({"filename": doc.get("filename")})
                all_chunks.extend(doc_chunks)

            # Save chunks
            if save_chunks:
                save_path = save_chunks_jsonl(
                    all_chunks,
                    owner,
                    repo,
                    branch,
                    strategy,
                )
                st.sidebar.success(f"✅ Chunks saved to {save_path}")
            else:
                st.sidebar.info("ℹ️ Chunks were not saved to disk.")

        elif mode == "Load existing chunks" and chunks_choice is not None:
            chunks_path = chunks_files[chunks_choice]["path"]
            all_chunks = load_chunks_jsonl(chunks_path)
        else:
            st.error("No chunks available.")
            st.stop()

        # Step 2. Build indexes
        text_index = create_text_index(all_chunks)
        embedding_model = load_embedding_model()
        vector_index = create_vector_index(all_chunks, embedding_model)

        # Step 3. Create tools + agent
        tools = make_agent_tools(text_index, vector_index, embedding_model)
        agent = create_agent(prompt_file_path="prompts/system_prompt.yml", model_name="gpt-4o-mini", tools=tools)

        # Step 4. Run agent
        result = run_agent(agent, question)

        # Step 5. Show result
        answer = getattr(result, "output", None) or str(result)
        st.markdown("### 🧾 Answer")
        st.markdown(answer)
