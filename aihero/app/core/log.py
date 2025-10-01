import json
import secrets
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Union

from pydantic_ai.messages import ModelMessagesTypeAdapter


def log_entry(agent: Any, messages: Any, source: str = "user") -> Dict[str, Any]:
    """
    Construct a structured log entry for an agent interaction.

    Args:
        agent: The agent object (must have a .name attribute).
        messages: Messages returned from the agent (pydantic type).
        source: Who initiated the interaction (default: 'user').

    Returns:
        dict: Structured log entry with agent details, tools, and messages.
    """
    tools: List[str] = []
    for ts in getattr(agent, "toolsets", []):
        tools.extend(getattr(ts, "tools", {}).keys())

    dict_messages: List[Dict[str, Any]] = ModelMessagesTypeAdapter.dump_python(messages)

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

    Args:
        agent: The agent object (must have .name attribute).
        messages: Messages returned from the agent (pydantic type).
        source: String describing who triggered the interaction (default: 'user').

    Returns:
        Path: Path to the saved JSON log file.
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    entry: Dict[str, Any] = log_entry(agent, messages, source)

    # Use last message timestamp if available, else fallback to now
    last_msg: Dict[str, Any] = entry["messages"][-1] if entry["messages"] else {}
    ts: Union[datetime, None] = last_msg.get("timestamp", datetime.now())

    ts_str = ts.strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"{entry['agent_name']}_{ts_str}_{rand_hex}.json"
    filepath = log_dir / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath
