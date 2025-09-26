import re
from typing import List, Dict, Any, Literal

def simple_chunking(text: str, size: int) -> List[Dict[str, Any]]:
    """Chunk text into non-overlapping chunks of a given size.

    Args:
        text (str): Text to chunk.
        size (int): Size of each chunk.

    Returns:
        list: List of dicts with 'start', 'end', and 'chunk' keys.
    """
    if size <= 0:
        raise ValueError("Size must be positive.")

    result: List[Dict[str, Any]] = []
    for i in range(0, len(text), size):
        chunk = text[i:i + size]
        result.append({'start': i, 'end': i + size, 'chunk': chunk})
    return result


def sliding_window_chunking(text: str, size: int, step: int) -> List[Dict[str, Any]]:
    """Chunk text using a sliding window approach.

    Args:
        text (str): Text to chunk.
        size (int): Size of each chunk.
        step (int): Step size between chunk starts (controls overlap).

    Raises:
        ValueError: If size or step are not positive.

    Returns:
        list: List of dicts with 'start', 'end', and 'chunk' keys.
    """
    if size <= 0 or step <= 0:
        raise ValueError("Size and step must be positive.")

    result: List[Dict[str, Any]] = []
    for i in range(0, len(text), step):
        chunk = text[i:i + size]
        result.append({'start': i, 'end': i + size, 'chunk': chunk})
        if i + size >= len(text):  # reached the end
            break
    return result


def paragraph_chunking(text: str) -> List[Dict[str, Any]]:
    """Split text into paragraphs based on double newlines.

    Args:
        text (str): Text to split.

    Returns:
        list: List of dicts with 'start', 'end', and 'chunk' keys.
    """
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
    return result


def markdown_section_chunking(text: str, level: int = 2) -> List[Dict[str, Any]]:
    """Split markdown text into sections based on header levels.

    Args:
        text (str): Markdown text to split.
        level (int, optional): Header level to split by (e.g., 2 for '##'). Defaults to 2.

    Returns:
        list: List of dicts with 'start', 'end', and 'chunk' keys.
    """
    header_pattern = r'^(#{' + str(level) + r'} )(.+)$'
    pattern = re.compile(header_pattern, re.MULTILINE)
    parts = pattern.split(text)

    result: List[Dict[str, Any]] = []
    start = 0
    for i in range(1, len(parts), 3):
        header = (parts[i] + parts[i+1]).strip()
        content = parts[i+2].strip() if i + 2 < len(parts) else ""
        section_text = f"{header}\n\n{content}" if content else header
        end = start + len(section_text)
        result.append({'start': start, 'end': end, 'chunk': section_text})
        start = end
    return result

def chunk_text(
    text: str,
    method: Literal["simple", "sliding", "paragraph", "markdown"],
    size: int = 2000,
    step: int = 1000,
    level: int = 2
) -> List[Dict[str, Any]]:
    """Dispatch to a chosen chunking strategy.

    Args:
        text (str): Text to chunk.
        method (str): 'simple', 'sliding', 'paragraph', or 'markdown'.
        size (int): Chunk size for 'simple' and 'sliding'.
        step (int): Step size for 'sliding'.
        level (int): Markdown header level for 'markdown'.

    Returns:
        list: List of dicts with 'start', 'end', and 'chunk' keys.
    """
    if method == "simple":
        return simple_chunking(text, size)
    elif method == "sliding":
        return sliding_window_chunking(text, size, step)
    elif method == "paragraph":
        return paragraph_chunking(text)
    elif method == "section":
        return markdown_section_chunking(text, level)
    else:
        raise ValueError(f"Unknown method: {method}")
