import os
from typing import List, Dict, Any
import asyncio

import dotenv
dotenv.load_dotenv()

from pydantic_ai import Agent
from utils import load_yaml_config


def create_agent(
    prompt_file_path: str,
    model_name: str = "gpt-4o-mini",
    tools: List[Any] | None = None,
    agent_name: str = "Agent",
    **kwargs
) -> Agent:
    """
    Create a Pydantic AI agent with a system or evaluation prompt and optional tools.

    The YAML prompt file must contain a top-level 'instructions' key.

    Args:
        prompt_file_path (str): Path to YAML file containing the prompt.
        model_name (str): Name of the LLM model to use (default: gpt-4o-mini).
        tools (List[Any] | None): Python callables to expose as tools (default: None).
        agent_name (str): Name of the agent (default: "Agent").

    Returns:
        Agent: Configured Pydantic AI agent.

    Raises:
        EnvironmentError: If the required API key is missing.
        FileNotFoundError: If the prompt file is not found.
        KeyError: If the YAML config does not contain 'instructions'.
    """
    if model_name.startswith(("gpt-", "gemini-")):
        api_key_env_var = "OPENAI_API_KEY" if model_name.startswith("gpt-") else "GOOGLE_API_KEY"
        if os.getenv(api_key_env_var) is None:
            raise EnvironmentError(f"Missing {api_key_env_var} in environment.")

    try:
        config = load_yaml_config(prompt_file_path)
        instructions = config["instructions"]
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file_path}") from e
    except KeyError:
        raise KeyError("YAML config must contain an 'instructions' key.")

    return Agent(
        name=agent_name,
        instructions=instructions,
        tools=tools or [],
        model=model_name,
        **kwargs
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
