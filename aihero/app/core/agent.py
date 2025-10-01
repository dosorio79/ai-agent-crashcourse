import os
from typing import List, Dict, Any, Optional, Type
import asyncio

import dotenv
dotenv.load_dotenv()

from pydantic_ai import Agent
from utils.utils import load_yaml_config


def create_agent(
    prompt_file_path: str,
    model_name: str = "gpt-4o-mini",
    tools: Optional[List[Any]] = None,
    agent_name: str = "Agent",
) -> Agent:
    """
    Create a Pydantic AI agent with a system prompt and optional tools.

    The YAML prompt file must contain a top-level 'instructions' key.
    """
    # Ensure API key is present
    if model_name.startswith("gpt-") and os.getenv("OPENAI_API_KEY") is None:
        raise EnvironmentError("Missing OPENAI_API_KEY in environment.")
    if model_name.startswith("gemini-") and os.getenv("GOOGLE_API_KEY") is None:
        raise EnvironmentError("Missing GOOGLE_API_KEY in environment.")

    # Load prompt instructions
    config = load_yaml_config(prompt_file_path)
    if "instructions" not in config:
        raise KeyError("YAML config must contain an 'instructions' key.")

    return Agent(
        name=agent_name,
        instructions=config["instructions"],
        tools=tools or [],
        model=model_name,
    )


async def run_agent_async(agent_instance: Agent, user_question: str) -> Dict[str, Any]:
    """
    Run the agent asynchronously with a given user question.
    """
    return await agent_instance.run(user_prompt=user_question)


def run_agent(agent_instance: Agent, user_question: str) -> Dict[str, Any]:
    """
    Run the agent synchronously with a given user question.
    """
    return asyncio.run(run_agent_async(agent_instance, user_question))
