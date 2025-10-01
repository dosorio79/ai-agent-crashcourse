import json
import yaml
from typing import List, Dict, Any
import secrets
from datetime import datetime
from pathlib import Path


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def save_chunks_jsonl(
    chunks: List[Dict[str, Any]],
    owner: str,
    repo: str,
    branch: str,
    strategy: str,
    ensure_ascii: bool = False,
) -> Path:
    """
    Save chunks to JSONL with a structured filename:
    owner_repo_branch_strategy_timestamp_rand.jsonl
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand = secrets.token_hex(2)
    filename = f"{owner.lower()}_{repo.lower()}_{branch.lower()}_{strategy}_{ts}_{rand}.jsonl"
    filepath = DATA_DIR / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        for chunk in chunks:
            json.dump(chunk, f_out, ensure_ascii=ensure_ascii)
            f_out.write("\n")

    return filepath


def load_chunks_jsonl(filepath: Path) -> List[Dict[str, Any]]:
    """
    Load chunks from a JSONL file.
    """
    chunks: List[Dict[str, Any]] = []
    with filepath.open("r", encoding="utf-8") as f_in:
        for line in f_in:
            chunks.append(json.loads(line))

    return chunks


def parse_chunk_filename(filename: str) -> Dict[str, str]:
    """
    Parse a chunk filename into metadata.

    Expected format:
    owner_repo_branch_strategy_timestamp_rand.jsonl
    """
    base = Path(filename).stem
    parts = base.split("_")

    if len(parts) < 6:
        raise ValueError(f"Unexpected chunk filename format: {filename}")

    return {
        "owner": parts[0],
        "repo": parts[1],
        "branch": parts[2],
        "strategy": parts[3],
        "timestamp": parts[4],
        "rand": parts[5],
    }


def list_chunks() -> List[Dict[str, Any]]:
    """
    List all saved chunk files with metadata.

    Returns:
        List of dicts, each containing:
        - path: Path to the file
        - meta: Parsed metadata (owner, repo, branch, strategy, timestamp, rand)
    """
    results = []
    for f in DATA_DIR.glob("*.jsonl"):
        try:
            meta = parse_chunk_filename(f.name)
            results.append({"path": f, "meta": meta})
        except ValueError:
            continue
    return results


def load_yaml_config(path: str) -> Dict[str, Any]:
    """
    Load a YAML config file.

    Args:
        path (str): Path to the YAML file.

    Returns:
        dict: Parsed configuration.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_log_data_from_file(log_file_path: str) -> Dict[str, Any]:
    """
    Load log data from a JSON file.

    Args:
        log_file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed log data.
    """
    with open(log_file_path, 'r') as file_in:
        log_data = json.load(file_in)
        log_data['log_file_path'] = log_file_path
        return log_data
