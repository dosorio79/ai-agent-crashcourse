import argparse
from utils import load_chunks_jsonl
from search import (
    create_text_index,
    load_embedding_model,
    create_vector_index,
    text_search,
    vector_search,
    hybrid_search,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Search chunks with text, vector, or hybrid mode")
    parser.add_argument("--chunks-file", required=True, help="Path to chunks JSONL file")
    parser.add_argument("--mode", choices=["text", "vector", "hybrid"], required=True, help="Search mode")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    return parser.parse_args()


def main():
    args = parse_args()

    chunks = load_chunks_jsonl(args.chunks_file)
    text_index = create_text_index(chunks)
    model = load_embedding_model()
    vindex = create_vector_index(chunks, model)

    if args.mode == "text":
        results = text_search(text_index, args.query, top_k=args.top_k)
    elif args.mode == "vector":
        results = vector_search(vindex, model, args.query, top_k=args.top_k)
    else:
        results = hybrid_search(text_index, vindex, model, args.query, top_k=args.top_k)

    for i, r in enumerate(results, 1):
        print(f"\nResult {i}")
        print(f"File: {r.get('filename')}")
        print(f"Snippet: {r.get('chunk', '')[:200]}")
        print("---")


if __name__ == "__main__":
    main()
