import re
from typing import List, Dict, Any, Literal, Union
from utils import save_chunks_jsonl

def simple_chunking(text: str, size: int, save_file: Union[bool, str] = False) -> List[Dict[str, Any]]:
    if size <= 0:
        raise ValueError("Size must be a positive integer.")

    result: List[Dict[str, Any]] = []
    for i in range(0, len(text), size):
        chunk = text[i:i + size]
        result.append({'start': i, 'end': min(i + size, len(text)), 'chunk': chunk})

    if save_file:
        path = "chunks.jsonl" if isinstance(save_file, bool) else save_file
        save_chunks_jsonl(result, path)
    return result

def sliding_window_chunking(
    text: str,
    size: int,
    step: int,
    save_file: Union[bool, str] = False,
) -> List[Dict[str, Any]]:
    if size <= 0 or step <= 0:
        raise ValueError("Size and step must be positive integers.")

    result: List[Dict[str, Any]] = []
    for i in range(0, len(text), step):
        chunk = text[i:i + size]
        result.append({'start': i, 'end': min(i + size, len(text)), 'chunk': chunk})
        if i + size >= len(text):
            break

    if save_file:
        path = "chunks.jsonl" if isinstance(save_file, bool) else save_file
        save_chunks_jsonl(result, path)
    return result


def paragraph_chunking(text: str, save_file: Union[bool, str] = False) -> List[Dict[str, Any]]:
    paragraphs: List[str] = re.split(r"\n\s*\n", text.strip())
    result: List[Dict[str, Any]] = []
    start = 0
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        end = start + len(p)
        result.append({'start': start, 'end': end, 'chunk': p})
        start = end + 2  # account for skipped newlines

    if save_file:
        path = "chunks.jsonl" if isinstance(save_file, bool) else save_file
        save_chunks_jsonl(result, path)
    return result


def markdown_section_chunking(text: str, level: int = 2, save_file: Union[bool, str] = False) -> List[Dict[str, Any]]:
    header_pattern = r'^(#{' + str(level) + r'} )(.+)$'
    pattern = re.compile(header_pattern, re.MULTILINE)
    parts = pattern.split(text)

    result: List[Dict[str, Any]] = []
    for i in range(1, len(parts), 3):
        header = (parts[i] + parts[i + 1]).strip()
        content = parts[i + 2].strip() if i + 2 < len(parts) else ""
        section = f"{header}\n\n{content}" if content else header
        start = text.find(section)
        end = start + len(section)
        result.append({'start': start, 'end': end, 'chunk': section})

    if save_file:
        path = "chunks.jsonl" if isinstance(save_file, bool) else save_file
        save_chunks_jsonl(result, path)
    return result


def chunk_text(
    text: str,
    method: Literal["simple", "sliding", "paragraph", "section"],
    size: int = 2000,
    step: int = 1000,
    level: int = 2,
    save_file: Union[bool, str] = False
) -> List[Dict[str, Any]]:
    if method == "simple":
        return simple_chunking(text, size, save_file)
    elif method == "sliding":
        return sliding_window_chunking(text, size, step, save_file)
    elif method == "paragraph":
        return paragraph_chunking(text, save_file)
    elif method == "section":
        return markdown_section_chunking(text, level, save_file)
    else:
        raise ValueError(f"Unknown method: {method}")
