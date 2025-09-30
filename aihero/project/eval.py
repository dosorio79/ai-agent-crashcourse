import random
from typing import List, Dict, Any
from pydantic_ai import Agent
import json

from prompts.templates import user_prompt_template   # XML evaluation prompt template
from agent import run_agent_async
from schemas.evaluation import EvaluationChecklist


async def generate_questions_from_chunks(
    chunks: List[Dict[str, Any]],
    qgen_agent: Agent,
    prompt_template: str,
    num_questions: int = 10,
    random_seed: int = 42,
) -> List[Dict[str, str]]:
    """
    Generate questions from chunks using a question generation agent.

    Args:
        chunks: List of dictionaries containing chunk metadata.
        qgen_agent: Question generation agent.
        prompt_template: Template for generating prompts.
        num_questions: Number of questions to generate.
        random_seed: Random seed for reproducibility.

    Returns:
        List of dictionaries containing filename and generated question.
    """
    if num_questions > len(chunks):
        num_questions = len(chunks)

    random.seed(random_seed)
    sampled_chunks = random.sample(chunks, num_questions)

    questions = []
    for chunk in sampled_chunks:
        prompt = prompt_template.replace("<CONTENT>", chunk["chunk"])
        response = await run_agent_async(qgen_agent, prompt)

        # Extract the first question string
        question = response.output.questions[0]

        questions.append({
            "filename": chunk.get("filename", "unknown"),
            "question": question
        })

    return questions


def simplify_log_messages(
    log_messages: List[Dict[str, Any]],
    keep_timestamps: bool = False
) -> List[Dict[str, Any]]:
    """
    Simplify log messages by stripping unnecessary fields to save tokens.

    Args:
        log_messages: List of raw log messages from the agent.
        keep_timestamps: Whether to keep timestamps (default: False).

    Returns:
        A simplified list of log messages with unneeded fields removed.
    """
    simplified_messages: List[Dict[str, Any]] = []

    for message in log_messages:
        parts: List[Dict[str, Any]] = []

        for part in message["parts"]:
            simplified_part: Dict[str, Any] = part.copy()
            kind: str = part["part_kind"]

            if kind == "user-prompt":
                if not keep_timestamps:
                    simplified_part.pop("timestamp", None)
            elif kind == "tool-call":
                simplified_part.pop("tool_call_id", None)
            elif kind == "tool-return":
                simplified_part.pop("tool_call_id", None)
                simplified_part.pop("metadata", None)
                if not keep_timestamps:
                    simplified_part.pop("timestamp", None)
                simplified_part["content"] = "RETURN_RESULTS_REDACTED"
            elif kind == "text":
                simplified_part.pop("id", None)

            parts.append(simplified_part)

        simplified_messages.append({
            "kind": message["kind"],
            "parts": parts,
        })

    return simplified_messages


def extract_question_answer(messages: list[Dict[str, Any]]) -> tuple[str, str]:
    """
    Extract the user question and model answer from log messages.
    - Finds the first 'user-prompt'
    - Finds the last 'text' message
    """
    question, answer = None, None

    # First user prompt
    for m in messages:
        for p in m.get("parts", []):
            if p.get("part_kind") == "user-prompt":
                question = p.get("content")
                break
        if question:
            break

    # Last model text
    for m in reversed(messages):
        for p in m.get("parts", []):
            if p.get("part_kind") == "text":
                answer = p.get("content")
                break
        if answer:
            break

    return question, answer


async def evaluate_log_record(
    eval_agent, log_record: Dict[str, Any]
) -> EvaluationChecklist:
    """
    Evaluate a single log record using the evaluation agent.
    Faithful to the tutorial: simplify messages, build XML prompt, run eval agent.
    """
    messages = log_record["messages"]

    # Extract question and answer
    question, answer = extract_question_answer(messages)
    if not question or not answer:
        raise ValueError("Could not extract question or answer from log messages.")

    # System instructions
    instructions = log_record.get("system_prompt", "")

    # Simplify log for token efficiency
    log_simplified = simplify_log_messages(messages)
    log_str = json.dumps(log_simplified)

    # Build evaluation prompt
    user_prompt = user_prompt_template.format(
        instructions=instructions,
        question=question,
        answer=answer,
        log=log_str,
    )

    # Run evaluation agent
    result = await run_agent_async(
        eval_agent, user_prompt
    )
    return result.output
