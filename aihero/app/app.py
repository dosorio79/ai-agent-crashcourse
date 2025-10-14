import streamlit as st
from core.read import read_repo_data
from core.chunks import chunk_text
from utils.utils import save_chunks_jsonl, load_chunks_jsonl, list_chunks
from core.search import create_text_index, create_vector_index, load_embedding_model
from core.agent import create_agent, run_agent
from core.agent_tools import make_agent_tools

st.set_page_config(page_title="🤖 AI Agent Crashcourse", layout="wide")
st.title("🤖 GitHub Repo Q&A")

# --- Session init ---
if "agent" not in st.session_state:
    st.session_state.agent = None
if "ready" not in st.session_state:
    st.session_state.ready = False
if "history" not in st.session_state:
    st.session_state.history = []

# --- Cache layers ---
@st.cache_data(show_spinner=False)
def load_and_chunk_repo(owner, repo, branch, strategy, level, size, step):
    docs = read_repo_data(owner, repo, branch=branch)
    all_chunks = []
    for doc in docs:
        if strategy == "section":
            doc_chunks = chunk_text(doc.get("content", ""), method="section", level=level)
        else:
            doc_chunks = chunk_text(doc.get("content", ""), method=strategy, size=size, step=step)
        for c in doc_chunks:
            c.update({"filename": doc.get("filename")})
        all_chunks.extend(doc_chunks)
    return all_chunks

@st.cache_resource(show_spinner=False)
def build_indexes(all_chunks):
    text_index = create_text_index(all_chunks)
    embedding_model = load_embedding_model()
    vector_index = create_vector_index(all_chunks, embedding_model)
    return text_index, vector_index, embedding_model

@st.cache_resource(show_spinner=False)
def build_agent(_text_index, _vector_index, _embedding_model):
    tools = make_agent_tools(_text_index, _vector_index, _embedding_model)
    return create_agent(
        prompt_file_path="prompts/system_prompt.yml",
        model_name="gpt-4o-mini",
        tools=tools
    )

# --- Sidebar buttons (top) ---
st.sidebar.subheader("⚡ Session Controls")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button("🆕 Reset", key="reset_btn"):
        st.session_state.history = []
        st.rerun()
with col2:
    if st.button("🧹 Cache", key="clear_cache_btn"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.ready = False
        st.session_state.agent = None
        st.sidebar.warning("Cache cleared — please reinitialize agent.")
        st.rerun()
with col3:
    init_clicked = st.button("🚀 Init", key="init_btn")

st.sidebar.divider()

# --- Sidebar inputs ---
st.sidebar.header("⚙️ Repository")
owner = st.sidebar.text_input("Repo owner", "TheAlgorithms")
repo = st.sidebar.text_input("Repo name", "Python")
branch = st.sidebar.text_input("Branch", "master")

st.sidebar.header("📄 Chunking")
strategy = st.sidebar.selectbox("Chunking strategy", ["simple", "sliding", "paragraph", "section"])
level = st.sidebar.number_input("Markdown header level (section)", 1, 6, 2)
size = st.sidebar.number_input("Chunk size", 50, 5000, 1000, step=50)
step = st.sidebar.number_input("Chunk step (for sliding)", 10, 5000, 500, step=10)

st.sidebar.header("🛠️ Advanced")
save_chunks = st.sidebar.checkbox("Save chunks to disk", value=False)
mode = st.sidebar.radio("Mode", ["Generate new chunks", "Load existing chunks"])

chunks_files = list_chunks()
chunks_choice = None
if mode == "Load existing chunks" and chunks_files:
    labels = [f"{c['meta']['owner']}/{c['meta']['repo']} ({c['meta']['strategy']})" for c in chunks_files]
    chunks_choice = st.sidebar.selectbox(
        "Select chunks file", range(len(chunks_files)), format_func=lambda i: labels[i]
    )

st.sidebar.divider()

# --- Initialization logic with visible messages ---
if init_clicked:
    log = st.container()
    with st.spinner("Initializing agent..."):
        log.write("📥 Reading and chunking repository...")
        if mode == "Generate new chunks":
            all_chunks = load_and_chunk_repo(owner, repo, branch, strategy, level, size, step)
            if save_chunks:
                save_path = save_chunks_jsonl(all_chunks, owner, repo, branch, strategy)
                log.write(f"💾 Saved chunks to `{save_path}`")
            else:
                log.write("ℹ️ Chunks not saved to disk.")
        elif mode == "Load existing chunks" and chunks_choice is not None:
            chunks_path = list_chunks()[chunks_choice]["path"]
            all_chunks = load_chunks_jsonl(chunks_path)
            log.write(f"📂 Loaded existing chunks from `{chunks_path}`")
        else:
            st.error("No chunks available.")
            st.stop()

        log.write("🔍 Building indexes...")
        text_index, vector_index, embedding_model = build_indexes(all_chunks)

        log.write("🧩 Creating agent...")
        agent = build_agent(text_index, vector_index, embedding_model)

        st.session_state.agent = agent
        st.session_state.ready = True

    log.success("✅ Agent ready!")

# --- REPL interaction ---
if st.session_state.ready:
    st.subheader("💬 Ask a question")

    with st.form(key="repl_form", clear_on_submit=True):
        user_query = st.text_input("Your question:")
        submitted = st.form_submit_button("Ask")

    if submitted and user_query.strip():
        with st.spinner("Thinking..."):
            result = run_agent(st.session_state.agent, user_query.strip())
            answer = getattr(result, "output", None) or str(result)

        st.session_state.history.insert(0, (user_query, answer))
        st.rerun()

    if st.session_state.history:
        st.divider()
        for q, a in st.session_state.history:
            st.markdown(f"**❓ {q}**")
            st.markdown(f"🧾 {a}")
            st.divider()
else:
    st.info("👈 Choose params and Initialize the agent using the sidebar.")
