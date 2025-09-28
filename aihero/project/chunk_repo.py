import argparse
from pprint import pprint
from tqdm import tqdm

from read import read_repo_data
from chunks import chunk_text
from utils import save_chunks_jsonl


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
    parser.add_argument("--level", type=int, default=2, help="Section header level (for section)")
    parser.add_argument(
        "--save-json",
        nargs="?",
        const=True,
        default=False,
        help="Save chunks to chunks.jsonl. "
             "If provided without a value, defaults to chunks.jsonl. "
             "If a string is provided, that string is used as the filename."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    docs = read_repo_data(args.owner, args.repo, branch=args.branch)
    if not docs:
        print("No documents found in repository.")
        return

    # Collect chunks from all docs
    all_chunks = []
    for doc in tqdm(docs, desc="Chunking docs"):
        chunks = chunk_text(
            doc.get("content", ""),
            method=args.method,
            size=args.size,
            step=args.step,
            level=args.level,
            save_file=False,  # prevent per-doc saving
        )
        for c in chunks:
            c["filename"] = doc.get("filename", "unknown")
        all_chunks.extend(chunks)

    # Save once if requested
    if args.save_json:
        path = "chunks.jsonl" if args.save_json is True else args.save_json
        save_chunks_jsonl(all_chunks, path)
        print(f"\n💾 Saved {len(all_chunks)} chunks to {path}")

    # Preview only first document
    first_doc = docs[0]
    print(f"\n📄 Example document: {first_doc.get('filename', 'unknown')}")
    sample_chunks = [c for c in all_chunks if c["filename"] == first_doc.get("filename")]
    print(f"✅ Method: {args.method}")
    print(f"Total chunks from first doc: {len(sample_chunks)}")
    if sample_chunks:
        print("\n--- First chunk ---")
        pprint(sample_chunks[0])
        if len(sample_chunks) > 1:
            print("\n--- Second chunk ---")
            pprint(sample_chunks[1])
    else:
        print("No chunks produced for first document.")


if __name__ == "__main__":
    main()
