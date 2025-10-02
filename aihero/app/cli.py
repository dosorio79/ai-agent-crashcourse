import argparse
from core.read import read_repo_data
from core.chunks import chunk_text
from utils.utils import save_chunks_jsonl
from core.search import create_text_index, create_vector_index, load_embedding_model
from core.agent import create_agent, run_agent
from core.agent_tools import make_agent_tools
from yaspin import yaspin
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(description="AI Agent CLI pipeline")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--branch", default="main", help="Branch (default: main)")
    parser.add_argument("--method", choices=["simple", "sliding", "paragraph", "section"], default="section")
    parser.add_argument("--size", type=int, default=1000, help="Chunk size")
    parser.add_argument("--step", type=int, default=500, help="Step size (for sliding)")
    parser.add_argument("--level", type=int, default=2, help="Markdown header level (for section)")
    parser.add_argument("--save-json", nargs="?", const=True, default=False,
                        help="Save chunks to JSONL (default: False). If string provided, use as filename.")
    return parser.parse_args()


def main():
    args = parse_args()

    # Step 1. Load repo + chunk
    console.print(f"📥 Reading repo [bold green]{args.owner}/{args.repo}@{args.branch}[/bold green]...")
    docs = read_repo_data(args.owner, args.repo, branch=args.branch)

    all_chunks = []
    for doc in docs:
        if args.method == "section":
            doc_chunks = chunk_text(doc.get("content", ""), method="section", level=args.level)
        else:
            doc_chunks = chunk_text(doc.get("content", ""), method=args.method,
                                    size=args.size, step=args.step)
        for c in doc_chunks:
            c.update({"filename": doc.get("filename")})
        all_chunks.extend(doc_chunks)

    if args.save_json:
        path = save_chunks_jsonl(all_chunks, args.owner, args.repo, args.branch, args.method)
        console.print(f"✅ Chunks saved to [yellow]{path}[/yellow]")
    else:
        console.print("ℹ️ Chunks not saved to disk")

    # Step 2. Build indexes
    console.print("🔍 Building indexes...")
    text_index = create_text_index(all_chunks)
    embedding_model = load_embedding_model()
    vector_index = create_vector_index(all_chunks, embedding_model)

    # Step 3. Agent setup
    tools = make_agent_tools(text_index, vector_index, embedding_model)
    agent = create_agent(prompt_file_path="prompts/system_prompt.yml",
                         model_name="gpt-4o-mini",
                         tools=tools)

    console.print("\n🤖 Agent ready! Ask questions (type 'exit' to quit).\n")

    # Step 4. REPL loop
    while True:
        try:
            query = console.input("[bold blue]❓ Question:[/bold blue] ").strip()
            if query.lower() in ["exit", "quit"]:
                console.print("👋 Exiting...")
                break
            if not query:
                continue

            with yaspin(text="Thinking...", color="cyan") as spinner:
                result = run_agent(agent, query)
                answer = getattr(result, "output", None) or str(result)
                spinner.ok("✅")

            console.rule("[bold green]🧾 Answer[/bold green]")
            console.print(Markdown(answer))
            console.rule()

        except KeyboardInterrupt:
            console.print("\n👋 Exiting...")
            break


if __name__ == "__main__":
    main()
