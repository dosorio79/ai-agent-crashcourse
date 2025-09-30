import json
import yaml
from typing import List, Dict, Any


def save_chunks_jsonl(chunks: List[Dict[str, Any]], filepath: str):
    """
    Save a list of chunks to a JSONL (JSON Lines) file.

    Args:
        chunks (list): The data to be saved.
        filepath (str): The path to the output JSONL file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_chunks_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """
    Load chunks from a JSONL (JSON Lines) file.

    Args:
        filepath (str): The path to the JSONL file.

    Returns:
        list: The loaded data from the JSONL file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f.readlines()]


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
