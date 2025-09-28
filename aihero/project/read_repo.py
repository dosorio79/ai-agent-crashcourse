from read import read_repo_data
import argparse
from pprint import pprint

def main():
    """
    Parses command-line arguments to specify a GitHub repository and branch, reads the repository data,
    and prints the number of FAQ documents along with the first two entries.

    Command-line Arguments:
        --owner (str): Repository owner (required).
        --repo (str): Repository name (required).
        --branch (str): Branch to read from (default: "main").

    Returns:
        None

    Side Effects:
        Prints the number of FAQ documents and the first two FAQ entries to stdout.
    """
    parser = argparse.ArgumentParser(description="Read a GitHub repo data.")
    parser.add_argument("--owner", type=str, required=True, help="Repository owner")
    parser.add_argument("--repo", type=str, required=True, help="Repository name")
    parser.add_argument("--branch", type=str, default="main", help="Branch to read from")
    args = parser.parse_args()
    repo_data = read_repo_data(args.owner, args.repo, branch=args.branch)
    print(f"FAQ documents: {len(repo_data)}")
    pprint(repo_data[0])

if __name__ == "__main__":
    main()
