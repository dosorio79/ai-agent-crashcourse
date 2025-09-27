import json

def save_chunks_jsonl(chunks, filepath):
    """
    Save a list of chunks to a JSONL (JSON Lines) file.

    Args:
        chunks (list): The data to be saved.
        filepath (str): The path to the output JSONL file.
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

def load_chunks_jsonl(filepath):
    """
    Load chunks from a JSONL (JSON Lines) file.

    Args:
        filepath (str): The path to the JSONL file.

    Returns:
        list: The loaded data from the JSONL file.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f.readlines()]
