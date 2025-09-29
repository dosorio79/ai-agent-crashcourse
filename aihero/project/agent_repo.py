import argparse
from rich.console import Console
from rich.markdown import Markdown

from utils import load_chunks_jsonl
from search import create_text_index, create_vector_index, load_embedding_model
from agent_tools import make_agent_tools
from agent import create_agent, run_agent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run an AI agent over chunked repository data"
    )
    parser.add_argument("--chunks-file", required=True, help="Path to chunks.jsonl file")
    parser.add_argument("--query", required=True, help="User query to ask the agent")
    parser.add_argument("--prompt", default="prompts/system_prompt_strict.yml",
                        help="Path to system prompt YAML (default: prompts/system_prompt_strict.yml)")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM model name")
    parser.add_argument(
        "--tool",
        choices=["text", "vector", "hybrid"],
        required=True,
        help="Which search tool to expose to the agent"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    console = Console()

    # 1. Load chunks
    with console.status("[bold cyan]Loading chunks...", spinner="dots"):
        chunks = load_chunks_jsonl(args.chunks_file)

    # 2. Build indexes
    with console.status("[bold cyan]Building indexes...", spinner="dots"):
        text_index = create_text_index(chunks)
        embedding_model = load_embedding_model()
        vector_index = create_vector_index(chunks, embedding_model)

    # 3. Select tool(s)
    tools = make_agent_tools(text_index, vector_index, embedding_model)
    tool_map = {
        "text": [tools[0]],
        "vector": [tools[1]],
        "hybrid": [tools[2]],
    }
    selected_tools = tool_map[args.tool]

    # 4. Create agent
    agent = create_agent(
        system_prompt_path=args.prompt,
        model_name=args.model,
        tools=selected_tools,
    )

    # 5. Run query with spinner
    console.print(f"🤖 Running agent with [bold green]{args.tool}[/] tool on query:\n[italic]{args.query}[/]\n")
    with console.status("[bold green]Thinking...", spinner="bouncingBall"):
        response = run_agent(agent, args.query)

    # 6. Pretty print result
    if hasattr(response, "output"):
        console.print(Markdown(response.output))
    else:
        console.print("[red]No response text available[/]")


if __name__ == "__main__":
    main()
