import argparse
from pprint import pprint

from read import read_repo_data
from chunks import chunk_text

def parse_args():
    parser = argparse.ArgumentParser(
        description="Demo chunking strategies on a GitHub repo"
    )
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--branch", default="main", help="Branch to read from (default: main)")
    parser.add_argument(
        "--method",
        choices=["simple", "sliding", "paragraph", "section"],
        required=True,
        help="Chunking method to use"
    )
    parser.add_argument("--size", type=int, default=2000, help="Chunk size (for simple/sliding)")
    parser.add_argument("--step", type=int, default=1000, help="Step size / overlap (for sliding)")
    parser.add_argument("--level", type=int, default=2, help="section header level (for section)")
    return parser.parse_args()

def main():
    args = parse_args()

    docs = read_repo_data(args.owner, args.repo, branch=args.branch)
    if not docs:
        print("No documents found in repository.")
        return

    doc = docs[0]
    print(f"📄 Using document: {doc.get('filename', 'unknown')}")

    try:
        chunks = chunk_text(
            doc.get("content", ""),
            method=args.method,
            size=args.size,
            step=args.step,
            level=args.level
        )
    except Exception as e:
        print(f"Error during chunking: {e}")
        return

    print(f"\n✅ Method: {args.method}")
    print(f"Total chunks: {len(chunks)}")
    if chunks:
        print("\n--- First chunk ---")
        pprint(chunks[0])
        if len(chunks) > 1:
            print("\n--- Second chunk ---")
            pprint(chunks[1])
    else:
        print("No chunks produced.")

if __name__ == "__main__":
    main()
