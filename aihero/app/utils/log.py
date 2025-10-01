import json
import secrets
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Union

from pydantic_ai.messages import ModelMessagesTypeAdapter


def log_entry(agent: Any, messages: Any, source: str = "user") -> Dict[str, Any]:
    """
    Construct a structured log entry for an agent interaction.
    """
    tools: List[str] = []
    for ts in getattr(agent, "toolsets", []):
        tools.extend(getattr(ts, "tools", {}).keys())

    raw_messages = ModelMessagesTypeAdapter.dump_python(messages)

    # Normalize to list of dicts
    if isinstance(raw_messages, dict):
        dict_messages: List[Dict[str, Any]] = [raw_messages]
    elif isinstance(raw_messages, list):
        dict_messages = raw_messages
    else:
        dict_messages = []

    return {
        "agent_name": getattr(agent, "name", "unknown"),
        "system_prompt": getattr(agent, "_instructions", None),
        "provider": getattr(getattr(agent, "model", None), "system", None),
        "model": getattr(getattr(agent, "model", None), "model_name", None),
        "tools": tools,
        "messages": dict_messages,
        "source": source,
    }


def serializer(obj: Any) -> str:
    """
    Custom serializer for objects that aren't natively JSON serializable.

    Currently only supports datetime -> ISO 8601 string.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def log_interaction_to_file(agent: Any, messages: Any, source: str = "user") -> Path:
    """
    Save an agent interaction log to a uniquely named JSON file.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    entry: Dict[str, Any] = log_entry(agent, messages, source)

    # Safely handle last message
    last_msg: Dict[str, Any] = entry.get("messages", [])[-1] if entry.get("messages") else {}
    ts: datetime = last_msg.get("timestamp", datetime.now())

    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"{entry['agent_name']}_{ts_str}_{rand_hex}.json"
    filepath = log_dir / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath
