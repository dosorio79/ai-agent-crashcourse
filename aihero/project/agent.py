import os
import dotenv
import asyncio
import dotenv
dotenv.load_dotenv()

from typing import List, Dict, Any, Literal, Union

from pydantic_ai import Agent
from utils import load_yaml_config


def create_agent(
    system_prompt_path: str,
    model_name: str = "gpt-4o-mini",
    tools: List[Any] = None,
    agent_name: str = "Agent",
) -> Agent:
    """
    Create a Pydantic AI agent with a system prompt and optional tools.

    Args:
        system_prompt_path (str): Path to YAML file containing the system prompt.
        model_name (str): Name of the LLM model to use.
        tools (List[Any], optional): Python callables to expose as tools. Defaults to None.
        agent_name (str): Name of the agent. Defaults to "Agent".

    Returns:
        Agent: Configured Pydantic AI agent.

    Raises:
        EnvironmentError: If the required API key is missing.
        FileNotFoundError: If the system prompt file is not found.
    """
    # Check for API key
    if model_name.startswith("gpt-"):
        if os.getenv("OPENAI_API_KEY") is None:
            raise EnvironmentError("Missing OPENAI_API_KEY in environment.")
    elif model_name.startswith("gemini-"):
        if os.getenv("GOOGLE_API_KEY") is None:
            raise EnvironmentError("Missing GOOGLE_API_KEY in environment.")

    # Load system prompt
    try:
        cfg = load_yaml_config(system_prompt_path)
        system_prompt = cfg["system_prompt"]
    except FileNotFoundError as e:
        raise FileNotFoundError(f"System prompt file not found: {system_prompt_path}") from e
    except KeyError:
        raise KeyError("YAML config must contain a 'system_prompt' key.")

    return Agent(
        name=agent_name,
        instructions=system_prompt,
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
